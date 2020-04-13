from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogPostCreateForm
from account.models import Account
from .models import BlogPost

def create_blog_view(request):
    user = request.user
    context = {}
    if not user.is_authenticated:
        return redirect('login')
    
    form = BlogPostCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        account = Account.objects.filter(email=user.email).first()
        obj.author = account
        obj.save()
        form = BlogPostCreateForm()
    context['create_post_form'] = form
    return render(request, 'blog/create_post.html', context)

def detail_blog_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post
    return render(request, 'blog/detail_blog.html', context)

