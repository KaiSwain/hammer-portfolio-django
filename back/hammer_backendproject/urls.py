from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from hammer_backendapi.views import login_user, StudentForeignKeyOptionsView
from hammer_backendapi.views.students import StudentViewSet
from hammer_backendapi.views.certificates import generate_workforce_certificate,generate_employability_certificate,generate_hammermath_certificate,generate_nccer_certificate,generate_osha_certificate,generate_portfolio_certificate
from hammer_backendapi.views.generate_all import generate_all_certificates
from hammer_backendapi.views.health import health_check, api_info
from hammer_backendapi.views.support import support_request

router = routers.DefaultRouter(trailing_slash=True)  # Enable trailing slashes
router.register(r"students", StudentViewSet, "student")

# API URLs with /api/ prefix
api_patterns = [
    path('', include(router.urls)),
    path('login/', login_user),
    path("generate/all/", generate_all_certificates),
    path("generate/portfolio/", generate_portfolio_certificate),
    path("generate/nccer/", generate_nccer_certificate),
    path("generate/osha/", generate_osha_certificate),
    path("generate/hammermath/", generate_hammermath_certificate),
    path("generate/employability/", generate_employability_certificate),
    path("generate/workforce/", generate_workforce_certificate),
    path("details/", StudentForeignKeyOptionsView.as_view()),
    path("health/", health_check),
    path("info/", api_info),
    path("support/", support_request),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('health/', health_check),  # Root health check for load balancers
    
    # Backward compatibility (remove in future versions)
    path('', include(router.urls)),
    path('login', login_user),
    path("generate/all/", generate_all_certificates),
    path("generate/portfolio/", generate_portfolio_certificate),
    path("generate/nccer/", generate_nccer_certificate),
    path("generate/osha/", generate_osha_certificate),
    path("generate/hammermath/", generate_hammermath_certificate),
    path("generate/employability/", generate_employability_certificate),
    path("generate/workforce/", generate_workforce_certificate),
    path("details/", StudentForeignKeyOptionsView.as_view()),
]

