from rest_framework.routers import DefaultRouter
from .viewsets import BookViewSet, AuthorViewSet, UserViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
