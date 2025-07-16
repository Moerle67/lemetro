from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        # Summe aller Mengen statt nur Anzahl der Items
        total_items = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        total_items = 0  # Falls der Benutzer nicht eingeloggt ist

    return {'cart_item_count': total_items}
