from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg, Count
from datetime import date
from .models import ThemeZone, Attraction, Guest, FastPass, TimeSlot

def home(request):
    """Home page with park overview statistics."""
    context = {
        'zone_count': ThemeZone.objects.filter(is_open=True).count(),
        'attraction_count': Attraction.objects.filter(is_operational=True).count(),
        'avg_wait': Attraction.objects.filter(
            attraction_type='ride',
            is_operational=True
        ).aggregate(Avg('current_wait_minutes'))['current_wait_minutes__avg'],
        'featured': Attraction.objects.filter(
            is_operational=True
        ).order_by('current_wait_minutes')[:3],
    }
    return render(request, 'fastpass/home.html', context)

def zone_list(request):
    """List all open theme zones."""
    zones = ThemeZone.objects.filter(is_open=True).annotate(
        num_attractions=Count('attractions')
    )
    return render(request, 'fastpass/zone_list.html', {'zones': zones})

def zone_detail(request, zone_id):
    """Show a single zone with its attractions."""
    zone = get_object_or_404(ThemeZone, id=zone_id)
    attractions = zone.attractions.filter(
        is_operational=True
    ).order_by('current_wait_minutes')
    context = {
        'zone': zone,
        'attractions': attractions,
    }
    return render(request, 'fastpass/zone_detail.html', context)

def attraction_list(request):
    """List all attractions with filtering."""
    attractions = Attraction.objects.filter(is_operational=True)
    zone_id = request.GET.get('zone')
    attraction_type = request.GET.get('type')
    if zone_id:
        attractions = attractions.filter(zone_id=zone_id)
    if attraction_type:
        attractions = attractions.filter(attraction_type=attraction_type)
    attractions = attractions.order_by('current_wait_minutes')
    context = {
        'attractions': attractions,
        'zones': ThemeZone.objects.filter(is_open=True),
    }
    return render(request, 'fastpass/attraction_list.html', context)

def attraction_detail(request, pk):
    """Show details for a single attraction."""
    attraction = get_object_or_404(Attraction, pk=pk)
    time_slots = attraction.time_slots.filter(is_active=True)
    context = {
        'attraction': attraction,
        'time_slots': time_slots,
    }
    return render(request, 'fastpass/attraction_detail.html', context)

def short_wait_rides(request):
    """Show rides with wait times under 30 minutes."""
    rides = Attraction.objects.filter(
        attraction_type='ride',
        is_operational=True,
        current_wait_minutes__lt=30
    ).order_by('current_wait_minutes')
    return render(request, 'fastpass/short_waits.html', {'rides': rides})

def guest_login(request):
    """Find or identify a guest by email."""
    if request.method == 'POST':
        from .forms import GuestLookupForm
        form = GuestLookupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                guest = Guest.objects.get(email=email)
                request.session['guest_id'] = guest.id
                messages.success(request, f"Welcome back, {guest.first_name}!")
                return redirect('fastpass:guest_dashboard', guest_id=guest.id)
            except Guest.DoesNotExist:
                messages.error(request, "No guest found with that email.")
    else:
        from .forms import GuestLookupForm
        form = GuestLookupForm()
    return render(request, 'fastpass/guest_login.html', {'form': form})

def guest_dashboard(request, guest_id):
    """Show guest's profile and today's FastPasses."""
    guest = get_object_or_404(Guest, id=guest_id)
    todays_passes = guest.fastpasses.filter(
        booking_date=date.today()
    ).order_by('time_slot__start_time')
    confirmed_count = todays_passes.filter(status='confirmed').count()
    remaining = guest.daily_fastpass_limit - confirmed_count
    context = {
        'guest': guest,
        'todays_passes': todays_passes,
        'remaining_passes': remaining,
    }
    return render(request, 'fastpass/guest_dashboard.html', context)

def book_fastpass(request, attraction_id):
    """Book a FastPass for an attraction."""
    attraction = get_object_or_404(Attraction, id=attraction_id)
    guest_id = request.session.get('guest_id')
    if not guest_id:
        messages.info(request, "Please enter your email to book a FastPass.")
        return redirect('fastpass:guest_login')
    guest = get_object_or_404(Guest, id=guest_id)
    if not attraction.fastpass_enabled:
        messages.error(request, "This attraction doesn't offer FastPass.")
        return redirect('fastpass:attraction_detail', pk=attraction.id)
    todays_count = FastPass.objects.filter(
        guest=guest,
        booking_date=date.today(),
        status='confirmed'
    ).count()
    if todays_count >= guest.daily_fastpass_limit:
        messages.error(request,
            f"You've reached your daily limit of {guest.daily_fastpass_limit} FastPasses.")
        return redirect('fastpass:guest_dashboard', guest_id=guest.id)
    already_booked = FastPass.objects.filter(
        guest=guest,
        attraction=attraction,
        booking_date=date.today()
    ).exists()
    if already_booked:
        messages.warning(request, "You already have a FastPass for this attraction today.")
        return redirect('fastpass:guest_dashboard', guest_id=guest.id)
    if request.method == 'POST':
        from .forms import FastPassBookingForm
        form = FastPassBookingForm(attraction, request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data['time_slot']
            FastPass.objects.create(
                guest=guest,
                attraction=attraction,
                time_slot=time_slot,
                booking_date=date.today(),
                status='confirmed'
            )
            messages.success(request,
                f"FastPass booked for {attraction.name} at "
                f"{time_slot.start_time.strftime('%I:%M %p')}!")
            return redirect('fastpass:guest_dashboard', guest_id=guest.id)
    else:
        from .forms import FastPassBookingForm
        form = FastPassBookingForm(attraction)
    context = {
        'form': form,
        'attraction': attraction,
        'guest': guest,
    }
    return render(request, 'fastpass/book_fastpass.html', context)
