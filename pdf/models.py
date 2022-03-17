from django.db import models

def local_image_upload_path(instance, filename):
    return f'static/media/{filename}'

class My_model(models.Model):
    pdf = models.FileField(upload_to=local_image_upload_path)


    def __str__(self):
        return self.pdf
