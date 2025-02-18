from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Publisher, Author, Book, Loan, Reservation, Comment, Favorite, Penalty, BookTracking

# Kategori Modeli
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# Yayınevi Modeli
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)
    list_filter = ("name",)


# Yazar Modeli
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    search_fields = ("first_name", "last_name")
    list_filter = ("birth_date",)


# Kitap Modeli
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "category", "publisher", "status", "stock")
    list_filter = ("status", "category", "publisher")
    search_fields = ("title", "isbn")
    filter_horizontal = ("author",)  # ManyToMany alanı için daha iyi bir görünüm
    readonly_fields = ("created_at", "updated_at")

    # Kapak resmini gösterme
    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="50" height="75" />', obj.cover_image.url)
        return "(Kapak Yok)"

    cover_image_preview.short_description = "Kapak Resmi"


# Ödünç Alma Modeli (Loan)
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "loan_date", "due_date", "return_date", "is_returned")
    list_filter = ("is_returned", "loan_date", "due_date")
    search_fields = ("user__username", "book__title")
    autocomplete_fields = ("user", "book")  # Kullanıcı ve kitap seçimini kolaylaştırır
    readonly_fields = ("return_date",)


# Rezervasyon Modeli
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "reservation_date", "expiration_date", "is_active")
    list_filter = ("is_active", "reservation_date")
    search_fields = ("user__username", "book__title")
    autocomplete_fields = ("user", "book")


# Yorum Modeli
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "book__title")


# Favori Modeli
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "added_at")
    search_fields = ("user__username", "book__title")


# Ceza Modeli
@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "reason", "is_paid", "issued_at", "paid_at")
    list_filter = ("is_paid", "reason")
    search_fields = ("user__username",)
    readonly_fields = ("issued_at", "paid_at")


# Kitap Takip Modeli
@admin.register(BookTracking)
class BookTrackingAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "notification_status", "notified_at")
    list_filter = ("notification_status",)
    search_fields = ("user__username", "book__title")
