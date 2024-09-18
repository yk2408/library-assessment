from django.contrib.auth.models import User
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []

    @action(detail=True, methods=['post'])
    def add_favorite(self, request, pk=None):
        book = self.get_object()
        user = request.user
        user.favorite_books.add(book)
        return Response({"status": "Book added to favorites"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_favorite(self, request, pk=None):
        book = self.get_object()
        user = request.user
        user.favorite_books.remove(book)
        return Response({"status": "Book removed from favorites"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        user = request.user
        favorite_books = user.favorite_books.all()

        if not favorite_books.exists():
            return Response({"status": "No favorites to base recommendations on"}, status=status.HTTP_400_BAD_REQUEST)

        favorite_books = favorite_books[:20]  # Limit to 20 favorite books
        favorite_descriptions = [book.description for book in favorite_books]

        all_books = Book.objects.exclude(id__in=favorite_books.values_list('id', flat=True))
        all_descriptions = [book.description for book in all_books]

        # Use TF-IDF Vectorizer for similarity
        vectorizer = TfidfVectorizer()
        all_descriptions.append(" ".join(favorite_descriptions))
        tfidf_matrix = vectorizer.fit_transform(all_descriptions)

        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        similar_books_indices = cosine_sim[0].argsort()[-5:][::-1]

        # Convert QuerySet to list
        all_books_list = list(all_books)
        recommended_books = [all_books_list[i] for i in similar_books_indices]
        serializer = BookSerializer(recommended_books, many=True)

        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [AllowAny()]
        return super().get_permissions()