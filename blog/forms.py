from django import forms
from .models import BlogPost

class BlogPostCreateForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']