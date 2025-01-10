from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from notifications.services import create_notification
from properties.models import Property

class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            property_id = request.data.get('property')
            try:
                property_instance = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(user=request.user, property=property_instance)

            # Notify the property owner
            create_notification(
                user=property_instance.owner,
                message=f"{request.user.username} has left a review on your property '{property_instance.name}'."
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListReviewsForPropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, property_id):
        try:
            property_instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(property=property_instance).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
