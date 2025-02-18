from django.contrib import admin
from userSystem.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    
    list_display=("username","first_name","last_name","email","role","is_active","is_superuser","created_at","updated_at")
    search_fields=("username","email",)
    ordering=("username","email",)
    fieldsets=(
        ("Kullanıcı Bilgileri",{"fields":("username","password","email","profile_picture")}),
        ("Personel Bilgileri",{"fields":("first_name","last_name",)}),
        ("İzinleri",{"fields":("role","is_superuser","is_active",)}),
    )
    
    add_fieldsets=(
        (None,{
            "classes":("wide",),
            "fields":("username","password1","password2","role","is_active","is_staff","is_superuser",)
        }),
    )