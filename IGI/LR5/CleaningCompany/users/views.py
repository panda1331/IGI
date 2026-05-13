import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import EmployeeProfile, User, Specialization
from .forms import UserRegisterForm, UserUpdateForm

logger = logging.getLogger(__name__)

def contacts(request):
    logger.info('Contacts page is loaded')
    employee_profiles = EmployeeProfile.objects.all()
    return render(request, 'users/contacts.html', {'employees': employee_profiles})

@login_required
def profile(request):
    logger.info('Profile page is loaded')
    user = request.user
    return render(request, 'users/profile.html', {'user': user})

def register(request):
    logger.info('Register page is loaded')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def update_profile(request):
    logger.info('Update profile page is loaded')
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/profile_edit.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def show_users(request):
    logger.info('Manage page is loaded')
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'users/manage.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, pk):
    logger.info('Edit user page is loaded')
    try:
        user = User.objects.get(pk=pk)
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                if user.user_type=='employee':
                    profile = user.employee_profile
                    profile.hire_date = request.POST.get('hire_date')
                    profile.description = request.POST.get('description')
                    profile.save()
                    spec_ids = request.POST.getlist('specializations')
                    profile.specializations.set(spec_ids)
                elif user.user_type=='client':
                    user.client_type = request.POST.get('client_type')
                    user.company_name = request.POST.get('company_name')
                    user.save()
                return redirect('manage_users')
        else:
            form = UserUpdateForm(instance=user)
        specializations = Specialization.objects.all()
        return render(request, 'users/edit_user.html', {'form': form, 'specializations': specializations, 'user': user})
    except User.DoesNotExist:
        logger.error('User does not exist')
        return HttpResponseNotFound('User not found')

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    logger.info('Deleting user')
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return redirect('manage_users')
    except User.DoesNotExist:
        logger.error('User does not exist')
        return HttpResponseNotFound('User not found')

@user_passes_test(lambda u: u.is_superuser)
def create_employee(request):
    logger.info('Create employee page is loaded')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        birth_date = request.POST.get('date_of_birth') or None
        hire_date = request.POST.get('hire_date') or None
        description = request.POST.get('description')
        specialization_ids = request.POST.getlist('specializations')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type='employee',
            middle_name=middle_name,
            phone_number=phone,
            date_of_birth=birth_date,
        )
        profile = EmployeeProfile.objects.create(
            user=user,
            hire_date=hire_date,
            description=description,
        )
        profile.specializations.set(specialization_ids)
        return redirect('manage_users')

    specializations = Specialization.objects.all()
    return render(request, 'users/create_employee.html', {'specializations': specializations})

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('profile')
#         else:
#             return render(request, 'users/login.html', {'error': 'Invalid username and/or password.'})
#     return render(request, 'users/login.html')
#
# @login_required
# def logout(request):
#     auth.logout(request)
#     return redirect('index')