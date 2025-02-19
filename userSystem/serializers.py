from rest_framework import serializers
from userSystem.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "phone_number", "tckn", "address", "profile_picture", "role",
            "created_at", "updated_at", "is_active", "is_staff"
        ]
        read_only_fields = ["created_at", "updated_at"]