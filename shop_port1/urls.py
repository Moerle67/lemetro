from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('impressum/', views.impressum, name='impressum'),
    path('search/', views.search, name='search'),
    


    # Warenkorb
    path('cart/', views.cart, name='cart'),
    path('cart/preview/', views.get_cart_preview, name='get_cart_preview'),
    path('cart/add/<int:article_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:article_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),

    # Struktur: Warengruppe > Artikelgruppe > Artikel
    path('articlegroup/<int:pk>/', views.articlegroup_detail, name='articlegroup_detail'),
    path('productgroup/<int:pk>/', views.article_groups_list, name='article_groups_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
