from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
import json
from .models import Product, ProductSize, Category, Order, OrderItem
from django.db import models

# Create your views here.

def home(request):
    """Home page view with featured products"""
    featured_products = Product.objects.filter(featured=True, available=True)[:6]
    categories = Category.objects.all()
    
    # Get category images for display - separate by gender
    category_images = {}
    for category in categories:
        category_images[category.slug] = {}
        for gender in ['men', 'women']:
            images = []
            image_dir = f'static/images/{gender}/{category.slug}/'
            try:
                import os
                image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'))]
                for img_file in image_files[:4]:  # Limit to 4 images per gender per category
                    images.append(f'images/{gender}/{category.slug}/{img_file}')
            except (OSError, FileNotFoundError):
                continue
            category_images[category.slug][gender] = images
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'category_images': category_images,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """Product listing page with filtering and pagination"""
    products = Product.objects.filter(available=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    category_images = []
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
        # Get all images for this category (both men's and women's)
        for gender in ['men', 'women']:
            image_dir = f'static/images/{gender}/{category_slug}/'
            try:
                import os
                image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'))]
                for img_file in image_files:
                    category_images.append(f'images/{gender}/{category_slug}/{img_file}')
            except (OSError, FileNotFoundError):
                continue
    
    # Filter by gender
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_gender': gender,
        'category_images': category_images,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    sizes = product.sizes.all().order_by('size')
    context = {
        'product': product,
        'related_products': related_products,
        'sizes': sizes,
    }
    return render(request, 'store/product_detail.html', context)

def category_detail(request, slug):
    """Category detail page"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)

    # Filter by gender
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Get all images for this category (both men's and women's)
    category_images = []
    for gender_dir in ['men', 'women']:
        image_dir = f'static/images/{gender_dir}/{slug}/'
        try:
            import os
            image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'))]
            for img_file in image_files:
                category_images.append(f'images/{gender_dir}/{slug}/{img_file}')
        except (OSError, FileNotFoundError):
            continue

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'products': products,
        'category_images': category_images,
    }
    return render(request, 'store/category_detail.html', context)


def men_shoes(request):
    """Men's shoes page"""
    products = Product.objects.filter(gender='M', available=True)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'gender': 'Men',
    }
    return render(request, 'store/gender_products.html', context)


def women_shoes(request):
    """Women's shoes page"""
    products = Product.objects.filter(gender='W', available=True)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'gender': 'Women',
    }
    return render(request, 'store/gender_products.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    
    # Use ProductSize if size is selected
    size_obj = None
    if size:
        try:
            size_obj = ProductSize.objects.get(product=product, size=size)
        except ProductSize.DoesNotExist:
            size_obj = None
    
    cart = request.session.get('cart', {})
    key = f"{product_id}:{size}" if size else str(product_id)
    
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'product_id': product_id,
            'size': size,
            'quantity': quantity,
        }
    
    request.session['cart'] = cart
    request.session.modified = True  # Ensure session is saved
    
    messages.success(request, f'{product.name} has been added to your cart!')
    return redirect('store:cart')

def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:cart')
    
    cart_items = []
    subtotal = Decimal('0.00')
    
    for key, item in cart.items():
        product = get_object_or_404(Product, id=item['product_id'])
        size = item.get('size')
        price = product.price
        
        if size:
            try:
                size_obj = ProductSize.objects.get(product=product, size=size)
                price = size_obj.price
            except ProductSize.DoesNotExist:
                pass
        
        quantity = item['quantity']
        item_total = price * quantity
        subtotal += item_total
        
        cart_items.append({
            'product': product,
            'size': size,
            'quantity': quantity,
            'price': price,
            'subtotal': item_total,
        })
    
    # Calculate shipping and tax
    shipping_cost = Decimal('0.00')  # Free shipping
    tax_rate = Decimal('0.18')  # 18% GST
    tax = subtotal * tax_rate
    total = subtotal + shipping_cost + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'store/checkout.html', context)

def process_order(request):
    """Process the order and create dummy transaction"""
    if request.method != 'POST':
        return redirect('store:checkout')
    
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:cart')
    
    # Get form data
    customer_name = request.POST.get('customer_name')
    customer_email = request.POST.get('customer_email')
    customer_phone = request.POST.get('customer_phone')
    shipping_address = request.POST.get('shipping_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    postal_code = request.POST.get('postal_code')
    payment_method = request.POST.get('payment_method', 'Credit Card')
    
    # Validate required fields
    if not all([customer_name, customer_email, customer_phone, shipping_address, city, state, postal_code]):
        messages.error(request, 'Please fill in all required fields.')
        return redirect('store:checkout')
    
    # Calculate totals
    cart_items = []
    subtotal = Decimal('0.00')
    
    for key, item in cart.items():
        product = get_object_or_404(Product, id=item['product_id'])
        size = item.get('size')
        price = product.price
        
        if size:
            try:
                size_obj = ProductSize.objects.get(product=product, size=size)
                price = size_obj.price
            except ProductSize.DoesNotExist:
                pass
        
        quantity = item['quantity']
        item_total = price * quantity
        subtotal += item_total
        
        cart_items.append({
            'product': product,
            'size': size,
            'quantity': quantity,
            'price': price,
            'subtotal': item_total,
        })
    
    shipping_cost = Decimal('0.00')
    tax_rate = Decimal('0.18')
    tax = subtotal * tax_rate
    total = subtotal + shipping_cost + tax
    
    # Create order
    order = Order.objects.create(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        shipping_address=shipping_address,
        city=city,
        state=state,
        postal_code=postal_code,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax=tax,
        total=total,
        payment_method=payment_method,
        payment_status='completed',  # Dummy transaction
        status='processing'
    )
    
    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            size=item['size'],
            quantity=item['quantity'],
            price=item['price']
        )
    
    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True
    
    messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
    return redirect('store:order_success', order_number=order.order_number)

