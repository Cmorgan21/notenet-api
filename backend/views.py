from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view()
@permission_classes([AllowAny])
def root_route(request):
    return Response({
        "message": "Welcome to my Notenet Api! Where you can create, read, update, and delete notes"
    })