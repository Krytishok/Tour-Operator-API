from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import timedelta
from ..serializers import (
    TourExcursionStatsSerializer,
    EmployeeRatingSerializer,
    TourPriceComparisonSerializer,
    ClientPavelSerializer,
    MonthlyPaymentStatsSerializer,
    EmployeePerformanceSerializer,
    ClientDetailSerializer,
    TourThemeStatsSerializer
)
from django.db.models.functions import (
    Round, ExtractDay, ExtractMonth, Coalesce, Concat, TruncMonth)
from django.db.models import (
    Subquery, OuterRef, Count,
    Avg, Sum, Case, When, IntegerField,
    F, Value, Q, Min, Max, FloatField, CharField, ExpressionWrapper
)
from ..models import (
    Client, Booking, Tour, TourExcursion, Review, Employee,
    Excursion, TourFestival, Payment, TourTransport, TransportProvider, TourHotel
)


class PavelFriendsView(APIView):
    permission_classes = [AllowAny]
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
            efficiency_score=(
                    F('confirmed_bookings') * 0.4 +
                    F('high_season_tours') * 0.3 +
                    F('avg_rating') * 0.3
            )
        ).filter(
            confirmed_bookings__gt=0
        ).order_by('-efficiency_score')

        serializer = EmployeeRatingSerializer(employees, many=True)
        return Response(serializer.data)


class FestivalTourPriceComparisonView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        festival_tours_stats = Tour.objects.filter(
            tourfestival__festival__popularity__gte=4
        ).annotate(
            avg_popularity=Avg('tourfestival__festival__popularity')
        ).filter(
            avg_popularity__gte=4
        ).aggregate(
            tour_count=Count('tour_id'),
            avg_price=Round(Avg('price'), 2)
        )

        non_festival_tours_stats = Tour.objects.exclude(
            tour_id__in=TourFestival.objects.values('tour__tour_id')
        ).aggregate(
            tour_count=Count('tour_id'),
            avg_price=Round(Avg('price'), 2)
        )

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


class MonthlyPaymentStatsView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request):
        monthly_deposits = Payment.objects.filter(
            is_deposit=True
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            deposit_amount=Sum('amount')
        ).order_by('month')

        monthly_full_payments = Payment.objects.filter(
            is_deposit=False
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            full_payment_amount=Sum('amount')
        ).order_by('month')

        all_months = Payment.objects.annotate(
            month=TruncMonth('payment_date')
        ).values_list('month', flat=True).distinct().order_by('month')

        results = []
        for month in all_months:
            deposit = next(
                (item['deposit_amount'] for item in monthly_deposits if item['month'] == month),
                0
            )
            full_payment = next(
                (item['full_payment_amount'] for item in monthly_full_payments if item['month'] == month),
                0
            )

            results.append({
                'month': month.strftime('%Y-%m'),
                'deposits': deposit,
                'full_payments': full_payment,
                'total_income': deposit + full_payment
            })

        serializer = MonthlyPaymentStatsSerializer(results, many=True)
        return Response(serializer.data)


class EmployeePerformanceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        employees = Employee.objects.filter(
            position="Agent"
        ).annotate(
            employee_name=Concat('first_name', Value(' '), 'last_name'),
            total_bookings=Count('booking'),
            total_sales=Sum('booking__total_price'),
            avg_check=Avg('booking__total_price'),
            confirmation_rate=100.0 * Sum(
                Case(
                    When(booking__status='Confirmed', then=1),
                    default=0,
                    output_field=FloatField()
                )
            ) / Count('booking'),
            avg_processing_time=Avg(
                F('booking__booking_date') - F('booking__client__visa__application_date')
            )
        ).filter(
            total_bookings__gt=0
        )

        ranked_employees = []
        for emp in employees.order_by('-total_sales'):
            emp_data = {
                'employee_name': emp.employee_name,
                'total_bookings': emp.total_bookings,
                'total_sales': float(emp.total_sales or 0),
                'avg_check': round(float(emp.avg_check or 0), 2),
                'confirmation_rate': round(float(emp.confirmation_rate or 0), 2),
            }

            emp_data['sales_rank'] = Employee.objects.filter(
                position="Agent",
                booking__isnull=False
            ).annotate(
                total_sales=Sum('booking__total_price')
            ).filter(
                total_sales__gt=emp.total_sales
            ).count() + 1

            emp_data['check_rank'] = Employee.objects.filter(
                position="Agent",
                booking__isnull=False
            ).annotate(
                avg_check=Avg('booking__total_price')
            ).filter(
                avg_check__gt=emp.avg_check
            ).count() + 1

            emp_data['rate_rank'] = Employee.objects.filter(
                position="Agent",
                booking__isnull=False
            ).annotate(
                rate=100.0 * Sum(
                    Case(
                        When(booking__status='Confirmed', then=1),
                        default=0,
                        output_field=FloatField()
                    )
                ) / Count('booking')
            ).filter(
                rate__gt=emp.confirmation_rate
            ).count() + 1

            emp_data['time_rank'] = Employee.objects.filter(
                position="Agent",
                booking__isnull=False
            ).annotate(
                proc_time=Avg(
                    F('booking__booking_date') - F('booking__client__visa__application_date')
                )
            ).filter(
                proc_time__lt=emp.avg_processing_time
            ).count() + 1

            emp_data['composite_rank'] = (
                    emp_data['sales_rank'] +
                    emp_data['check_rank'] +
                    emp_data['rate_rank'] +
                    emp_data['time_rank']
            )

            if emp_data['composite_rank'] <= 10:
                emp_data['performance_category'] = 'Top Performer'
            elif emp_data['composite_rank'] <= 20:
                emp_data['performance_category'] = 'High Performer'
            elif emp_data['composite_rank'] <= 30:
                emp_data['performance_category'] = 'Average Performer'
            else:
                emp_data['performance_category'] = 'Needs Improvement'

            ranked_employees.append(emp_data)


        ranked_employees.sort(key=lambda x: x['composite_rank'])

        serializer = EmployeePerformanceSerializer(ranked_employees, many=True)
        return Response(serializer.data)


class ClientListWithDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        last_booking_subquery = Booking.objects.filter(
            client_id=OuterRef('pk')
        ).order_by('-booking_date').values('booking_date')[:1]

        last_tour_subquery = Tour.objects.filter(
            booking__client_id=OuterRef('pk')
        ).order_by('-booking__booking_date').values('name')[:1]

        last_rating_subquery = Review.objects.filter(
            client_id=OuterRef('pk')
        ).order_by('-review_date').values('rating')[:1]

        last_comment_subquery = Review.objects.filter(
            client_id=OuterRef('pk')
        ).order_by('-review_date').values('comment')[:1]

        clients = Client.objects.annotate(
            client_name=Concat('first_name', Value(' '), 'last_name'),
            total_bookings=Count('booking'),
            last_booking_date=Coalesce(
                Subquery(last_booking_subquery),
                Value('Нет бронирований', output_field=CharField()),
                output_field=CharField()
            ),
            last_tour=Coalesce(
                Subquery(last_tour_subquery),
                Value('Не бронировал', output_field=CharField()),
                output_field=CharField()
            ),
            last_rating=Coalesce(
                Subquery(last_rating_subquery),
                Value('Нет оценки', output_field=CharField()),
                output_field=CharField()
            ),
            last_comment=Coalesce(
                Subquery(last_comment_subquery),
                Value('Нет отзыва', output_field=CharField()),
                output_field=CharField()
            )
        ).filter(
            booking__isnull=False
        ).order_by(
            '-booking__booking_date'
        ).distinct()[:5]

        serializer = ClientDetailSerializer(clients, many=True)
        return Response(serializer.data)


class TourThemeAnalysisView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        most_popular_subquery = Tour.objects.filter(
            theme=OuterRef('theme')
        ).annotate(
            bookings_count=Count('booking')
        ).order_by('-bookings_count').values('name')[:1]

        theme_stats = Tour.objects.filter(
            theme__isnull=False
        ).values('theme').annotate(
            tours_count=Count('tour_id', distinct=True),
            avg_price=Avg('price'),
            avg_difficulty=Avg('difficulty_level'),
            cheapest_tour=Min('price'),
            most_expensive_tour=Max('price'),
            total_revenue=Sum(
                'booking__total_price',
                filter=~Q(booking__status='Cancelled')
            ),
            bookings_count=Coalesce(
                Count(
                    'booking',
                    filter=~Q(booking__status='Cancelled'),
                    distinct=True
                ),
                0
            ),
            avg_rating=Coalesce(
                Round(Avg('review__rating'), 1, output_field=CharField()),
                Value("Нет рейтинга", output_field=CharField())
            ),
            most_popular_tour=Coalesce(
                Subquery(most_popular_subquery),
                Value("Нет данных", output_field=CharField())
            )
        ).order_by('-bookings_count')

        results = []
        for stat in theme_stats:

            results.append({
                'theme': stat['theme'],
                'tours_count': stat['tours_count'],
                'avg_price': round(float(stat['avg_price'] or 0), 2),
                'avg_difficulty': round(float(stat['avg_difficulty'] or 0), 1),
                'cheapest_tour': round(float(stat['cheapest_tour'] or 0), 2),
                'most_expensive_tour': round(float(stat['most_expensive_tour'] or 0), 2),
                'total_revenue': round(float(stat['total_revenue'] or 0), 2),
                'bookings_count': stat['bookings_count'],
                'avg_rating': stat['avg_rating'],
                'most_popular_tour': stat['most_popular_tour']
            })

        serializer = TourThemeStatsSerializer(results, many=True)
        return Response(serializer.data)




