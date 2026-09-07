from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from services.models import Service, Category
from decimal import Decimal

def catalog(request):
    all_categories = Category.objects.all()
    categories = Category.objects.prefetch_related('services').all()
    category_ids = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_ids:
        categories = categories.filter(id__in=category_ids)

    for category in categories:
        passed = []
        for service in category.services.all():
            ok = True
            if min_price:
                try:
                    if service.price < float(min_price):
                        ok = False
                except ValueError:
                    pass
            if max_price:
                try:
                    if service.price > float(max_price):
                        ok = False
                except ValueError:
                    pass
            if ok:
                passed.append(service)
        category.filtered_services = passed

    sort = request.GET.get('sort', '')
    for category in categories:
        if sort == 'price_asc':
            category.filtered_services.sort(key=lambda service: service.price)
        elif sort == 'price_desc':
            category.filtered_services.sort(key=lambda service: service.price, reverse=True)
        elif sort == 'name_asc':
            category.filtered_services.sort(key=lambda service: service.name.lower())
        elif sort == 'name_desc':
            category.filtered_services.sort(key=lambda service: service.name.lower(), reverse=True)

    categories = [category for category in categories if category.filtered_services]
    selected_categories = [int(c) for c in request.GET.getlist('category') if c.isdigit()]

    search = request.GET.get('search_service', '').strip()
    if search:
        for category in categories:
            category.filtered_services = [s for s in category.filtered_services if search.lower() in s.name.lower()]
        categories = [category for category in categories if category.filtered_services]

    all_services = []
    for category in categories:
        all_services.extend(category.filtered_services)
    return render(request, 'services/catalog.html', {'all_categories': all_categories ,'categories': categories, 'selected_categories': selected_categories, 'services': all_services})

def service_detail(request, pk):
    try:
        service = Service.objects.get(pk=pk)
    except Service.DoesNotExist:
        return HttpResponseNotFound("Service does not exist")

    return render(request, 'services/service_detail.html', {'service': service})

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    service_id = str(pk)
    
    # Увеличиваем количество на 1
    cart[service_id] = cart.get(service_id, 0) + 1
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')

    for service_id, quantity in cart.items():
        try:
            service = Service.objects.get(pk=service_id)
            item_total = service.price * quantity
            total_price += item_total
            cart_items.append({
                'service': service,
                'quantity': quantity,
                'total_price': item_total,
            })
        except Service.DoesNotExist:
            continue

    return render(request, 'services/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def update_cart_quantity(request, pk, action):
    cart = request.session.get('cart', {})
    service_id = str(pk)

    if service_id in cart:
        if action == 'increase':
            cart[service_id] += 1
        elif action == 'decrease':
            cart[service_id] -= 1
            if cart[service_id] <= 0:
                del cart[service_id]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    service_id = str(pk)

    if service_id in cart:
        del cart[service_id]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')

@user_passes_test(lambda u: u.is_superuser)
def create_service(request):
    if request.method == 'POST':
        service = Service()
        service.name = request.POST.get('name')
        service.price = request.POST.get('price')
        category_id = request.POST.get('category')
        if category_id:
            try:
                service.category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                return HttpResponseNotFound("Category does not exist")
        service.description = request.POST.get('description')
        service.save()
        return redirect('catalog')
    categories = Category.objects.all()
    return render(request, 'services/create_service.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
def edit_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        if request.method == 'POST':
            service.name = request.POST.get('name')
            service.price = request.POST.get('price')
            service.description = request.POST.get('description')
            category_id = request.POST.get('category')
            if category_id:
                try:
                    service.category = Category.objects.get(pk=category_id)
                except Category.DoesNotExist:
                    return HttpResponseNotFound("Category does not exist")
            service.save()
            return redirect('catalog')
        else:
            categories = Category.objects.all()
            return render(request, 'services/edit_service.html', {'service': service, 'categories': categories})
    except Service.DoesNotExist:
        return HttpResponseNotFound("Service does not exist")

@user_passes_test(lambda u: u.is_superuser)
def delete_service(request, pk):
    try:
        service = Service.objects.get(pk=pk)
        service.delete()
        return redirect('catalog')
    except Service.DoesNotExist:
        return HttpResponseNotFound("Service does not exist")

@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == 'POST':
        category = Category()
        category.name = request.POST.get('name')
        category.save()
        return redirect('catalog')
    return render(request, 'services/create_category.html')

@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        if request.method == 'POST':
            category.name = request.POST.get('name')
            category.save()
            return redirect('catalog')
        else:
            return render(request, 'services/edit_category.html', {'category': category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category does not exist")

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('catalog')
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category does not exist")

