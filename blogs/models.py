from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField

# Create your models here.


class Blogs(models.Model):
    THEME = "THEME UPDATE"
    UPDATE = "GENERAL UPDATE"
    TUTORIAL = "TUTORIAL"

    CAT_CHOICES = [
        (THEME,"Theme Update"),
        (UPDATE,"General Update"),
        (TUTORIAL,"Tutorial")
    ]

    category = models.CharField(choices=CAT_CHOICES,max_length=50,null=True,blank=True)
    
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from = "title",unique=True,null=True,default=None)

    sub_desc = models.CharField(max_length=255)
    description = HTMLField()
    thumbnail = models.ImageField(upload_to="blogs_thumbnail",blank=True,null=True)

    def __str__(self):
        return self.title


