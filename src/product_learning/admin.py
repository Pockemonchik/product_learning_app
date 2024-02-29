from django.contrib import admin
from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name", "creator", "start_date", "stop_date", "price")
    list_filter = ("name", "creator", "start_date", "stop_date", "price")
    search_fields = ("name", "creator", "start_date", "stop_date", "price")


admin.site.register(Product, ProductAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(StudentGroup)
# Register your models here.
