#!/usr/bin/python
# -*- coding: utf-8 -*-
from resizeimage import resizeimage
from PIL import Image
from os.path import join, exists, basename
from os import makedirs, chmod, rmdir, remove
from shutil import rmtree
from base64 import b64decode
import cStringIO

'''
400*400 - small gallery size
800*600 - large gallery size
banner: 1680*945
3200*1800
'''

'''
Here be objects to handle different types of image uploads.
We take a byte stream of an image, convert it into a PIL.Image() type
resize it to the multiple sizes that are input in self.image_specs
and save those to the incoming upload_path
If we receive a subfolder_name we then split out the image into a specific sub-folder
Ex: /profile_pics/<user_id>/image.png
'''

__version__ = '1.0.0'


class UploadImage(object):
    """
    Requires:
        image: the actual image, type: werkzeug.datastructures.FileStorage
        upload path: path to images
        image_specs: a configuration point that includes image names and
            related sizes that you want to create
    Optional:
        subfolder_name: will sort into a specific subfolder if passed in. This is user_id for user profile pics
            and doll_id for doll pics, etc.
        image_name: used primarily for quill images, this will save only one copy of the image in the original size
        encoding: options are 'werkzeug or base64, dependent on the type of image we're uploading
    """
    def __init__(self, image, upload_path, image_specs=None, subfolder_name=None, image_name=None, encoding='werkzeug'):
        self.encoding = encoding.lower()
        if image_name:
            self.image_name = image_name.lower()
        else:
            self.image_name = None

        if self.encoding == 'werkzeug':
            self.image = image.stream
        elif self.encoding == 'base64':
            self.image = image

        self.image_specs = image_specs
        if self.image_specs is None:
            self.image_specs = []
        self.file_type = None

        try:
            content_type = image.headers['Content-Type'].lower()
        except:
            content_type = 'image/png'
        if content_type == 'image/png':
            self.file_type = 'jpg'
        elif content_type == 'image/jpg' or content_type == 'image/jpeg':
            self.file_type = 'jpg'

        if subfolder_name:
            self.upload_path = join(upload_path, subfolder_name)
        else:
            self.upload_path = upload_path

    def resize_and_save_image(self):
            if self.file_type is None:
                return False, 'Bad File Type'
            elif not all([self.image, self.upload_path]):
                return False, 'Not enough information to perform task'
            else:
                try:
                    if self.encoding == 'base64':
                        decoded_data = b64decode(self.image)
                        image_buffer = cStringIO.StringIO(decoded_data)
                        image = Image.open(image_buffer)
                    else:
                        image = Image.open(self.image)
                    if not exists(self.upload_path):
                        makedirs(self.upload_path)
                except Exception, e:
                    return False, 'Fatal exception resizing image (before saving image): {}'.format(e)

                if self.image_name:
                    try:
                        size = image.size
                        new_image = resizeimage.resize_cover(image=image, size=size)
                        full_upload_path = '{}.{}'.format(join(self.upload_path, self.image_name), self.file_type)
                        new_image.save(full_upload_path, image.format)
                        chmod(full_upload_path, 0666)
                    except Exception, e:
                        return False, 'Fatal exception resizing image with image name: {}'.format(e)
                else:
                    try:
                        # Create sized copies as defined in IMAGE_SPECS configs
                        for image_spec in self.image_specs:
                            # image = Image.open(self.image)
                            size = image_spec['size']
                            if size == 'original':
                                size = image.size
                            new_image = resizeimage.resize_cover(image=image, size=size)
                            full_upload_path = '{}.{}'.format(join(self.upload_path, image_spec['image_name']), self.file_type)
                            new_image.save(full_upload_path, image.format)
                            chmod(full_upload_path, 0666)
                    except Exception, e:
                        rmtree(self.upload_path)
                        return False, 'Fatal exception resizing image with image specs: {}'.format(e)
                return True, 'Success'



class RemoveImageDirectory(object):
    """
        Meant for removing a full directory of images,
        for example, all profile pictures for a single user
        Requires:
            upload path: path to images
        Optional:
            subfolder_name: deletes the subfolder
        """

    def __init__(self, upload_path, subfolder_name=None):

        if subfolder_name:
            self.upload_path = join(upload_path, subfolder_name)
        else:
            self.upload_path = upload_path

    def remove_image_directory(self):
        try:
            rmtree(self.upload_path)
            return True, 'Success'
        except Exception, e:
            return False, 'Fatal exception removing directory: {}'.format(e)
