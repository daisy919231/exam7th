from django.contrib import admin
from course.models import Category, Course, Comment, Video, Teacher, Customer
# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Teacher)
admin.site.register(Customer)