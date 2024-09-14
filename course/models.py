from django.db import models
from user.models import CustomUser

# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Category(BaseModel):
    title=models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='Categories'

class Teacher(BaseModel):
    full_name=models.CharField(max_length=250)
    image=models.ImageField(upload_to='teachers/', blank=True, default='default_teacher.png')
    telegram_url=models.URLField(max_length=250, null=True, blank=True)
    instagram_url=models.URLField(max_length=250, null=True, blank=True)


class Course(BaseModel):
    name=models.CharField(max_length=250)
    description=models.TextField(blank=True, null=True)
    image=models.ImageField(upload_to='courses/', blank=True, default='default_course.jpg')
    price=models.FloatField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE, related_name='courses')
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)


class Video(BaseModel):
    name=models.CharField(max_length=250)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    duration=models.PositiveIntegerField(default=0)
    file=models.FileField(upload_to='videos/', default='default_video.jpeg')


    @property
    def video_duration(self):
        # hour=0
        # minute=self.duration
        hour=self.duration//60
        minute=self.duration % 60 
        return hour,minute


class Customer(BaseModel):
    phone_number=models.CharField(max_length=100)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='customers')
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero=0
        one=1
        two=2
        three=3
        four=4
        five=5
    title=models.TextField()
    message=models.TextField()
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    rating=models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)




