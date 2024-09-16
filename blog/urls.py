from django.urls import path
from blog import views

urlpatterns=[
    path('blog_view/', views.blog_view, name='blog_view'),
]