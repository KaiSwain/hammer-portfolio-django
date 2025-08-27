from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hammer_backendapi.models import (
    GenderIdentity,
    DiscAssessment,
    SixteenTypeAssessment,
    EnneagramResult,
    OshaType,
    FundingSource
)

class StudentForeignKeyOptionsView(APIView):
    def get(self, request):
        try:
            data = {
                "gender_identities": list(GenderIdentity.objects.values("id", "gender")),
                "disc_assessments": list(DiscAssessment.objects.values("id", "type_name")),
                "sixteen_type_assessments": list(SixteenTypeAssessment.objects.values("id", "type_name")),
                "enneagram_results": list(EnneagramResult.objects.values("id", "result_name")),
                "osha_types": list(OshaType.objects.values("id", "name")),
                "funding_sources": list(FundingSource.objects.values("id", "name", "description")),
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
