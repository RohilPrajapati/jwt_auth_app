from django.urls import path
from .views import RegisterView,PostListView,AuthorListView,LoginView,PostDetailUpdateDeleteView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

urlpatterns = [
    # local urls
    path('register/', RegisterView.as_view()),
    path('post/', PostListView.as_view()),
    path('author/', AuthorListView.as_view()),
    path('login/', LoginView.as_view()),
    path('post/<int:pk>/', PostDetailUpdateDeleteView.as_view()),

    # third party url
    path('retoken/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]