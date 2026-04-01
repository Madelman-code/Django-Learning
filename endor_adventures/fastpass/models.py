from django.db import models

class ThemeZone(models.Model):
    """
    Represents a themed area of Endor Adventures park.
    Examples: Forest of Endor, Ewok Village, Imperial Ruins
    """
    # Basic information about the zone
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Is this zone currently open to guests?
    is_open = models.BooleanField(default=True)
    # When was this record created?
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


class Attraction(models.Model):
    """
    Represents a ride, show, or experience in the park.
    Each attraction belongs to one ThemeZone.
    """
    # Attraction types (we'll use these as choices)
    RIDE = 'ride'
    SHOW = 'show'
    EXPERIENCE = 'experience'
    DINING = 'dining'
    TYPE_CHOICES = [
        (RIDE, 'Ride'),
        (SHOW, 'Show'),
        (EXPERIENCE, 'Experience'),
        (DINING, 'Dining'),
    ]
    # Thrill levels for rides
    THRILL_CHOICES = [
        (1, 'Mild - All Ages'),
        (2, 'Moderate - Some Thrills'),
        (3, 'Thrilling - Not for the Faint of Heart'),
        (4, 'Extreme - Hold onto Your Ewok!'),
    ]
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField()
    attraction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=RIDE
    )
    # THIS IS THE FOREIGN KEY - connects Attraction to ThemeZone
    zone = models.ForeignKey(
        ThemeZone,
        on_delete=models.CASCADE,
        related_name='attractions'
    )
    # Ride specifications
    thrill_level = models.IntegerField(choices=THRILL_CHOICES, default=1)
    min_height_cm = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=5)
    # Current status
    current_wait_minutes = models.IntegerField(default=0)
    is_operational = models.BooleanField(default=True)
    fastpass_enabled = models.BooleanField(default=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['zone', 'name']
    def __str__(self):
        return f"{self.name} ({self.zone.name})"


class TimeSlot(models.Model):
    """
    Represents an available time window for FastPass bookings.
    Each time slot belongs to one attraction.
    """
    # Which attraction is this time slot for?
    attraction = models.ForeignKey(
        Attraction,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    # Time window
    start_time = models.TimeField()
    end_time = models.TimeField()
    # How many FastPasses can be booked for this slot?
    max_fastpasses = models.IntegerField(default=50)
    # Is this slot available for booking?
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['attraction', 'start_time']
        unique_together = ['attraction', 'start_time']
    def __str__(self):
        return f"{self.attraction.name}: {self.start_time.strftime('%I:%M %p')}"


class Guest(models.Model):
    """
    Represents a park visitor who can book FastPasses.
    """
    # Membership tiers
    STANDARD = 'standard'
    SILVER = 'silver'
    GOLD = 'gold'
    PLATINUM = 'platinum'
    MEMBERSHIP_CHOICES = [
        (STANDARD, 'Standard - Day Pass'),
        (SILVER, 'Silver - Season Pass'),
        (GOLD, 'Gold - Premium Season Pass'),
        (PLATINUM, 'Platinum - VIP All-Access'),
    ]
    # Guest information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Membership details
    membership_tier = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        default=STANDARD
    )
    # How many FastPasses can this guest book per day?
    daily_fastpass_limit = models.IntegerField(default=3)
    # Guest's height (for ride requirements)
    height_cm = models.IntegerField(null=True, blank=True)
    # When did they register?
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['last_name', 'first_name']
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class FastPass(models.Model):
    """
    Represents a FastPass reservation.
    Links a Guest to an Attraction at a specific TimeSlot.
    """
    # Status options
    CONFIRMED = 'confirmed'
    USED = 'used'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (USED, 'Used'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
    ]
    # The THREE foreign keys connecting everything together
    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name='fastpasses'
    )
    attraction = models.ForeignKey(
        Attraction,
        on_delete=models.CASCADE,
        related_name='fastpasses'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='fastpasses'
    )
    # Booking information
    booking_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=CONFIRMED
    )
    # When was this booked?
    booked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-booking_date', 'time_slot__start_time']
        verbose_name_plural = "FastPasses"
        unique_together = ['guest', 'attraction', 'booking_date']
    def __str__(self):
        return f"{self.guest.full_name} - {self.attraction.name}"
