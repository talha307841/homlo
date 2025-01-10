from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_seller_dashboard_data

class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_seller:
            return Response(
                {"error": "Only sellers can access this data."},
                status=403
            )
        data = get_seller_dashboard_data(user)
        return Response(data, status=200)
