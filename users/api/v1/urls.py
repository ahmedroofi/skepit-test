from rest_framework.routers import DefaultRouter
from users.api.v1 import viewsets

app_name = 'users'
router = DefaultRouter()
router.register(r'register', viewsets.UserRegister, basename='register')
router.register(r'login', viewsets.UserLogin, basename='login')
router.register(r'logout', viewsets.Logout, basename='logout')
urlpatterns = router.urls
