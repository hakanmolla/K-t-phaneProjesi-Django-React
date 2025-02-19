
# 📌 Kategori Serializer'ı
from rest_framework import serializers
from .models import User, Category, Publisher, Author, Book, Loan, Reservation, Comment, Favorite, Penalty, BookTracking
from userSystem.serializers import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

# 📌 Yayınevi Serializer'ı
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "address", "website"]

# 📌 Yazar Serializer'ı
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "birth_date"]

# 📌 Kitap Serializer'ı
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id", "title", "isbn", "category", "author", "publisher",
            "publication_date", "pages", "language", "description",
            "cover_image", "stock", "status", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

# 📌 Ödünç Alma Serializer'ı
class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "user", "book", "loan_date", "due_date", "return_date", "is_returned"]
        read_only_fields = ["loan_date", "return_date"]

# 📌 Rezervasyon Serializer'ı
class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "book", "reservation_date", "expiration_date", "is_active"]
        read_only_fields = ["reservation_date", "expiration_date"]

# 📌 Yorum Serializer'ı
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "book", "text", "rating", "created_at"]
        read_only_fields = ["created_at"]

# 📌 Favori Serializer'ı
class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "user", "book", "added_at"]
        read_only_fields = ["added_at"]

# 📌 Ceza Serializer'ı
class PenaltySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Penalty
        fields = ["id", "user", "amount", "reason", "is_paid", "issued_at", "paid_at"]
        read_only_fields = ["issued_at", "paid_at"]

# 📌 Kitap Takip Serializer'ı
class BookTrackingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookTracking
        fields = ["id", "user", "book", "notification_status", "notified_at"]
        read_only_fields = ["notified_at"]