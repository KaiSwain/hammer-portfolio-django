from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),  # This enables /admin
    path('', include(router.urls)),
]

