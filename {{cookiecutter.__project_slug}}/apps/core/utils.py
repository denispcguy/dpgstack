from django.core.paginator import Paginator
import json
from django.http import HttpRequest, QueryDict
from typing import Literal
from django.http import HttpResponse


def get_paginated_queryset(queryset, page_number=1, paginate_by=10):
    paginator = Paginator(queryset, paginate_by)
    page_obj = paginator.get_page(page_number)
    return list(page_obj), page_obj


def toast(message='OK',
          response=None,
          variant: Literal["success", "danger"] = "success",
          title="Notification",
          ):
    if not response:
        response = HttpResponse()
    trigger_data = {
        "notify": {
            "message": message,
            "variant": variant,
            "title": title,
        }
    }
    response['HX-Trigger'] = json.dumps(trigger_data)
    return response


def extract_payload(request: HttpRequest):
    payload = {}
    payload.update(request.GET.dict())

    if request.POST or request.FILES:
        payload.update(request.POST.dict())
        payload.update(request.FILES.dict())

    elif request.body:
        payload.update(QueryDict(request.body).dict())

    return payload