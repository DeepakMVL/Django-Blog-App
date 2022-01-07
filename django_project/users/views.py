from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .form import UserRegisterForm, UserUpdateForm, UserProfileForm
from django.contrib.auth.decorators import login_required #to restrict the access of profile page to public

# Create your views here.
def register(request):
    if request.method == "POST": #to check if the method is POST ie after submitting
        #form=UserCreationForm(request.POST)
        form=UserRegisterForm(request.POST)
        if form.is_valid(): #checks if form is valid
            form.save() #to save the user details
            username=form.cleaned_data.get('username') #assigning username to username field
            messages.success(request, "Account created for {}!".format(username) )
            return redirect('blog-home')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid(): #checks if form is valid
            u_form.save()
            p_form.save()
            messages.success(request, "Account has been updated" )
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)
    context = {
    'u_form':u_form,
    'p_form':p_form
    }
    return render(request,'users/profile.html',context)
