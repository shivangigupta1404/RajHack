from django.contrib import admin
from .models import *

class BlockAdmin(admin.ModelAdmin):
    list_display = ('index','timestamp','hash','previous_hash','title','text','image')

admin.site.register(Block,BlockAdmin)