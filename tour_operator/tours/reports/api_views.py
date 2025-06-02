from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..serializers import (
    TourExcursionStatsSerializer,
    EmployeeRatingSerializer,
    TourPriceComparisonSerializer,
    ClientPavelSerializer,
    MonthlyPaymentStatsSerializer,
    EmployeePerformanceSerializer
)
from django.db.models.functions import (
    Round, ExtractYear, ExtractMonth, Coalesce, Concat, TruncMonth)
from django.db.models import (
    Subquery, OuterRef, Count,
    Avg, Sum, Case, When, IntegerField,
    F, Value, Q, Min, Max, FloatField, CharField
)
from ..models import (
    Client, Booking, Tour, TourExcursion, Review, Employee,
    Excursion, TourFestival, Payment
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
