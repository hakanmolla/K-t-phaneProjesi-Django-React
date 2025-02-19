from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.core.exceptions import ValidationError

User = get_user_model()  # Kullanıcı modelini dinamik olarak al

# ISBN doğrulama
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

def isbn_validator(value):
    """Sadece ISBN-13 formatının uzunluğunu ve sayısallığını kontrol eder."""
    
    if not isinstance(value, str) or len(value) != 13 or not value.isdigit():
        raise ValidationError("❌ Geçersiz ISBN. ISBN 13 haneli ve sadece rakamlardan oluşmalıdır.")


# Kategori Modeli
class Category(models.Model):
    """Kitap kategorileri"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Yayınevi Modeli
class Publisher(models.Model):
    """Kitap yayınevi bilgileri"""
    name = models.CharField(max_length=150, unique=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Yazar Modeli
class Author(models.Model):
    """Kitap yazar bilgileri"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Kitap Modeli
class Book(models.Model):
    """Kitap bilgileri"""
    
    STATUS_CHOICES = [
        ("available", "Mevcut"),
        ("borrowed", "Ödünç Verildi"),
        ("reserved", "Rezerve Edildi"),
        ("lost", "Kayıp"),
    ]

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, validators=[isbn_validator], help_text="13 haneli ISBN numarası")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    author = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name="books")
    publication_date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default="Türkçe")
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True, default="book_covers/default.jpg")
    stock = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Ödünç Alma Modeli
def default_due_date():
    return now().date() + timedelta(days=14)

class Loan(models.Model):
    """Kitap ödünç alma modeli"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateField(default=now)
    due_date = models.DateField(default=default_due_date)  # Varsayılan iade süresi: 14 gün
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_returned:
            self.return_date = now().date()  # İade tarihi güncellensin
            self.book.status = "available"
            self.book.save()

        # Önce Loan kaydını güncelle
        super().save(*args, **kwargs)

        # Eğer bu kitabı rezerve eden biri varsa, rezervasyonu kapatıp yeni loan oluşturacağız
        if self.is_returned:
            reservation = Reservation.objects.filter(book=self.book, is_active=True).first()
            if reservation:
                reservation.is_active = False  # Rezervasyonu tamamlandı olarak işaretleyelim
                reservation.save()

                # Yeni Loan kaydını oluşturuyoruz
                new_loan = Loan.objects.create(
                    user=reservation.user,
                    book=self.book
                )

                # Kitabın durumunu güncelle
                new_loan.book.status = "borrowed"
                new_loan.book.save()



# Rezervasyon Modeli
def default_expiration_date():
    return now() + timedelta(days=3)

class Reservation(models.Model):
    """Kitap rezervasyon modeli"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
    reservation_date = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(default=default_expiration_date)  # Otomatik 3 gün geçerli
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title} (Rezerve)"

# Yorum Modeli
class Comment(models.Model):
    """Kitap yorumları"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)  # 1-5 arası puanlama
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title} ⭐{self.rating}"

# Favori Modeli
class Favorite(models.Model):
    """Kullanıcının favori kitapları"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorites")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ❤️ {self.book.title}"

# Ceza Modeli
class Penalty(models.Model):
    """Kullanıcı ceza modeli"""
    
    REASON_CHOICES = [
        ("late_return", "Gecikmiş Kitap İadesi"),
        ("damage", "Kitap Hasarı"),
        ("lost", "Kitap Kaybı"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="penalties")
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # 999.99 TL'ye kadar ceza
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    is_paid = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)  # Ödeme tarihi eklendi!

    def save(self, *args, **kwargs):
        now_time = now()  # `now()` sadece bir kez çağrılsın!

        if self.is_paid:
            self.paid_at = now_time
        else:
            self.paid_at = None  # Eğer ödeme geri alınırsa, tarih sıfırlansın

        super().save(*args, **kwargs)



# Kitap Takip Modeli
class BookTracking(models.Model):
    """Kitap stok takibi ve bildirimler"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="book_trackings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_trackings")
    notification_status = models.BooleanField(default=False)
    notified_at = models.DateTimeField(blank=True, null=True)  # Bildirim gönderildiği tarih

    def save(self, *args, **kwargs):
    # Eğer kitap tekrar "Mevcut" hale geldiyse ve bildirim gönderilmemişse, gönderelim
        if self.book.status == "available" and not self.notification_status:
            self.notification_status = True
            self.notified_at = now()  # Bildirim tarihi kaydedilsin

            # Burada kullanıcıya e-posta veya bildirim gönderme kodu eklenebilir
            # Örneğin:
            # send_email(self.user.email, "Takip ettiğiniz kitap artık kütüphanede!")

        super().save(*args, **kwargs)  # Her durumda `save(
