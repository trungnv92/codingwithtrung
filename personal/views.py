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
    print(blog_posts)
    context['weather_data'] = get_list_data_weather
    return render(request, 'personal/home.html', context)


def rss_view(request):
    context = {}
    blog_posts = []
    import feedparser
    from newsplease import NewsPlease

    # Get a list of feed URLs
    with open('feeds.txt') as f:
        rss_urls = list(f)
    for url in rss_urls:
        NewsFeed = feedparser.parse(url)
        for entry in NewsFeed.entries:
            blog = {}
            blog['title'] = entry.title
            blog['link'] = entry.link
            # get content
            article = NewsPlease.from_url(entry.link) 
            blog['content'] = article.maintext
            blog['image'] = article.image_url
            blog['date_published'] = article.date_publish
            blog['author'] = ''
            blog['description'] = article.description
            #print("date_publish: ", article.date_publish)

            blog_posts.append(blog)

    
    context['blog_posts'] = blog_posts
    return render(request, 'personal/rss.html', context)