from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Post, Group
from django.core.paginator import Paginator
from posts.forms import PostForm

User = get_user_model()

def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10) 

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    post_list = user_obj.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user_obj': user_obj,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts_group.all()[:10]
    context = {'group': group,
               'posts': posts, }
    return render(request, 'posts/group_list.html', context)

@login_required
def post_create(request):
    form = PostForm(data=request.POST)

    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/post_create.html', {'form': form})

    if not form.is_valid():
        return render(request, 'posts/post_create.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


def post_edit(request, post_id):
    is_edit = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=is_edit)

    if is_edit.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method != 'POST' or not form.is_valid():
        form = PostForm(instance=is_edit)
        return render(
            request,
            'posts/post_create.html',
            {
                'form': form,
                'post_id': post_id,
                'is_edit': is_edit
            }
        )

    form.save()
    return redirect('posts:post_detail', post_id)