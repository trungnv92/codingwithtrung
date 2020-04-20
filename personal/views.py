from django.shortcuts import render
from blog.models import BlogPost
from operator import attrgetter
from weather.views import get_list_data_weather
def index_view(request):
    return home_view(request)
def home_view(request):
    context = {}
    blog_posts = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
    context['blog_posts'] = blog_posts
    context['weather_data'] = get_list_data_weather
    return render(request, 'personal/home.html', context)