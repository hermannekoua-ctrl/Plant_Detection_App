#!/usr/bin/env python3
"""Unzip a SavedModel archive and convert it to TensorFlow Lite.

Usage:
  python convert_saved_model_to_tflite.py --zip plant_disease_saved_model-...zip
  python convert_saved_model_to_tflite.py --dir extracted_folder

Options:
  --zip   Path to the ZIP that contains a TensorFlow SavedModel directory or a Keras .h5
  --dir   Path to a directory containing a SavedModel (or .h5)
  --out   Output tflite path (default: assets/models/plant_model.tflite)
  --quantize  Enable post-training quantization (default: false)

Note: Run this on a machine with TensorFlow installed (pip install tensorflow).
"""
import argparse
import os
import zipfile
import shutil
import sys


def extract_zip(zip_path, dest):
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(dest)


def find_saved_model_dir(root):
    # Look for directory containing saved_model.pb
    for dirpath, dirnames, filenames in os.walk(root):
        if 'saved_model.pb' in filenames:
            return dirpath
    # fallback: look for .h5
    for file in os.listdir(root):
        if file.endswith('.h5') or file.endswith('.keras'):
            return os.path.join(root, file)
    return None


def convert(saved_model_path, out_path, quantize=False):
    import tensorflow as tf

    if os.path.isdir(saved_model_path):
        print('Converting SavedModel at', saved_model_path)
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
    else:
        # assume keras .h5
        print('Converting Keras model file', saved_model_path)
        model = tf.keras.models.load_model(saved_model_path)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)

    if quantize:
        print('Enabling post-training quantization (may require representative dataset)')
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_model = converter.convert()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(tflite_model)
    print('Wrote', out_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zip', help='ZIP file containing SavedModel or .h5')
    parser.add_argument('--dir', help='Directory containing SavedModel or .h5')
    parser.add_argument('--out', default=os.path.join('assets', 'models', 'plant_model.tflite'))
    parser.add_argument('--quantize', action='store_true')
    args = parser.parse_args()

    temp_dir = None
    try:
        if args.zip:
            if not os.path.exists(args.zip):
                print('ZIP not found:', args.zip)
                sys.exit(1)
            temp_dir = os.path.join(os.getcwd(), 'tmp_extracted_model')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir, exist_ok=True)
            print('Extracting', args.zip, '->', temp_dir)
            extract_zip(args.zip, temp_dir)
            model_path = find_saved_model_dir(temp_dir)
        elif args.dir:
            model_path = find_saved_model_dir(args.dir)
        else:
            parser.print_help()
            sys.exit(1)

        if not model_path:
            print('Could not find SavedModel or .h5 inside the provided path')
            sys.exit(1)

        convert(model_path, args.out, quantize=args.quantize)

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
