from django.contrib import admin
from .models import *


# 注册数据表
# Register your models here.
@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'statua']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'name', 's_time', 'e_time']
