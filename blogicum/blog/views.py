import datetime

from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post

dt = datetime.datetime.now()


def index(request):
    template = 'blog/index.html'
    post = Post.objects.select_related('category').filter(
        is_published=True, category__is_published=True
        ).exclude(pub_date__date__gt=dt.date()
                  )[:5]
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
        ).exclude(pub_date__date__gt=dt.date()),
        pk=post_id,
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.all(), slug=category_slug,
                                 is_published=True)
    post = Post.objects.select_related(
        'category').filter(
        is_published=True, pub_date__lte=dt.date(),
        category__is_published=True,
        category__slug=category_slug,
        )
    context = {
        'category': category,
        'post_list': post,
    }
    return render(request, template, context)
