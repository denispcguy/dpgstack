from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest

from apps.core.utils import get_paginated_queryset, toast, extract_payload
from ..forms import BlueprintSimpleModelForm
from ..models import BlueprintSimpleModel


class CardsChildView(View):
    template_name = '_blueprint_cards_child.html'
    fields = ['name', 'description']
    url_name = '_blueprint:cards_child'
    url_name_detail = '_blueprint:cards_child_detail'

    def _get_context(self, payload: dict, local_context: dict):
        shared_context = {
            'page': payload.get('page', 1),
            'order_by': payload.get('order_by', 'id'),
            'fields': self.fields,
            'url_name': self.url_name,
            'url_name_detail': self.url_name_detail,
            'form': BlueprintSimpleModelForm(),
        }

        queryset = BlueprintSimpleModel.objects.all().order_by(
            shared_context['order_by'] or 'id')

        items, page_obj = get_paginated_queryset(
            queryset, shared_context['page'], paginate_by=8)

        local_context.update({
            'queryset': items,
            'page_obj': page_obj
        })

        return {**shared_context, **local_context}

    def get(self, request, pk=None):
        payload = extract_payload(request)

        match payload.pop('action', ''):
            case '':
                context = self._get_context(payload, {})
                return render(request, self.template_name, context)

            case 'normal-row':
                piece = get_object_or_404(BlueprintSimpleModel, pk=pk)
                local_context = {'piece': piece, 'form': BlueprintSimpleModelForm()}
                context = self._get_context(payload, local_context)
                return render(request, f'{self.template_name}#table_row', context)

            case 'edit-row':
                piece = get_object_or_404(BlueprintSimpleModel, pk=pk)
                local_context = {'piece': piece, 'form': BlueprintSimpleModelForm(instance=piece)}
                context = self._get_context(payload, local_context)
                return render(request, f'{self.template_name}#edit_row', context)

            case _:
                return HttpResponseBadRequest()

    def post(self, request, pk=None):
        payload = extract_payload(request)
        match payload.pop('action', ''):
            case 'accept-form':
                form = BlueprintSimpleModelForm(payload)
                if form.is_valid():
                    piece = form.save()
                    context = self._get_context(
                        payload, local_context=dict(piece=piece))
                    response = render(
                        request, f'{self.template_name}#table_row', context)
                    return toast("BlueprintSimpleModel added!", response)
                else:
                    response = HttpResponse("Invalid Data", status=400)
                    return toast(
                        form.errors.as_text() or "Invalid data",
                        response,
                        title="Error",
                        variant="danger"
                    )
            case _:
                return HttpResponseBadRequest()

    def put(self, request, pk):
        payload = extract_payload(request)
        match payload.pop('action', ''):
            case 'simple-update':
                instance = get_object_or_404(BlueprintSimpleModel, pk=pk)
                for field in self.fields:
                    if field in payload:
                        setattr(instance, field, payload[field])
                instance.save()
                context = self._get_context(
                    payload, local_context=dict(piece=instance))
                response = render(
                    request, f'{self.template_name}#table_row', context)
                
                return toast("Changes saved.", response, title="Updated")
            case _:
                return HttpResponseBadRequest()

    def delete(self, request, pk):
        payload = extract_payload(request)
        match payload.pop('action', ''):
            case 'simple-delete':
                BlueprintSimpleModel.objects.filter(pk=pk).delete()
                response = HttpResponse("")
                return toast()
            case _:
                return HttpResponseBadRequest()