import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import EmployeeProfile, User, Specialization
from .forms import UserRegisterForm, UserUpdateForm
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

def contacts(request):
    logger.info('Contacts page is loaded')
    employee_profiles = EmployeeProfile.objects.all()
    return render(request, 'users/contacts.html', {'employees': employee_profiles})

def contacts_api(request):
    logger.info('API contacts called')
    employees = EmployeeProfile.objects.all()
    data = []

    for emp in employees:
        data.append({
            'id': emp.id,
            'full_name': emp.user.get_full_name() or emp.user.username,
            'description': emp.description or 'No description',
            'phone': emp.user.phone_number or 'Not specified',
            'email': emp.user.email or 'Not specified',
            'website_url': emp.website_url or '',
            'photo': emp.photo.url if emp.photo else ''
        })

    return JsonResponse({'contacts': data})

def add_employee_api(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '')
            website_url = request.POST.get('website_url', '')
            description = request.POST.get('description', '')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            
            photo_file = request.FILES.get('photo') 

            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            username = f"emp_{User.objects.count() + 1}_{first_name.lower()}"
            
            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone,
                user_type='employee'
            )
            
            EmployeeProfile.objects.create(
                user=user,
                description=description,
                website_url=website_url,
                photo=photo_file  # Передаем сам файл
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

def contacts_table(request):
    logger.info('Contacts Table page is loaded')
    return render(request, 'users/contacts_table.html')

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