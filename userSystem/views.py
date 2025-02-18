from rest_framework import viewsets,permissions
from userSystem.models import User
from userSystem.serializers import UserSerializer


class UserViewSets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    