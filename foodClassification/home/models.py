from django.db import models

# Create your models here.

class File_upload(models.Model):
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        print(self.file.name)
        return self.file.name