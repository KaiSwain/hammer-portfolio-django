from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from hammer_backendapi.views import login_user
router = routers.DefaultRouter(trailing_slash=False)



urlpatterns = [
    path('admin/', admin.site.urls),  # This enables /admin
    path('', include(router.urls)),
    path('login', login_user)
]

