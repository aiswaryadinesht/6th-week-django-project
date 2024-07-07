from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, LoginForm,AdminLoginForm,CustomUserChangeForm,CustomUserPasswordChangeForm

# Signup view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_view(request):
    # Don't redirect from home to signup page if it is authenticated 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Login view

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    # Don't redirect from home to login page if it is authenticated 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Home page view
@login_required(login_url="login")
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html')


# Class-based view for home page
@method_decorator(never_cache, name='dispatch')
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

# Logout view
def user_logout(request):
    logout(request)
    request.session.flush()  # Ensure session data is completely cleared
    return redirect('login')


#Custom Admin  Panel 
#################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login_view(request):
    # Don't redirect from home to signup page if it is authenticated 
    if request.user.is_authenticated:
        return redirect('admin_panel')
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_panel')
            else:
                return render(request, 'admin_login.html', {'form': form, 'error': 'Invalid credentials or not an admin'})
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


@login_required(login_url="admin_login")
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_staff)
def admin_panel_view(request):
  if request.user.is_authenticated:
    #return redirect('admin_panel')
    users = CustomUser.objects.all()
    return render(request, 'admin_panel.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def user_search_view(request):
    query = request.GET.get('query', '')
    users = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'admin_panel.html', {'users': users, 'query': query})

@user_passes_test(lambda u: u.is_staff)
def user_detail_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_detail.html', {'user': user})

@user_passes_test(lambda u: u.is_staff)
def user_edit_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form,'user_id': user_id})

@user_passes_test(lambda u: u.is_staff)
def user_password_change_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = CustomUserPasswordChangeForm(user)
    return render(request, 'change_password.html', {'form': form, 'user_id': user_id})

@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = SignUpForm()
    return render(request, 'create_user.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def user_delete_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return render(request, 'delete_user.html', {'username': user.username})

def admin_logout(request):
    logout(request)
    request.session.flush()  # Ensure session data is completely cleared
    return redirect('admin_login')