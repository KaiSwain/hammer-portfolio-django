from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from hammer_backendapi.views import login_user, StudentForeignKeyOptionsView
from hammer_backendapi.views.students import StudentViewSet
# Import original certificate views
from hammer_backendapi.views import certificates, generate_all
from hammer_backendapi.views.health import health_check, api_info
from hammer_backendapi.views.support import support_request
# from hammer_backendapi.views.ai_diagnostic import ai_diagnostic

def test_view(request):
    return HttpResponse("TEST VIEW WORKING - Django URLs functional with MAIN branch (Sep 2)", content_type="text/plain")

router = routers.DefaultRouter(trailing_slash=True)  # Enable trailing slashes
router.register(r"students", StudentViewSet, "student")

# API URLs with /api/ prefix
api_patterns = [
    path('', include(router.urls)),
    path('login/', login_user),
    path("generate/all/", generate_all.generate_all_certificates),
    path("generate/portfolio/", certificates.generate_portfolio_certificate),
    path("generate/nccer/", certificates.generate_nccer_certificate),
    path("generate/osha/", certificates.generate_osha_certificate),
    path("generate/hammermath/", certificates.generate_hammermath_certificate),
    path("generate/employability/", certificates.generate_employability_certificate),
    path("generate/workforce/", certificates.generate_workforce_certificate),
    path("details/", StudentForeignKeyOptionsView.as_view()),
    path("health/", health_check),
    path("info/", api_info),
    path("support/", support_request),
    # path("ai-diagnostic/", ai_diagnostic),
]

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin interface - MOVED TO TOP
    path('test-django/', test_view),  # Test if Django routing works at all
    path('api/', include(api_patterns)),
    path('health/', health_check),  # Root health check for load balancers
    
    # Root URL - restored after fixing routing issue
    path('', api_info, name='api_info'),
]

# Add static files serving for production
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

