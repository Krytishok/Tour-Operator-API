# tours/serializers.py
from rest_framework import serializers
from .models import (
    Client,
    Employee,
    Tour,
    Booking,
    VisaType,
    Visa,
    ChinaRegion,
    ChinaCity,
    Hotel,
    Excursion,
    ChineseGuide,
    Festival,
    TransportProvider,
    Insurance,
    Review,
    TourAgency,
    Payment,
    BookingsVisa,
    TourExcursion,
    TourFestival,
    TourHotel,
    TourRegion,
    TourToAgency,
    TourTransport,
    HotelOccupancy,
)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class VisaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaType
        fields = '__all__'


class VisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visa
        fields = '__all__'


class ChinaRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChinaRegion
        fields = '__all__'


class ChinaCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChinaCity
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = '__all__'


class ChineseGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChineseGuide
        fields = '__all__'


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = '__all__'


class TransportProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportProvider
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TourAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourAgency
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class BookingsVisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingsVisa
        fields = '__all__'


class TourExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourExcursion
        fields = '__all__'


class TourFestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourFestival
        fields = '__all__'


class TourHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourHotel
        fields = '__all__'


class TourRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourRegion
        fields = '__all__'


class TourToAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourToAgency
        fields = '__all__'


class TourTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourTransport
        fields = '__all__'


class HotelOccupancySerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField()
    hotel_name = serializers.CharField()
    month = serializers.CharField()
    season = serializers.CharField()
    bookings = serializers.IntegerField()
    avg_tour_difficulty = serializers.DecimalField(max_digits=5, decimal_places=2)

class ClientPavelSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()


class TourExcursionStatsSerializer(serializers.ModelSerializer):
    total_excursions = serializers.IntegerField()
    paid_excursions = serializers.IntegerField()
    paid_percent = serializers.FloatField()

    class Meta:
        model = Tour
        fields = [
            'tour_id',
            'name',
            'total_excursions',
            'paid_excursions',
            'paid_percent'
        ]


class EmployeeRatingSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    total_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    avg_rating = serializers.FloatField()
    high_season_tours = serializers.IntegerField()
    efficiency_score = serializers.FloatField()

    class Meta:
        model = Employee
        fields = [
            'employee_id',
            'full_name',
            'total_bookings',
            'confirmed_bookings',
            'avg_rating',
            'high_season_tours',
            'efficiency_score'
        ]

class TourPriceComparisonSerializer(serializers.Serializer):
    category = serializers.CharField()
    tour_count = serializers.IntegerField()
    avg_price = serializers.FloatField()

class MonthlyPaymentStatsSerializer(serializers.Serializer):
    month = serializers.CharField()
    deposits = serializers.DecimalField(max_digits=10, decimal_places=2)
    full_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)

class EmployeePerformanceSerializer(serializers.Serializer):
    employee_name = serializers.CharField()
    total_bookings = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_check = serializers.DecimalField(max_digits=10, decimal_places=2)
    confirmation_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    composite_rank = serializers.IntegerField()
    performance_category = serializers.CharField()


class ClientDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(read_only=True)
    total_bookings = serializers.IntegerField(read_only=True)
    last_booking_date = serializers.CharField(read_only=True)
    last_tour = serializers.CharField(read_only=True)
    last_rating = serializers.CharField(read_only=True)
    last_comment = serializers.CharField(read_only=True)

    class Meta:
        model = Client
        fields = [
            'client_id',
            'client_name',
            'email',
            'phone',
            'total_bookings',
            'last_booking_date',
            'last_tour',
            'last_rating',
            'last_comment'
        ]


class TourThemeStatsSerializer(serializers.Serializer):
    theme = serializers.CharField()
    tours_count = serializers.IntegerField()
    avg_price = serializers.FloatField()
    avg_difficulty = serializers.FloatField()
    cheapest_tour = serializers.FloatField()
    most_expensive_tour = serializers.FloatField()
    total_revenue = serializers.FloatField()
    bookings_count = serializers.IntegerField()
    avg_rating = serializers.CharField()
    most_popular_tour = serializers.CharField()