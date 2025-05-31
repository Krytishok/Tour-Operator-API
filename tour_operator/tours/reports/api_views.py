from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..serializers import (
    TourExcursionStatsSerializer,
    EmployeeRatingSerializer,
    TourPriceComparisonSerializer, ClientPavelSerializer,
)
from django.db.models.functions import (
    Round, ExtractYear, ExtractMonth, Coalesce, Concat)
from django.db.models import (
    Subquery, OuterRef, Count,
    Avg, Sum, Case, When, IntegerField,
    F, Value, Q, Min, Max, FloatField, CharField
)
from ..models import (
    Client, Booking, Tour, TourExcursion, Review, Employee,
    Excursion, TourFestival
)


class PavelFriendsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ClientPavelSerializer
    def get(self, request):
        client_tours = Booking.objects.filter(client_id=1).values('tour_id')

        friends = Client.objects.filter(
            booking__tour_id__in=Subquery(client_tours)
        ).exclude(client_id=1).distinct().values(
            'client_id', 'first_name', 'last_name', 'email', 'phone'
        )

        serializer = ClientPavelSerializer(friends, many=True)
        return Response(serializer.data)


class TourWithPaidExcursionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tours = Tour.objects.annotate(
            total_excursions=Count('tourexcursion'),
            paid_excursions=Sum(
                Case(
                    When(tourexcursion__included_in_price=False, then=1),
                    default=0,
                    output_field=FloatField()
                )
            )
        ).annotate(
            paid_percent=Round(
                (100.0 * F('paid_excursions') / F('total_excursions')),
                2
            )
        ).filter(
            paid_excursions__gt=0,
            paid_percent__gt=30
        ).order_by('-paid_percent')

        # Сериализуем результаты
        serializer = TourExcursionStatsSerializer(tours, many=True)
        return Response(serializer.data)


class EmployeeRatingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        employees = Employee.objects.annotate(
            full_name=Concat(
                'first_name',
                Value(' '),
                'last_name',
                output_field=CharField()
            ),
            total_bookings=Count('booking'),
            confirmed_bookings=Sum(
                Case(
                    When(booking__status='Confirmed', then=1),
                    default=0,
                    output_field=FloatField()
                )
            ),
            avg_rating=Avg('booking__client__review__rating')
        ).annotate(
            # Рассчитываем количество туров в высокий сезон
            high_season_tours=Coalesce(
                Count(
                    Case(
                        When(booking__tour__season='High', then='booking__tour'),
                        distinct=True,
                        output_field=FloatField()
                    )
                ),
                0
            ),
            # Рассчитываем эффективность по формуле
            efficiency_score=(
                    F('confirmed_bookings') * 0.4 +
                    F('high_season_tours') * 0.3 +
                    F('avg_rating') * 0.3
            )
        ).filter(
            confirmed_bookings__gt=0
        ).order_by('-efficiency_score')

        # Сериализуем результаты
        serializer = EmployeeRatingSerializer(employees, many=True)
        return Response(serializer.data)


class FestivalTourPriceComparisonView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Туры с популярными фестивалями (средняя популярность >= 4)
        festival_tours_stats = Tour.objects.filter(
            tourfestival__festival__popularity__gte=4
        ).annotate(
            avg_popularity=Avg('tourfestival__festival__popularity')
        ).filter(
            avg_popularity__gte=4
        ).aggregate(
            tour_count=Count('tour_id'),  # Используем tour_id вместо id
            avg_price=Round(Avg('price'), 2)
        )

        # 2. Туры без фестивалей
        non_festival_tours_stats = Tour.objects.exclude(
            tour_id__in=TourFestival.objects.values('tour__tour_id')  # Используем tour__tour_id
        ).aggregate(
            tour_count=Count('tour_id'),  # Используем tour_id вместо id
            avg_price=Round(Avg('price'), 2)
        )

        # 3. Формируем итоговый результат
        results = [
            {
                'category': 'Festival Tours',
                'tour_count': festival_tours_stats['tour_count'] or 0,
                'avg_price': festival_tours_stats['avg_price'] or 0
            },
            {
                'category': 'Non-Festival Tours',
                'tour_count': non_festival_tours_stats['tour_count'] or 0,
                'avg_price': non_festival_tours_stats['avg_price'] or 0
            }
        ]

        return Response(results)