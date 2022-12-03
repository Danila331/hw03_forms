
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

from posts.forms import PostForm
from .models import Post, Group

User = get_user_model()


def _get_page_obj(post_list, request):
    paginator = Paginator(post_list, settings.NUMBER_POST)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.select_related('group')
    page_obj = _get_page_obj(post_list=post_list,
                             request=request)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = _get_page_obj(post_list=post_list,
                             request=request)
    template = 'posts/profile.html'
    context = {'page_obj': page_obj, 'author': author}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_count = post.author.posts.count()
    template = 'posts/post_detail.html'
    context = {
        'post': post, 'posts_count': posts_count, 'requser': request.user}
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = _get_page_obj(post_list=post_list,
                             request=request)
    template = 'posts/group_list.html'
    context = {'group': group, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    template = 'posts/post_create.html'
    context = {'form': form, 'is_edit': True}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    edit_post = get_object_or_404(Post, id=post_id)
    if request.user != edit_post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=edit_post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    template = 'posts/post_create.html'
    context = {'form': form, 'is_edit': True}
    return render(request, template, context)
