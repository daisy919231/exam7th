from django.shortcuts import render
from django.views import View
from typing import Optional
from django.db.models import Count, Avg, Sum, Max, Min

# Create your views here.
from course.models import Course, Category, Comment, Video, Teacher
from blog.models import Blog

class Home_Page(View):
    def get(self,request, *args, **kwargs):
        categories=Category.objects.all()
        context={
            'categories': categories
        }
        return render (request, 'course/index.html', context)



from django.shortcuts import get_object_or_404

class Course_View(View):
    def get(self, request, category_id: Optional[int] = None, course_id: Optional[int] = None, **kwargs):
        categories = Category.objects.all()
        videos = Video.objects.all()
        
        # Calculate average rating for all videos (or adjust as needed)
        average_rating = videos.aggregate(
            avg_rating=Avg('video_comments__rating'),
            rating_count=Count('video_comments')
        )

        # Initialize average and count
        average = 0
        count = 0
        
        # Only attempt to get the course if course_id is provided
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            rating_info = course.average_rating()
            average = rating_info['avg_rating'] or 0
            count = rating_info['rating_count'] or 0
        
        # Filter courses based on category_id
        if category_id:
            courses = Course.objects.filter(category__id=category_id)
        else:
            courses = Course.objects.all()

        context = {
            'categories': categories,
            'courses': courses,
            'category_id': category_id,
            'average': average,
            'count': count
        }
        
        return render(request, 'course/course.html', context)

    

class Detail_View(View):
    def get(self, request, course_id:Optional[int]=None,category_id:Optional[int]=None, **kwargs):
        course=Course.objects.get(id=course_id)
        categories=Category.objects.all()

        video_quantity=course.videos.all().count()

        avg_video_ratings=Comment.objects.filter(video__course_id=course_id).values('video_id').annotate(avg_rating=Avg('rating')).values('avg_rating')
        average_course_rating=avg_video_ratings.aggregate(overall_avg=Avg('avg_rating'))['overall_avg']

        avg_course_student=Comment.objects.filter(video__course_id=course_id).values('customer_id').count()
        avg_course_duration=Video.objects.filter(course_id=course_id).aggregate(overall_duration=Sum('duration'))['overall_duration'] or 0
        

        avg_course_hour=avg_course_duration // 60
        avg_course_minute=avg_course_duration % 60

        if category_id:
            courses=Course.objects.filter(category__id=category_id)
        else:
            courses=Course.objects.all()
        



        context={
            'course':course,
            'video_quantity':video_quantity,
            'average_course_rating':average_course_rating,
            'avg_course_student':avg_course_student,
            'avg_course_hour':avg_course_hour,
            'avg_course_minute':avg_course_minute,
            'categories':categories,
            'courses':courses,
        }
        return render(request, 'course/detail.html', context)
    
class AboutPage(View):
    def get(self, request, *args, **kwargs ):
        comments=Comment.objects.all()
        context={
            'comments':comments
        }
        return render(request, 'course/about.html',context)

class Teachers(View):
    def get(self, request,*args, **kwargs):
        teachers=Teacher.objects.all()
        context={
            'teachers':teachers
        }
        return render(request, 'course/teacher.html', context)

class Blogs(View):
    def get(self, request,*args, **kwargs):
        blogs=Blog.objects.all()
        context={
            'blogs':blogs
        }
        return render(request, 'course/blog.html', context)

class BlogDetail(View):
    def get(self, request, blog_id:Optional[int]=None, *args, **kwargs):
        blog=Blog.objects.all(id=blog_id)
        context={
            'blog':blog
        }
        return render(request, 'course/blog.html', context)