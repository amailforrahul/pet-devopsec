""" Admin doc file this is modified"""

from django.contrib import admin
from .models import pet, User, Book

# Register your models here.

admin.site.register(pet)
admin.site.register(User)
admin.site.register(Book)


