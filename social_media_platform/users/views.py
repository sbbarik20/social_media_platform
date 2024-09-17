from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend, AuthAlreadyAssociated
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=email, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')



def user_signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        mnub = request.POST.get('mnub')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')

        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('signup')
        
        my_user = User.objects.create_user(username=uname, password=pass1, email=email, first_name=fname, last_name=lname)
        my_user.save()

        messages.success(request, 'User created successfully!')
        return redirect('login')

    return render(request, 'signup.html')




@login_required(login_url='login')
def user_index(request):
    return render(request, 'index.html')


def user_forgot_password(request):
    return render(request, 'forgot_password.html')

def user_profile(request):
    return render(request, 'profile.html')


@login_required
def associate_social(request, backend):
    try:
        strategy = load_strategy(request)
        backend = load_backend(strategy=strategy, name=backend, redirect_uri=None)
        backend.auth_complete(user=request.user)
    except MissingBackend:
        messages.error(request, 'An error occurred while associating your account.')
    except AuthAlreadyAssociated:
        messages.error(request, 'This social account is already associated with another user.')
    return redirect('index')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def user__msg(request):
    return render(request, 'msg.html')


def user__notification(request):
    return render(request, 'notification.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        try:
            post = Post.objects.create(creater=request.user, content_text=text, content_image=pic)
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")



@login_required
@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        try:
            post.content_text = text
            if img_chg != 'false':
                post.content_image = pic
            post.save()
            
            if(post.content_text):
                post_text = post.content_text
            else:
                post_text = False
            if(post.content_image):
                post_image = post.img_url()
            else:
                post_image = False
            
            return JsonResponse({
                "success": True,
                "text": post_text,
                "picture": post_image
            })
        except Exception as e:
            print('-----------------------------------------------')
            print(e)
            print('-----------------------------------------------')
            return JsonResponse({
                "success": False
            })
    else:
            return HttpResponse("Method must be 'POST'")



@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))



@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))



@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        xempt
def comment(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Post.objects.get(id=post_id)
            try:
                newcomment = Comment.objects.create(post=post,commenter=request.user,comment_content=comment)
                post.comment_count += 1
                post.save()
                print(newcomment.serialize())
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)
    
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def delete_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.creater:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))





















             # copy from Barber

# def item_list(request):
#     items = Item.objects.all()
#     return render(request, 'shopee/item_list.html', {'items': items})

# def item_detail(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     return render(request, 'shopee/item_detail.html', {'item': item})

# def item_create(request):
#     if request.method == "POST":
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('item_list')
#     else:
#         form = ItemForm()
#     return render(request, 'shopee/item_form.html', {'form': form})

# def item_update(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     if request.method == "POST":
#         form = ItemForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('item_list')
#     else:
#         form = ItemForm(instance=item)
#     return render(request, 'shopee/item_form.html', {'form': form})

# def item_delete(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     if request.method == "POST":
#         item.delete()
#         return redirect('item_list')
#     return render(request, 'shopee/item_confirm_delete.html', {'item': item})

#  def signin(request):
#      items = Item.objects.all()
#      return render(request, 'shopee/signin.html', {'items': items})



# def signin(request):
#     items = Item.objects.all()
    
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         # Authenticate the user
#         user = authenticate(request, username=shakti, password=123)
        
#         if user is not None:
#             login(request, user)
#             return redirect('shopee/saloon.html')  # Redirect to the home page or any other page
#         else:
#             messages.error(request, 'Invalid username or password.')
#             # return render(request, 'shopee/signin.html', {'items': items})
    
#     return render(request, 'shopee/signin.html', {'items': items})