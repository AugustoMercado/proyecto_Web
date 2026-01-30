from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from cart.models import Cart
from myarticles.models import Products

User = get_user_model()

def display_login(request):
    """
    Handles user login.
    If authenticated, redirects to main.
    If POST, validates credentials and logs the user in.
    """
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main')
        return render(request, 'User/login/Loginaccount.html', {
            'form': form,
            'error': "Invalid username or password"
        })

    return render(request, 'User/login/Loginaccount.html', 
                  {'form': AuthenticationForm()})

def logout_account(request):
    """
    Logs out the user and redirects to the homepage.
    """
    logout(request) 
    return redirect('main') 

def show_history(request):
    """
    Displays the purchase history for the logged-in user.
    Shows only closed orders (active=False).
    """
    orders = Cart.objects.filter(user_id=request.user.id, active=False).order_by('-id').prefetch_related('cartbuy')
    return render(request, 'User/history.html', {'orders': orders})

def display_create_account(request):
    """
    Handles user registration.
    GET: Renders the registration form.
    POST: Validates input and creates a new User instance.
    """
    if request.method == 'GET':
        return render(request, 'User/create/Createaccount.html')
    
    return handle_user_registration(request)


def handle_user_registration(request):
    """
    Processes and validates user registration data.
    """
    first_name = request.POST.get('name')
    last_name = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    
    error = validate_registration_data(email, password, confirm_password)
    if error:
        return render(request, 'User/create/Createaccount.html', {'error': error})
    
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    login(request, user)
    return redirect('main')


def validate_registration_data(email, password, confirm_password):
    """
    Validates registration form data.
    Returns error message if validation fails, None otherwise.
    """
    if password != confirm_password:
        return 'Las contraseñas no coinciden'
    
    if User.objects.filter(username=email).exists():
        return 'El correo ya está registrado'
    
    return None

@staff_member_required(login_url='main')
def owner_dashboard(request):
    """
    Renders the business owner's dashboard.
    Displays total income from paid carts, sales count, recent orders, and low stock products.
    """
    closed_carts = Cart.objects.filter(active=False).order_by('-day_buy')
    paid_carts = closed_carts.filter(is_paid=True)
    low_stock_products = Products.objects.filter(stock__lte=10).order_by('stock')
    
    total_income = calculate_total_income(paid_carts)

    return render(request, 'User/owner_dashboard.html', {
        'total_income': total_income,
        'total_sales_count': paid_carts.count(),
        'recent_orders': closed_carts[:20],
        'low_stock': low_stock_products
    })


def calculate_total_income(paid_carts):
    """
    Calculates total income from paid carts.
    """
    return sum(cart.get_total() for cart in paid_carts)