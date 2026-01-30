from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Products, Category, Promotions


def display_main(request):
    """
    Renders the main homepage with random products and active promotions.
    """
    random_products = Products.objects.filter(category__is_active=True).order_by('?')[:10]
    promos = Products.objects.filter(is_promotion=True)
    
    return render(request, 'main/main.html', {
        'products': random_products,
        'promos': promos
    })


def display_categories(request):
    """
    Renders the page listing all available product categories.
    """
    categories = Category.objects.filter(is_active=True).order_by('my_order')
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
    promo = get_object_or_404(Products, pk=promo_id)
    return render(request, 'Promotions/promo_details.html', {'promo': promo})


def products_by_category(request, category_id):
    """
    Displays products belonging to a specific category, excluding promotions.
    """
    category = get_object_or_404(Category, id=category_id)
    products = Products.objects.filter(category=category, is_promotion=False)

    return render(request, 'Articles/allproducts.html', {
        'category': category,
        'products': products
    })


def product_details(request, product_id):
    """
    Renders the detailed view of a single product.
    """
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'Articles/product.html', {'product': product})


def search_products(request):
    """
    Searches for products by name or details based on query parameter.
    """
    query = request.GET.get('q', '').strip()
    results = search_products_by_query(query)

    return render(request, 'Articles/allproducts.html', {
        'products': results,
        'query': query
    })


def search_products_by_query(query):
    """
    Filters products based on name or details match.
    Returns empty list if query is empty.
    """
    if not query:
        return []
    
    return Products.objects.filter(
        Q(name__icontains=query) |
        Q(details__icontains=query)
    )