from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile',views.UserProfileViewSet)
urlpatterns = [
    path('login/',views.UserLoginApi.as_view()),
    path('', include(router.urls)),
]