from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'cafeteria/landing.html')

@login_required
def secret_menu(request):
    food_items = [
        {'name': 'Roasted Gorax Ribs', 'description': 'Tender ribs slow-roasted over an open fire.', 'emoji': '🍖'},
        {'name': 'Endorian Sunberries', 'description': 'Sweet and tangy berries harvested from the forest canopy.', 'emoji': '🫐'},
        {'name': 'Tip-Yip Skewers', 'description': 'Grilled Tip-Yip on skewers with forest herbs.', 'emoji': '🍢'},
    ]
    return render(request, 'cafeteria/secret_menu.html', {'food_items': food_items})
