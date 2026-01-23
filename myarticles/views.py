from django.shortcuts import render, get_object_or_404
from .models import Products, Category, Promotions
from django.db.models import Q 

def display_main(request):
    """
    Renders the main homepage with 10 random products and active promotions.
    """
    random_products = Products.objects.all().order_by('?')[:10]
    promos = Products.objects.filter(is_promotion=True)
    
    return render(request, 'main/main.html', {
        'products': random_products,
        'promos': promos
    })

def display_categories(request):
    """
    Renders the page listing all available product categories.
    """
    categories = Category.objects.all()
    return render(request, 'Articles/Articles.html', {
        'categories': categories
    })

def display_information(request):
    """
    Renders the static information page.
    """
    return render(request, 'Information/Information.html')

def display_promotions(request):
    """
    Renders a page showing all products marked as promotions.
    """
    promos = Products.objects.filter(is_promotion=True)
    return render(request, 'Promotions/Promotions.html', {'promos': promos})

def promo_detail(request, promo_id):
    """
    Renders the details of a specific promotional product.
    """
    selected_promo = get_object_or_404(Products, pk=promo_id)
    return render(request, 'Promotions/promo_details.html', {'promo': selected_promo})

def products_by_category(request, category_id):
    """
    Filters and displays products belonging to a specific category, excluding promotions.
    """
    selected_category = get_object_or_404(Category, id=category_id)
    filtered_products = Products.objects.filter(category=selected_category, is_promotion=False)

    context = {
        'category': selected_category,
        'products': filtered_products 
    }
    
    return render(request, 'Articles/allproducts.html', context)

def product_details(request, product_id):
    """
    Renders the detailed view of a single product.
    """
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'Articles/product.html', {'product': product})

def search_products(request):
    """
    Searches for products by name or details based on a query string.
    """
    query = request.GET.get('q', '').strip()
    
    if query:
        results = Products.objects.filter(
            Q(name__icontains=query) | 
            Q(details__icontains=query)
        )
    else:
        results = []

    return render(request, 'Articles/allproducts.html', {
        'products': results, 
        'query': query
    })