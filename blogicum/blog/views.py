import datetime

from django.shortcuts import get_object_or_404, render

from blog.models import Category, Post


def filtrations(post_object, is_publ1, is_publ2, count):
    if count > 0:
        #       Условием прохождения тестов "Убедитесь что на
        #       главной странице выводятся 5 постов"
        return (post_object.filter(
            is_published=is_publ1, category__is_published=is_publ2
            ).exclude(
            pub_date__date__gt=datetime.datetime.now().date())[:count])
    else:
        return (post_object.filter(
            is_published=is_publ1, category__is_published=is_publ2
            ).exclude(pub_date__date__gt=datetime.datetime.now().date()))


def index(request):
    return render(request, 'blog/index.html', {
        'post_list': filtrations(Post.objects.all(), True, True, 5),
        })


def post_detail(request, post_id):
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(
            filtrations(Post.objects.all(), True, True, 0), pk=post_id,),
    })


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.all(), slug=category_slug,
                                 is_published=True)
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': category.posts.select_related(
            'category').filter(
            is_published=True, category__is_published=True,).exclude(
            pub_date__gt=datetime.datetime.now().date())},)
