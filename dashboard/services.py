from django.db.models import Sum, Avg
from payments.models import Payment
from users.models import Booking

def get_seller_dashboard_data(seller):
    total_earnings = Payment.objects.filter(
        booking__property__owner=seller, status="COMPLETED"
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_bookings = Booking.objects.filter(property__owner=seller).count()

    avg_rating = Booking.objects.filter(property__owner=seller).aggregate(
        average=Avg('review__rating')
    )['average'] or 0

    monthly_earnings = Payment.objects.filter(
        booking__property__owner=seller, status="COMPLETED"
    ).extra(select={'month': "EXTRACT(month FROM created_at)"}) \
        .values('month') \
        .annotate(total=Sum('amount')) \
        .order_by('month')

    return {
        "total_earnings": total_earnings,
        "total_bookings": total_bookings,
        "average_rating": round(avg_rating, 2),
        "monthly_earnings": list(monthly_earnings),
    }
