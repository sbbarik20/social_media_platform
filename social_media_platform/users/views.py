from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from .models import Item
# from .forms import ItemForm



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
        mnub = request.POST.get('mnub')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already taken!')
            return redirect('signup')
        
        my_user = User.objects.create_user(username=email, password=pass1, email=email, first_name=fname, last_name=lname)
        my_user.save()

        messages.success(request, 'User created successfully!')
        return redirect('login')

    return render(request, 'signup.html')



@login_required(login_url='login')
def user_index(request):
    return render(request, 'index.html')

def user_profile(request):
    return render(request, 'profile.html')

def user_logout(request):
    logout(request)
    return redirect('login')



























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

# # def signin(request):
# #     items = Item.objects.all()
# #     return render(request, 'shopee/signin.html', {'items': items})



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