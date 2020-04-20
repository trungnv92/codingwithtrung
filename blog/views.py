from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from .models import BlogPost

def create_post_view(request):
    user = request.user
    context = {}
    if not user.is_authenticated:
        return redirect('login')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        account = Account.objects.filter(email=user.email).first()
        obj.author = account
        obj.save()
        form = CreateBlogPostForm()
    context['form'] = form
    return render(request, 'blog/create_post.html', context)

def detail_post_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post
    return render(request, 'blog/detail_post.html', context)

def edit_post_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated'
            blog_post = obj

    form = UpdateBlogPostForm(
        initial= {
            'title': blog_post.title,
            'body': blog_post.body,
            'image': blog_post.image,
        }
    )
    context['form'] = form
    context['blog_post'] = blog_post
    return render(request, 'blog/edit_post.html', context)