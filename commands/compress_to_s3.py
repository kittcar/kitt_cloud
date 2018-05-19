import argparse
import sys
sys.path.append("..")
from utils.compress import Compress

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ext', default='.tgz', help='The compression type')
    parser.add_argument('dir', nargs='+', help='Path to the folder(s) to compress')
    args = parser.parse_args()

    compress = Compress(args.ext)

    for path in args.dir:
        compress.add(path)

    compress.close()
    compress.upload()
    compress.delete()
