from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError

from .services import handle_notify


@method_decorator(csrf_exempt, name="dispatch")
class NotifyView(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            handle_notify(request.POST)
        except ValidationError as exc:
            msg = list(exc.detail.values())[0][0]
            return HttpResponse(f"NO: {msg}")
        return HttpResponse("YES")
