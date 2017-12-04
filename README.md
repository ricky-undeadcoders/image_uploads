#image_uploads

Installation instructions:

Add the following to requirements.txt
```
certifi==2017.7.27.1
chardet==3.0.4
idna==2.6
Pillow==4.2.1
python-resize-image==1.1.11
requests==2.18.4
olefile==0.44
urllib3==1.22
```

Drop the image_uploads folder into the application directory

Add the following to base_config:
```python
IMAGE_UPLOAD_ROOT_PATH = '/uploads'
```

You need to add a configuration point for each type of image we'll be uploading
```python
CAROUSEL_IMAGE_UPLOAD_PATH = '/uploads/CarouselImages'
CAROUSEL_IMAGE_MAX_COUNT = 8
CAROUSEL_IMAGE_SPECS = [{'image_name': 'lg',
                         'size': 'original'},
                        {'image_name': 'sm',
                         'size': [400, 400]}]
GALLERY_IMAGE_UPLOAD_PATH = '/uploads/GalleryImages'
GALLERY_IMAGE_SPECS = [{'image_name': 'lg',
                        'size': 'original'},
                       {'image_name': 'sm',
                        'size': [400, 400]}]
POST_IMAGE_UPLOAD_PATH = '/uploads/PostImages'
POST_IMAGE_SPECS = [{'image_name': 'lg',
                     'size': 'original'},
                    {'image_name': 'sm',
                     'size': [400, 400]}]
```

Here's an example of how to use this feature to upload a new image
```python
upload_pic = UploadImage(image=self.image.data,
                            upload_path=current_app.config['QUILL_IMAGE_UPLOAD_PATH'],
                            image_specs=current_app.config['QUILL_IMAGE_SPECS'],
                            subfolder_name=self.field_name.data,
                            image_name=str(self.image_id.data),
                            encoding='base64')
success, data = upload_pic.resize_and_save_image()
```

Make sure to add the directories that you're uploading into to the installation script:
```bash
UPLOAD_DIRS=("Quill" "PostImages" "GalleryImages")
```