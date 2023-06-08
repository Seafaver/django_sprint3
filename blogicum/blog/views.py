from django.shortcuts import get_object_or_404, render

from django.http import Http404

from blog.models import Post
from blog.models import Category
from blog.models import Location
from django.db.models import Q
import datetime

dt = datetime.datetime.now()


def index(request):
    template = 'blog/index.html'
    post = Post.objects.select_related('category'
                                       ).filter(
        is_published=True, category__is_published=True
        ).exclude(pub_date__date__gt=datetime.datetime.now().date())[:5]
    context = {
        'post_list': post,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category').filter(
            is_published=True,
            category__is_published=True
        ).exclude(pub_date__date__gt=datetime.datetime.now().date()),
        id=post_id,
    )
    context = {
        'post_list': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.all(), slug=category_slug)
    post = Post.objects.select_related(
        'category'
        ).filter(
        is_published=True, category__is_published=True,
        category__slug=category_slug
    ).exclude(pub_date__date__gt=datetime.datetime.now().date())
    context = {
        'category': category,
        'post_list': post,
    }
    return render(request, template, context)
