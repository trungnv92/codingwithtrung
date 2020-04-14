from rest_framework import serializers

from blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField()
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image','username']
	def get_username(self, blog_post):
		return blog_post.author.username