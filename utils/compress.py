#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import re
import tarfile
import boto3
import logging

S3_BUCKET_NAME = "logs.kittcar.com"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Compress:
    """Class to combine and compress files to a tarball

    Note:
        Currently only supports .tgz format

    Args:
        extension (str): The file compression format

    """
    def __init__(self, extension):
        self.ext = extension
        self.secret = ""
        self.arcfile = None
        self.arcname = datetime.now().isoformat()
        self._open()

    def _open(self):
        """ Function to open the tarfile for writing

            Raises:
                ReadError: Is raised when a tar archive is opened, that either cannot
                    be handled by the tarfile module or is somehow invalid.
                ValueError: Is raised when the given compression type is not supported
        """
        if re.match('^\.?tgz$', self.ext, re.IGNORECASE):
            try:
                self.arcfile = tarfile.open(self.arcname + '.tar.gz', 'w:gz')
            except Exception as e:
                logger.exception('[' + self.arcname + \
                                 '] Unable to create output file for writing ' + str(e))
                raise tarfile.ReadError('Unable to create output file for writing')
        else:
            logger.error('[' + self.arcname + '] Invalid compression type ' + self.ext)
            raise ValueError('Invalid compression type ' + self.ext)

    def add(self, path):
        """ Function to add a file to the tarfile
        """
        if not os.path.exists(path):
            logger.error('[' + self.arcname + '] ERROR: ' + path + ' does not exist')
            raise IOError(path + ' not found')
        if os.path.isfile(path):
            self.arcfile.add(path, arcname=os.path.basename(path))
        else:
            self.arcfile.add(path, arcname=self.arcname)

    def close(self):
        """ Function to close the open tarfile
        """
        if self.arcfile:
            self.arcfile.close()

    def delete(self):
        """ Function to delete the tarfile from the filesystem
        """
        if self.arcfile:
            os.remove(self.arcfile.name)

    def upload(self):
        """ Function to upload the tarfile to S3
        """
        try:
            session = boto3.Session(profile_name='KITT')
            conn = session.client('s3')
        except Exception as e:
            logger.exception('[' + self.arcname + '] Error fetching S3 credentials - ' + str(e))
            raise
        try:
            conn.upload_file(self.arcfile.name, S3_BUCKET_NAME, os.path.basename(self.arcfile.name))
            logger.info('[' + self.arcname + '] Successfully uploaded to ' + S3_BUCKET_NAME)
        except Exception as e:
            logger.exception('[' + self.arcname + '] Error uploading to S3 - ' + str(e))
            raise