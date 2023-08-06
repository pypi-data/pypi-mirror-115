import pix2tex
from dataset.dataset import test_transform

import pandas.io.clipboard as clipboard
from PIL import ImageGrab
from PIL import Image
import os
import sys
import argparse
import logging
import yaml
import re
import latex2mathml.converter
import numpy as np
import torch
import natsort

from torchvision import transforms
from munch import Munch
from transformers import PreTrainedTokenizerFast
from timm.models.resnetv2 import ResNetV2
from timm.models.layers import StdConv2dSame

from dataset.latex2png import tex2pil
from models import get_model
from utils import *

last_pic = None



def minmax_size(img, max_dimensions):
    ratios = [a/b for a, b in zip(img.size, max_dimensions)]
    if any([r > 1 for r in ratios]):
        size = np.array(img.size)//max(ratios)
        img = img.resize(size.astype(int), Image.BILINEAR)
    return img

def initialize(arguments=None):
    if arguments is None:
        arguments = Munch({'config': 'settings/config.yaml', 'checkpoint': 'checkpoints/weights.pth', 'no_cuda': True, 'no_resize': False})
    logging.getLogger().setLevel(logging.FATAL)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    with open(arguments.config, 'r') as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    args = Munch(params)
    args.update(**vars(arguments))
    args.wandb = False
    args.device = 'cuda' if torch.cuda.is_available() and not args.no_cuda else 'cpu'

    model = get_model(args)
    model.load_state_dict(torch.load(args.checkpoint, map_location=args.device))

    if 'image_resizer.pth' in os.listdir(os.path.dirname(args.checkpoint)) and not arguments.no_resize:
        image_resizer = ResNetV2(layers=[2, 3, 3], num_classes=22, global_pool='avg', in_chans=1, drop_rate=.05,
                                 preact=True, stem_type='same', conv_layer=StdConv2dSame).to(args.device)
        image_resizer.load_state_dict(torch.load(os.path.join(os.path.dirname(args.checkpoint), 'image_resizer.pth'), map_location=args.device))
        image_resizer.eval()
    else:
        image_resizer = None
    tokenizer = PreTrainedTokenizerFast(tokenizer_file=args.tokenizer)
    return args, model, image_resizer, tokenizer


def call_model(args, model, image_resizer, tokenizer, img=None):
    global last_pic
    encoder, decoder = model.encoder, model.decoder
    if type(img) is bool:
        img = None
    if img is None:
        if last_pic is None:
            print('Provide an image.')
            return
        else:
            img = last_pic.copy()
    else:
        last_pic = img.copy()
    img = minmax_size(pad(img), args.max_dimensions)
    if image_resizer is not None and not args.no_resize:
        with torch.no_grad():
            input_image = pad(img).convert('RGB').copy()
            r, w = 1, img.size[0]
            for i in range(10):
                img = minmax_size(input_image.resize((w, int(input_image.size[1]*r)), Image.BILINEAR if r > 1 else Image.LANCZOS), args.max_dimensions)
                t = test_transform(image=np.array(pad(img).convert('RGB')))['image'][:1].unsqueeze(0)
                w = image_resizer(t.to(args.device)).argmax(-1).item()*32
                if (w/img.size[0] == 1):
                    break
                r *= w/img.size[0]
    else:
        img = np.array(pad(img).convert('RGB'))
        t = test_transform(image=img)['image'][:1].unsqueeze(0)
    im = t.to(args.device)

    with torch.no_grad():
        model.eval()
        device = args.device
        encoded = encoder(im.to(device))
        dec = decoder.generate(torch.LongTensor([args.bos_token])[:, None].to(device), args.max_seq_len,
                               eos_token=args.eos_token, context=encoded.detach(), temperature=args.get('temperature', .25))
        pred = post_process(token2str(dec, tokenizer)[0])
    clipboard.copy(pred)
    return pred


