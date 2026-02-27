from django.test import TestCase
from django.urls import reverse

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health_check(request):
    try:
        connections['default'].cursor()
        db_status = "ok"
    except OperationalError:
        db_status = "error"

    return JsonResponse({
        "status": "ok" if db_status == "ok" else "error",
        "database": db_status
    })

class HealthEndpointTest(TestCase):
    def test_health_endpoint(self):
        response = self.client.get

