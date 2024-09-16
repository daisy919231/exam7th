
from django.urls import path
from course import views

urlpatterns=[
    path('home/', views.Home_Page.as_view(), name='home_page'),
    path('all_courses/', views.Course_View.as_view(), name='all_courses'),
    path('course_view/<int:category_id>/', views.Course_View.as_view(), name='course_view'),
    path('course_detail/<int:course_id>/', views.Detail_View.as_view(), name='detail'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('teachers/', views.Teachers.as_view(), name='teachers'),
    path('blogs/', views.Blogs.as_view(), name='blogs'),
    
]