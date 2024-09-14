from django.db import models

# Create your models here.

from course.models import Category
from user.models import CustomUser

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Blog(BaseModel):
    title=models.CharField(max_length=200)
    body=models.TextField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='blogs')
    image=models.ImageField(upload_to='blogs/',default='default_blog.png')

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
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)




    