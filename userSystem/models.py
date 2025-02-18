from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

# Dosya boyutu doğrulaması (Maksimum 2MB)
def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2 MB
    if value.size > limit:
        raise ValidationError('Dosya boyutu 2 MB\'dan büyük olamaz.')

# Telefon numarası doğrulaması
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Telefon numarası geçerli bir formatta olmalıdır."
)

# TCKN doğrulama
def validate_tckn(value):
    if len(value) != 11:
        raise ValidationError("TCKN 11 haneli olmalıdır.")
    
    if not value.isdigit():
        raise ValidationError("TCKN sadece rakamlardan oluşmalıdır.")
    
    if int(value[-1]) % 2 != 0:  # Son hane çift olmalı
        raise ValidationError("TCKN'nin son hanesi çift rakam olmalıdır.")

# Profil resmi için dinamik dosya yolu belirleme
def user_profile_picture_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'

# Kullanıcı yöneticisi (User Manager)
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Kullanıcı adı girmek zorunludur")
        if not email:
            raise ValueError("Email girmek zorunludur")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

# Kullanıcı Modeli
class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = [
        ("admin", "Admin"),
        ("staff", "Personel"),
        ("member", "Üye"),
    ]

    username = models.CharField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, validators=[phone_validator], blank=True, default="")
    tckn = models.CharField(max_length=11, blank=True, validators=[validate_tckn]) 
    address = models.TextField(blank=True, null=True)
    profile_picture = models.FileField(
        upload_to=user_profile_picture_path,
        validators=[validate_file_size],
        blank=True,
        null=True,
        default='profile_images/default.png'
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default="member")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    class Meta:
        db_table = 'user_tablosu'  

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
