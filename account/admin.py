from multiprocessing.resource_tracker import register
from .models import Person
from django.contrib import admin

# Register your models here.
admin.site.register(Person)
