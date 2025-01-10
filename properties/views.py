from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer

class CreatePropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListPropertiesView(APIView):
    def get(self, request):
        properties = Property.objects.filter(available=True).order_by('-created_at')
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PropertyDetailView(APIView):
    def get(self, request, property_id):
        try:
            property_instance = Property.objects.get(id=property_id, available=True)
        except Property.DoesNotExist:
            return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PropertySerializer(property_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
