from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductGroup, Article, ArticleGroup
from django.contrib.auth.decorators import login_required
from .models import CartItem
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import F

@login_required
def checkout_view(request):
    return render(request, 'shop_port1/checkout.html')



def index(request):
    categories = ProductGroup.objects.all()
    slideshow_products = Article.objects.filter(inventory__gt=0, available_for_sale=True)[:32]

    critical_articles = Article.objects.filter(inventory__gt=0, inventory__lte=F('minmum_inventory'))
    sold_out_articles = Article.objects.filter(inventory=0)

    return render(request, 'shop_port1/index.html', {
        'categories': categories,
        'slideshow_products': slideshow_products,
        'critical_articles': critical_articles,
        'sold_out_articles': sold_out_articles,
    })


def product_detail(request, pk):
    product = get_object_or_404(Article, pk=pk)
    return render(request, 'shop_port1/product_detail.html', {'product': product})



@login_required
def add_to_cart(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        article=article  # statt product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    return redirect('shop:cart')




@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price for item in cart_items)
    return render(request, 'shop_port1/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def remove_from_cart(request, article_id):
    item = get_object_or_404(CartItem, article_id=article_id, user=request.user)
    item.delete()

    total_price = sum(i.get_total_price() for i in CartItem.objects.filter(user=request.user))
    total_items = CartItem.objects.filter(user=request.user).count()

    return JsonResponse({
        'new_quantity': 0,
        'new_price': 0,
        'total_price': total_price,
        'total_items': total_items,
    })




@login_required
def get_cart_preview(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in cart_items)
    html = render_to_string('shop_port1/cart_preview.html', {
        'cart_items': cart_items
    }, request=request)
    return JsonResponse({'html': html, 'total_items': total_items})

def about(request):
    return render(request, 'shop_port1/about.html')

def contact(request):
    return render(request, 'shop_port1/contact.html')

def search(request):
    query = request.GET.get('query')
    results = Article.objects.filter(designation__icontains=query)
    return render(request, 'shop_port1/search_results.html', {
        'query': query,
        'results': results
    })


def impressum(request):
    return render(request, 'shop_port1/impressum.html')


def productgroup_detail(request, pk):
    group = get_object_or_404(ProductGroup, pk=pk)
    articles = Article.objects.filter(articlegroup__productgroup=group)

    return render(request, 'shop_port1/productgroup_detail.html', {
        'group': group,
        'articles': articles,
    })



def article_groups_list(request, pk):
    productgroup = get_object_or_404(ProductGroup, pk=pk)
    articlegroups = ArticleGroup.objects.filter(productgroup=productgroup)
    return render(request, 'shop_port1/article_groups_list.html', {
        'productgroup': productgroup,
        'articlegroups': articlegroups
    })


def articlegroup_detail(request, pk):
    group = get_object_or_404(ArticleGroup, pk=pk)
    articles = Article.objects.filter(articlegroup=group)
    return render(request, 'shop_port1/articlegroup_detail.html', {
        'group': group,
        'articles': articles
    })