def order_success(request, order_number):
    """Order success page"""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})

def order_detail(request, order_number):
    """Order detail page"""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_detail.html', {'order': order})

def test_form(request):
    """Simple test view for debugging cart form"""
    return render(request, 'test_form.html')

def test_cart(request):
    """Test cart functionality"""
    return render(request, 'test_cart.html')

def cart(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    total = 0
    for key, item in cart.items():
        product = get_object_or_404(Product, id=item['product_id'])
        size = item.get('size')
        size_obj = None
        price = product.price
        if size:
            try:
                size_obj = ProductSize.objects.get(product=product, size=size)
                price = size_obj.price
            except ProductSize.DoesNotExist:
                pass
        subtotal = price * item['quantity']
        total += subtotal
        cart_items.append({
            'product': product,
            'size': size,
            'quantity': item['quantity'],
            'price': price,
            'subtotal': subtotal,
        })
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)

def remove_from_cart(request, product_id, size=None):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    key = f"{product_id}:{size}" if size else str(product_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('store:cart')

def search_products(request):
    """Search products by name, description, or category"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if query:
        # Search in product name, description, and category
        products = products.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        )
    
    # Filter by gender
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'query': query,
        'current_gender': gender,
    }
    return render(request, 'store/search_results.html', context)

def profile(request):
    """User profile page"""
    # Get user data from session or use defaults
    user_data = request.session.get('user_data', {
        'user_name': 'Guest User',
        'email': 'guest@example.com',
        'bio': 'Shoe enthusiast and fashion lover. Always looking for the perfect pair!',
        'phone': '+1 (555) 123-4567',
        'address': '123 Main Street, City, State 12345',
        'join_date': 'January 2024',
        'total_orders': 0,
    })
    
    # Get actual orders from database (for demo, we'll get all orders)
    # In a real app, you'd filter by user ID
    orders = Order.objects.all().order_by('-created_at')[:10]  # Get last 10 orders
    
    context = {
        'user_name': user_data['user_name'],
        'email': user_data['email'],
        'user_data': user_data,
        'orders': orders,
    }
    return render(request, 'store/profile.html', context)

def profile_settings(request):
    """Profile settings page"""
    # Get current user data from session
    user_data = request.session.get('user_data', {
        'user_name': 'Guest User',
        'email': 'guest@example.com',
        'phone': '+1 (555) 123-4567',
        'address': '123 Main Street, City, State 12345',
    })
    
    if request.method == 'POST':
        # Update user data from form
        user_data.update({
            'user_name': request.POST.get('user_name', 'Guest User'),
            'email': request.POST.get('email', 'guest@example.com'),
            'phone': request.POST.get('phone', ''),
            'address': request.POST.get('address', ''),
        })
        
        # Save to session
        request.session['user_data'] = user_data
        request.session.modified = True
        
        messages.success(request, 'Profile settings updated successfully!')
        return redirect('store:profile')
    
    context = {
        'user_name': user_data['user_name'],
        'email': user_data['email'],
        'phone': user_data['phone'],
        'address': user_data['address'],
    }
    return render(request, 'store/profile_settings.html', context)

def profile_edit(request):
    """Edit profile page"""
    # Get current user data from session
    user_data = request.session.get('user_data', {
        'user_name': 'Guest User',
        'email': 'guest@example.com',
        'bio': 'Shoe enthusiast and fashion lover. Always looking for the perfect pair!',
        'join_date': 'January 2024',
        'total_orders': 0,
    })
    
    if request.method == 'POST':
        # Update user data from form
        user_data.update({
            'user_name': request.POST.get('user_name', 'Guest User'),
            'email': request.POST.get('email', 'guest@example.com'),
            'bio': request.POST.get('bio', ''),
        })
        
        # Save to session
        request.session['user_data'] = user_data
        request.session.modified = True
        
        messages.success(request, 'Profile information updated successfully!')
        return redirect('store:profile')
    
    context = {
        'user_name': user_data['user_name'],
        'email': user_data['email'],
        'bio': user_data['bio'],
        'join_date': user_data['join_date'],
        'total_orders': user_data['total_orders'],
    }
    return render(request, 'store/profile_edit.html', context)

def size_guide(request):
    """Size guide page"""
    context = {
        'page_title': 'Size Guide',
    }
    return render(request, 'store/size_guide.html', context)

def shipping_info(request):
    """Shipping information page"""
    context = {
        'page_title': 'Shipping Information',
    }
    return render(request, 'store/shipping_info.html', context)

def contact_support(request):
    """Contact support page"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # In a real application, you would send an email here
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('store:contact_support')
    
    context = {
        'page_title': 'Contact Support',
    }
    return render(request, 'store/contact_support.html', context)

def track_order(request):
    """Track order page"""
    order_number = request.GET.get('order_number', '')
    order = None
    
    if order_number:
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Please check your order number.')
    
    context = {
        'page_title': 'Track Order',
        'order': order,
        'order_number': order_number,
    }
    return render(request, 'store/track_order.html', context)
