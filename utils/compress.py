#!/usr/bin/python3
from datetime import datetime
import os
import sys
sys.path.append("..")
import settings
import re
import tarfile
import settings
import boto3
import logging

S3_BUCKET_NAME = getattr(settings, "S3_BUCKET_NAME", None)
S3_ACCESS_KEY_ID = getattr(settings, "S3_ACCESS_KEY_ID", None)
S3_SECRET_ACCESS_KEY = getattr(settings, "S3_SECRET_ACCESS_KEY", None)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Compress:
    def __init__(self, extension):
        self.ext = extension
        self.secret = ""
        self.output = None
        self.output_fn = datetime.now().isoformat()
        self.open()

    def open(self):
        if(re.match('^\.?tgz$', self.ext, re.IGNORECASE)):
            try:
                self.output = tarfile.open(self.output_fn + '.tar.gz', 'w:gz')
            except Exception as e:
                logger.exception('[' + self.output_fn + \
                                 '] Unable to create output file for writing ' + str(e))
                sys.exit(0)
        else:
            logger.error('[' + self.output_fn + '] Invalid compression type ' + self.ext)
            sys.exit(0)

    def add(self, path):
        if(not os.path.exists(path)):
            logger.error('[' + self.output_fn + '] ERROR: ' + path + ' does not exist')
            return
        if(os.path.isfile(path)):
            self.output.add(path, arcname=os.path.basename(path))
        else:
            self.output.add(path, arcname=self.output_fn)

    def close(self):
        if(self.output is not None):
            self.output.close()

    def delete(self):
        os.remove(self.output.name)

    def send_to_s3(self):
        if(not S3_BUCKET_NAME or not S3_ACCESS_KEY_ID or not S3_SECRET_ACCESS_KEY):
            logger.error('[' + self.output_fn + '] Could not find S3 information from settings')
            sys.exit(0)
        conn = boto3.client(
            's3',
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY
        )
        conn.upload_file(self.output.name, S3_BUCKET_NAME, os.path.basename(self.output.name))
        logger.info('[' + self.output_fn + '] Successfully uploaded to ' + S3_BUCKET_NAME)
