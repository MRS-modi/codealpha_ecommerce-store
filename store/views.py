import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Order, OrderItem

def store(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    context = {'products': products, 'query': query}
    return render(request, 'store/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)

@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Get or create an active incomplete order for the user
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    
    # Get or create the order item for this product
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if not created:
        order_item.quantity += 1
        order_item.save()
        
    return redirect('cart')

def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('store')


@login_required(login_url='login')
def checkout(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitem_set.all()
    
    if not items:
        return redirect('cart')

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def process_order(request):
    if request.method == 'POST':
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        
        # Mark order as completed and create transaction ID
        transaction_id = str(datetime.datetime.now().timestamp())
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        return redirect('order_success')
    
    return redirect('checkout')

def order_success(request):
    return render(request, 'store/order_success.html')

@login_required(login_url='login')
def update_item_quantity(request, item_id, action):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    
    if action == 'add':
        order_item.quantity += 1
        order_item.save()
    elif action == 'remove':
        order_item.quantity -= 1
        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()
    elif action == 'delete':
        order_item.delete()
        
    return redirect('cart')