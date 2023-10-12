from django.contrib import admin
from .models import VIDEOS,IMAGES,TestFile
# Register your models here.
admin.site.register(VIDEOS)
admin.site.register(TestFile)
admin.site.register(IMAGES)