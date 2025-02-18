from rest_framework import serializers
from userSystem.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=['groups','user_permissions',"last_login","is_superuser","is_staff"]