from django.contrib import admin
from .models import File, Link
from django.contrib.auth.models import User

# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display= ['name', 'file']



@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display= ['name', 'link']