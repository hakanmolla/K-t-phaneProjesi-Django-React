from rest_framework import viewsets, permissions
from .models import Category, Publisher, Author, Book, Loan, Reservation, Comment, Favorite, Penalty, BookTracking
from .serializers import (
    CategorySerializer, PublisherSerializer, AuthorSerializer, BookSerializer,
    LoanSerializer, ReservationSerializer, CommentSerializer, FavoriteSerializer,
    PenaltySerializer, BookTrackingSerializer
)

# 📌 Kategori ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 📌 Yayınevi ViewSet
class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 📌 Yazar ViewSet
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 📌 Kitap ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 📌 Ödünç Alma ViewSet
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # permission_classes = [permissions.IsAuthenticated]

# 📌 Rezervasyon ViewSet
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

# 📌 Yorum ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 📌 Favori ViewSet
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]

# 📌 Ceza ViewSet
class PenaltyViewSet(viewsets.ModelViewSet):
    queryset = Penalty.objects.all()
    serializer_class = PenaltySerializer
    # permission_classes = [permissions.IsAuthenticated]

# 📌 Kitap Takip ViewSet
class BookTrackingViewSet(viewsets.ModelViewSet):
    queryset = BookTracking.objects.all()
    serializer_class = BookTrackingSerializer
    # permission_classes = [permissions.IsAuthenticated]
