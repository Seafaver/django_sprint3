import datetime

from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post


def filtrations(name_of_category, is_publ1, is_publ2, count):
    if count>0:
        return (Post.objects.select_related(name_of_category).filter(
            is_published=is_publ1, category__is_published=is_publ2
            ).exclude(pub_date__date__gt=datetime.datetime.now().date())[:count])
    else:
        return (Post.objects.select_related(name_of_category).filter(
            is_published=is_publ1, category__is_published=is_publ2
            ).exclude(pub_date__date__gt=datetime.datetime.now().date()))


def index(request):
    template = 'blog/index.html'
    posts = filtrations('category', True,  True, 5)
    context = {
        'post_list': posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    posts = get_object_or_404(
        filtrations('category', True,  True, 0),
        pk=post_id,
    )
    context = {
        'post': posts,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.all(), slug=category_slug,
                                 is_published=True)
    posts = category.posts.select_related(
        'category').filter(
        is_published=True,
        category__is_published=True,).exclude(
        pub_date__gt=datetime.datetime.now().date())
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, template, context)
