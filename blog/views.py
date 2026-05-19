from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogCategory, BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(status='published').select_related('category', 'author')
    categories = BlogCategory.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog.html', context)


def blog_category(request, category_slug):
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = category.posts.filter(status='published').select_related('author')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog_category.html', context)


def blog_detail(request, post_slug):
    post = get_object_or_404(BlogPost, slug=post_slug, status='published')
    
    # Increment view count
    post.view_count += 1
    post.save()
    
    context = {
        'post': post,
    }
    return render(request, 'blog_detail.html', context)
