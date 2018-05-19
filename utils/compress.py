#!/usr/bin/env python3
from datetime import datetime
import os
import sys
import re
import tarfile
import boto3
import logging

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

            Raises:
                IOError: Is raised when the file/folder to compress is not found
        """
        if not os.path.exists(path):
            logger.error('[' + self.arcname + '] ERROR: ' + path + ' does not exist')
            raise IOError(path + ' not found')
        
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

    def upload(self, bucket, profile):
        """ Function to upload the tarfile to S3

            Raises:
                botocore.exceptions.ProfileNotFound: Is raised when AWS config credentials are not found
                boto3.exceptions.S3UploadFailedError: Is raised when the upload to S3 fails
        """
        try:
            session = boto3.Session(profile_name=profile)
            conn = session.client('s3')
        except Exception as e:
            logger.exception('[' + self.arcname + '] Error fetching S3 credentials - ' + str(e))
            raise
        try:
            conn.upload_file(self.arcfile.name, bucket, os.path.basename(self.arcfile.name))
            logger.info('[' + self.arcname + '] Successfully uploaded to ' + bucket)
        except Exception as e:
            logger.exception('[' + self.arcname + '] Error uploading to S3 - ' + str(e))
            raise
