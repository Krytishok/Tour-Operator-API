# tours/views.py
from rest_framework import viewsets
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
from .serializers import (
    ClientSerializer,
    EmployeeSerializer,
    TourSerializer,
    BookingSerializer,
    VisaTypeSerializer,
    VisaSerializer,
    ChinaRegionSerializer,
    ChinaCitySerializer,
    HotelSerializer,
    ExcursionSerializer,
    ChineseGuideSerializer,
    FestivalSerializer,
    TransportProviderSerializer,
    InsuranceSerializer,
    ReviewSerializer,
    TourAgencySerializer,
    PaymentSerializer,
    BookingsVisaSerializer,
    TourExcursionSerializer,
    TourFestivalSerializer,
    TourHotelSerializer,
    TourRegionSerializer,
    TourToAgencySerializer,
    TourTransportSerializer,
    BookingsVisaSerializer,
    HotelOccupancySerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class VisaTypeViewSet(viewsets.ModelViewSet):
    queryset = VisaType.objects.all()
    serializer_class = VisaTypeSerializer


class VisaViewSet(viewsets.ModelViewSet):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer


class ChinaRegionViewSet(viewsets.ModelViewSet):
    queryset = ChinaRegion.objects.all()
    serializer_class = ChinaRegionSerializer


class ChinaCityViewSet(viewsets.ModelViewSet):
    queryset = ChinaCity.objects.all()
    serializer_class = ChinaCitySerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class ExcursionViewSet(viewsets.ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer


class ChineseGuideViewSet(viewsets.ModelViewSet):
    queryset = ChineseGuide.objects.all()
    serializer_class = ChineseGuideSerializer


class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer


class TransportProviderViewSet(viewsets.ModelViewSet):
    queryset = TransportProvider.objects.all()
    serializer_class = TransportProviderSerializer


class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class TourAgencyViewSet(viewsets.ModelViewSet):
    queryset = TourAgency.objects.all()
    serializer_class = TourAgencySerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class BookingsVisaViewSet(viewsets.ModelViewSet):
    queryset = BookingsVisa.objects.all()
    serializer_class = BookingsVisaSerializer


class TourExcursionViewSet(viewsets.ModelViewSet):
    queryset = TourExcursion.objects.all()
    serializer_class = TourExcursionSerializer


class TourFestivalViewSet(viewsets.ModelViewSet):
    queryset = TourFestival.objects.all()
    serializer_class = TourFestivalSerializer


class TourHotelViewSet(viewsets.ModelViewSet):
    queryset = TourHotel.objects.all()
    serializer_class = TourHotelSerializer


class TourRegionViewSet(viewsets.ModelViewSet):
    queryset = TourRegion.objects.all()
    serializer_class = TourRegionSerializer


class TourToAgencyViewSet(viewsets.ModelViewSet):
    queryset = TourToAgency.objects.all()
    serializer_class = TourToAgencySerializer


class TourTransportViewSet(viewsets.ModelViewSet):
    queryset = TourTransport.objects.all()
    serializer_class = TourTransportSerializer


class HotelOccupancyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HotelOccupancy.objects.all()
    serializer_class = HotelOccupancySerializer