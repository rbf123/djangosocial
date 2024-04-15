from django.shortcuts import render
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.



@login_required
def post_create(request):
    if request.method=='POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
    else:
        form = PostCreateForm(data=request.GET)
    return render(request,'posts/create.html',{'form': form})

#def feed(request):
#    posts = Post.objects.all()
#    return render(request,'posts/feed.html',{'posts':posts})

@login_required
def feed(request):
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

    return render(request, 'posts/feed.html', {'posts': posts, 'users':users})

