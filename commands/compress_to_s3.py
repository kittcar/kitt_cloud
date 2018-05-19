#!usr/bin/env python3
import argparse
import sys
sys.path.append("..")
from utils.compress import Compress

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ext', default='.tgz', help='The compression type')
    parser.add_argument('--bucket', default='logs.kittcar.com', help='S3 bucket to upload to')
    parser.add_argument('--profile', default='KITT', help='Your AWS configuration profile name')
    parser.add_argument('dir', help='Path to the folder to compress')

    args = parser.parse_args()

    compress = Compress(args.ext)
    compress.add(args.dir)
    compress.close()
    compress.upload(args.bucket, args.profile)
    compress.delete()
