# tours/urls.py
from django.urls import path, include


from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    EmployeeViewSet,
    TourViewSet,
    BookingViewSet,
    VisaTypeViewSet,
    VisaViewSet,
    ChinaRegionViewSet,
    ChinaCityViewSet,
    HotelViewSet,
    ExcursionViewSet,
    ChineseGuideViewSet,
    FestivalViewSet,
    TransportProviderViewSet,
    InsuranceViewSet,
    ReviewViewSet,
    TourAgencyViewSet,
    PaymentViewSet,
    BookingsVisaViewSet,
    TourExcursionViewSet,
    TourFestivalViewSet,
    TourHotelViewSet,
    TourRegionViewSet,
    TourToAgencyViewSet,
    TourTransportViewSet,
    HotelOccupancyViewSet,
)
from .reports.api_views import (
    PavelFriendsView, FestivalTourPriceComparisonView,
    EmployeeRatingsView, TourWithPaidExcursionsView,
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'tours', TourViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'visa-types', VisaTypeViewSet)
router.register(r'visas', VisaViewSet)
router.register(r'regions', ChinaRegionViewSet)
router.register(r'cities', ChinaCityViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'excursions', ExcursionViewSet)
router.register(r'guides', ChineseGuideViewSet)
router.register(r'festivals', FestivalViewSet)
router.register(r'transport-providers', TransportProviderViewSet)
router.register(r'insurances', InsuranceViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'agencies', TourAgencyViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'booking-visas', BookingsVisaViewSet)
router.register(r'tour-excursions', TourExcursionViewSet)
router.register(r'tour-festivals', TourFestivalViewSet)
router.register(r'tour-hotels', TourHotelViewSet)
router.register(r'tour-regions', TourRegionViewSet)
router.register(r'tour-agencies', TourToAgencyViewSet)
router.register(r'tour-transports', TourTransportViewSet)
router.register(r'hotel-occupancy', HotelOccupancyViewSet, basename='hotel-occupancy')

urlpatterns = [
    path('', include(router.urls)),

    path('pavel/friends/', PavelFriendsView.as_view(), name='pavel-friends'),
    path('tours/with-paid-excursions/', TourWithPaidExcursionsView.as_view(), name='tours-with-paid-excursions'),
    path('festivals/tours/price-comparison', FestivalTourPriceComparisonView.as_view(), name='festival-comparsion'),
    path('employee/ratings/', EmployeeRatingsView.as_view(), name='employee-ratings'),
]