def output_prediction(pred, args):
    print("LaTex : ", pred, '\n')

    if args.show or args.katex:
        try:
            if args.katex:
                raise ValueError
            tex2pil([f'$${pred}$$'])[0].show()
        except Exception as e:

            # render using katex
            import webbrowser
            from urllib.parse import quote
            url = 'https://katex.org/?data=' + \
                quote('{"displayMode":true,"leqno":false,"fleqn":false,"throwOnError":true,"errorColor":"#cc0000",\
"strict":"warn","output":"htmlAndMathml","trust":false,"code":"%s"}' % pred.replace('\\', '\\\\'))
            webbrowser.open(url)

def convert(file_path, option):
    """
    list_png = r'.png'
    list_PNG = r'.PNG'


    png_file_list = [os.path.join(file_path, file) for file in
                     os.listdir(file_path) if file.endswith((list_png, list_PNG))]
    png_file_list = natsort.natsorted(png_file_list)
    """
    parser = argparse.ArgumentParser(description='Use model', add_help=False)
    parser.add_argument('-t', '--temperature', type=float, default=.333, help='Softmax sampling frequency')
    parser.add_argument('-c', '--config', type=str, default='settings/config.yaml')
    parser.add_argument('-m', '--checkpoint', type=str, default='checkpoints/weights.pth')
    parser.add_argument('-s', '--show', action='store_true', help='Show the rendered predicted latex code')
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Predict LaTeX code from image file instead of clipboard')
    parser.add_argument('-k', '--katex', action='store_true', help='Render the latex code in the browser')
    parser.add_argument('--no-cuda', action='store_true', help='Compute on CPU')
    parser.add_argument('--no-resize', action='store_true', help='Resize the image beforehand')
    arguments = parser.parse_args()
    latexocr_path = os.path.dirname(sys.argv[0])
    if latexocr_path != '':
        sys.path.insert(0, latexocr_path)
        os.chdir(latexocr_path)

    args, *objs = initialize(arguments)

    instructions = file_path


    possible_file = instructions.strip()
    ins = possible_file.lower()

    if ins in ['show', 'katex', 'no_resize']:
        setattr(args, ins, not getattr(args, ins, False))
        print('set %s to %s' % (ins, getattr(args, ins)))
        #continue
    elif os.path.isfile(possible_file):
        args.file = possible_file
    else:
        t = re.match(r't=([\.\d]+)', ins)
        if t is not None:
            t = t.groups()[0]
            args.temperature = float(t) + 1e-8
            print('new temperature: T=%.3f' % args.temperature)
            #continue
    try:
        img = None
        if args.file:
            img = Image.open(args.file)
        else:
            try:
                img = ImageGrab.grabclipboard()
            except:
                pass

        if option == 'latex':
            pred = call_model(args, *objs, img=img)
            output_prediction(pred, args)

            out_dir, files_name = os.path.split(file_path)
            filename_sans_extension = os.path.splitext(files_name)[0]
            os.makedirs(os.path.join(out_dir, filename_sans_extension), exist_ok=True)
            output_dir = os.path.join(out_dir, filename_sans_extension)
            fsave = os.path.join(output_dir, files_name)
            fsave = fsave + 'LaTex.txt'

            f = open(fsave, 'w')
            f.write(pred)
            f.close()

        elif option == 'mathml':
            pred = call_model(args, *objs, img=img)
            mathml_output = latex2mathml.converter.convert(pred)  # mathml 출력문
            print("mathml : ", mathml_output, '\n')  # mathml 출력문

            out_dir, files_names = os.path.split(file_path)
            filename_sans_extension = os.path.splitext(files_names)[0]
            os.makedirs(os.path.join(out_dir, filename_sans_extension), exist_ok=True)
            output_dir = os.path.join(out_dir, filename_sans_extension)
            fsaves = os.path.join(output_dir, files_names)
            fsaves = fsaves + 'MathML.txt'

            f = open(fsaves, 'w')
            f.write(mathml_output)
            f.close()

    except KeyboardInterrupt:
        pass
    args.file = None


