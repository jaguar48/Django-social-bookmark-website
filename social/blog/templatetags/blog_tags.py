from django import template
from ..models import Post
from django.db.models import Count, Max
from django.utils.safestring import mark_safe
import markdown
import random

register = template.Library()
@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=0):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=4):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

""" @register.simple_tag
def get_random():
    return Post.objects.all().order_by("?").first() """

""" @register.simple_tag
def get_random():
    max_id = Post.objects.all().aggregate(max_id =Max("id"))['max_id']
    pk = random.randint(3,max_id)
    poster = Post.objects.get(pk=pk) """
""" def post_random():
    max_id = Post.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1,max_id)
        poster = Post.objects.filter(pk=pk).first()
        if poster:
            return poster """