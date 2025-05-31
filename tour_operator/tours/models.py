# tours/models.py
from django.db import models


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    passport_data = models.CharField(max_length=50)
    registration_date = models.DateField(auto_now_add=True)
    preferred_language = models.CharField(max_length=50, default='Russian')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration_days = models.IntegerField()
    max_participants = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)  # Adventure, Cultural, VIP etc.
    season = models.CharField(max_length=50)
    difficulty_level = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Partial', 'Partial'),
        ('Paid', 'Paid'),
    ]

    booking_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Unpaid')
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.client}"


class VisaType(models.Model):
    visa_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    processing_days = models.IntegerField()
    validity_months = models.IntegerField()
    entries_allowed = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Visa(models.Model):
    STATUS_CHOICES = [
        ('Application', 'Application'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Collected', 'Collected'),
    ]

    visa_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    application_date = models.DateField()
    approval_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visa {self.visa_id} for {self.client}"


class ChinaRegion(models.Model):
    region_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ChinaCity(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(ChinaRegion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(ChinaCity, on_delete=models.CASCADE)
    star_rating = models.IntegerField()
    contact_phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Excursion(models.Model):
    excursion_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_hours = models.IntegerField()
    guide_language = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ChineseGuide(models.Model):
    guide_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    languages = models.CharField(max_length=255)
    city = models.ForeignKey(ChinaCity, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Festival(models.Model):
    festival_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField()
    location = models.CharField(max_length=255)
    popularity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class TransportProvider(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    service_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=255)
    coverage_description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.provider_name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review {self.review_id} by {self.client}"


class TourAgency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    comission_percent = models.DecimalField(max_digits=5, decimal_places=2)
    contact_phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Card', 'Card'),
        ('Online Payment', 'Online Payment'),
        ('Cash', 'Cash'),
    ]

    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_deposit = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.payment_id} for booking {self.booking}"


class BookingsVisa(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    visa = models.ForeignKey(Visa, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('booking', 'visa'),)


class TourExcursion(models.Model):
    tour_excursion_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE)
    guide = models.ForeignKey(ChineseGuide, on_delete=models.CASCADE)
    schedule_datetime = models.DateTimeField()
    included_in_price = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tour.name} - {self.excursion.name}"


class TourFestival(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tour', 'festival'),)


class TourHotel(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]
    MEALS = [
        ('Breakfast', 'Breakfast'),
        ('Half Board', 'Half Board'),
        ('Full Board', 'Full Board'),
    ]

    tour_hotel_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    meals_included = models.CharField(max_length=50, choices=MEALS)

    def __str__(self):
        return f"{self.tour.name} - {self.hotel.name}"


class TourRegion(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    region = models.ForeignKey(ChinaRegion, on_delete=models.CASCADE)
    days_spent = models.IntegerField()

    class Meta:
        unique_together = (('tour', 'region'),)


class TourToAgency(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    agency = models.ForeignKey(TourAgency, on_delete=models.CASCADE)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = (('tour', 'agency'),)


class TourTransport(models.Model):
    DIRECTION_TYPES = [
        ('Departure', 'Departure'),
        ('Arrival', 'Arrival'),
        ('Intercity', 'Intercity'),
    ]

    tour_transport_id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    company = models.ForeignKey(TransportProvider, on_delete=models.CASCADE)
    direction_type = models.CharField(max_length=50, choices=DIRECTION_TYPES)
    departure_city = models.ForeignKey(ChinaCity, on_delete=models.CASCADE, related_name='departure_transports')
    arrival_city = models.ForeignKey(ChinaCity, on_delete=models.CASCADE, related_name='arrival_transports', null=True)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.direction_type} transport for {self.tour.name}"


class HotelOccupancy(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)
    season = models.CharField(max_length=50)
    bookings = models.IntegerField()
    avg_tour_difficulty = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False  # Это представление из SQL, не управляется Django
        db_table = 'HotelOccupancy'