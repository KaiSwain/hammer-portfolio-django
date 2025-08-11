from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from hammer_backendapi.views import login_user, StudentViewSet, StudentForeignKeyOptionsView
from hammer_backendapi.views.certificates import generate_workforce_certificate,generate_employability_certificate,generate_hammermath_certificate,generate_nccer_certificate,generate_osha_certificate,generate_portfolio_certificate
router = routers.DefaultRouter(trailing_slash=False)

router.register(r"students", StudentViewSet, "student")



urlpatterns = [
    path('admin/', admin.site.urls),  # This enables /admin
    path('', include(router.urls)),
    path('login', login_user),
    path("generate/portfolio/", generate_portfolio_certificate),
    path("generate/nccer/", generate_nccer_certificate),
    path("generate/osha/", generate_osha_certificate),
    path("generate/hammermath/", generate_hammermath_certificate),
    path("generate/employability/", generate_employability_certificate),
    path("generate/workforce/", generate_workforce_certificate),
    path("details/", StudentForeignKeyOptionsView.as_view()),
]

