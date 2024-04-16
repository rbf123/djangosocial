from django.shortcuts import render, redirect
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.



@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Your post has been created successfully!")
            return redirect('create')  # Redirect to the same view to clear the form
    else:
        form = PostCreateForm()  # Present an empty form
    return render(request, 'posts/create.html', {'form': form})

#def feed(request):
#    posts = Post.objects.all()
#    return render(request,'posts/feed.html',{'posts':posts})

@login_required
def feed(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Your comment has been posted successfully!")  # Add success message
            comment_form = CommentForm()  # Clear the form after saving
    else:
        comment_form = CommentForm()

    logged_user = request.user
    # Filter by user
    user_id = request.GET.get('user_id')
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    posts = Post.objects.all()

    # Most Recent Posts
    posts = posts.order_by('-created')

    # Posts by Date
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        posts = posts.filter(created__date__range=(start_date, end_date))

    # Posts by User
    if user_id:
        posts = posts.filter(user_id=user_id)

    # Get list of users who have made posts
    users = User.objects.filter(post__isnull=False).distinct()

    return render(request, 'posts/feed.html', {'posts': posts, 'users': users, 'logged_user': logged_user, 'comment_form': comment_form})

''' start feed test
@login_required
def feed(request):
    if request.method =='POST':
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post,id=post_id)
        new_comment.post = post
        new_comment.save()
    else:
        comment_form = CommentForm()
        
    logged_user = request.user
    # Filter by user
    user_id = request.GET.get('user_id')
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    posts = Post.objects.all()

    # Most Recent Posts
    posts = posts.order_by('-created') 

    # Posts by Date
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        posts = posts.filter(created__date__range=(start_date, end_date))

    # Posts by User
    if user_id:
        posts = posts.filter(user_id=user_id)
    
    # Get list of users who have made posts
    users = User.objects.filter(post__isnull=False).distinct()

    return render(request, 'posts/feed.html', {'posts': posts, 'users':users, 'logged_user':logged_user, 'comment_form':comment_form})

end of feed test
'''

def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('feed')

def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        liked = False
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
            liked = True
        like_count = post.liked_by.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

