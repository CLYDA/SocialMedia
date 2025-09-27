from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger




@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                follow = False
            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True
            followers_count = user.followers.count()
            followings_count = user.following.count()
            return JsonResponse({'follow': follow, 'followers_count': followers_count, 'followings_count': followings_count})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
    return JsonResponse({'error': 'Invalid request'}) 



@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'users/user_detail.html', {'user': user})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'users/user_list.html', {'users': users})


# @login_required
# @require_POST
# def save_post(request):
#     post_id = request.POST.get('post_id')
#     if post_id is not None:
#         post = get_object_or_404(Post, pk=post_id)
#         user = request.user
#         if user in post.saved_by.all():
#             post.saved_by.remove(user)
#             saved = False
#         else:
#             post.saved_by.add(user)
#             saved = True
#         return JsonResponse({'saved': saved})
#     return JsonResponse({'error': 'Invalid post ID'})
 

@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = Post.objects.get(pk=post_id)
        user = request.user
        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False 
        else:
            post.saved_by.add(user)
            saved = True
        response_data = {
            'saved': saved,
        }
    else:
        response_data = {
            'error': 'Invalid post ID'
        }   
    return JsonResponse(response_data)


 
@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False 
        else:
            post.likes.add(user)
            liked = True
        post_likes_count = post.likes.count()
        response_data = {
            'liked': liked,
            'likes_count': post_likes_count,
        }
    else:
        response_data = {
            'error': 'Invalid post ID'
        }
    return JsonResponse(response_data)




@login_required
def post_detail(request,pk):
    post = get_object_or_404(Post , id = pk)
    post_tags_ids = post.tags.values_list('id', flat=True) #tuple
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-created')[:3]
    context = {
        'post':post,
        'similar_post': similar_post,
    }
    return render(request,"social/detail.html",context)      



@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('social:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})



    
def post_list(request,tag_slug=None):
    posts = Post.objects.select_related('author').order_by('-total_likes')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag]) 

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2 )   
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts =[]
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list_ajax.html', {'posts': posts})
    
    context={
        'posts': posts,
        'tag': tag,
    }
    return render(request,"social/list.html",context)



@login_required
def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['message']}"
            send_mail(
                cd['subject'],
                message,
                'arian.zafarei2016@gmail.com',
                ['arianzafari2019@gmail.com'],
                fail_silently=False,
            )
            sent = True
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'form': form, 'sent': sent})    



def log_out(request):
    logout(request)
    return HttpResponse("your exit from your page")

def profile(request):
    # user = request.user
    user = User.objects.prefetch_related('followers','following').get(id=request.user.id)
    saved_posts = user.saved_posts.all()
    return render(request, 'social/profile.html', {'saved_posts':saved_posts})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditFrom(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            # ذخیره فرم‌ها
            user_form.save()
            return redirect('social:profile')
        else:
            messages.error(request, "لطفاً خطاهای زیر را برطرف کنید.")
    else:
        user_form = UserEditFrom(instance=request.user)

    
    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/edit_account.html', context)




