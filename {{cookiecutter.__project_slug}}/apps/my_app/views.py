from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
import apps.core.utils as utils
from .models import Book
from .forms import BookForm
import json
from django.views import View


class BookView(View):
    template_name = 'my_app/book.html'
    fields = ['title', 'author', 'published_date']

    def _get_context(self, request, **kwargs):
        order_by = request.GET.get('order_by') or 'id'
        queryset = Book.objects.select_related('author').order_by(
            order_by)
        queryset, page_obj = utils.get_paginated_queryset(
            request, queryset, paginate_by=8
        )
        return self._get_context_no_query(
            queryset=queryset,
            page_obj=page_obj,
            **kwargs
        )

    def _get_context_no_query(self, **kwargs):
        context = {
            'fields': self.fields,
            'url_name': 'my_app:book',
            'form': BookForm(),
        }
        context.update(kwargs)
        return context

    def _toast(self, response, message, variant="success", title="Notification", extra_triggers=None):
        trigger_data = {
            "notify": {
                "variant": variant,
                "title": title,
                "message": message
            }
        }
        if extra_triggers:
            trigger_data.update(extra_triggers)
        response['HX-Trigger'] = json.dumps(trigger_data)
        return response

    def get(self, request):
        if request.htmx:
            data = request.GET
            match data.get('action'):
                case 'get-new-page' | 'get-rows-ordered':
                    context = self._get_context(request)
                    return render(request, self.template_name, context)

                case 'get-edit-row':
                    pk = data.get('pk')
                    piece = get_object_or_404(
                        Book, pk=pk)
                    form = BookForm(instance=piece, initial={
                                    'author': piece.author.name})
                    context = self._get_context_no_query(
                        form=form, piece=piece)
                    return render(request, f'{self.template_name}#edit_row', context)

                case 'get-normal-row':
                    piece = get_object_or_404(
                        Book, pk=data.get('pk'))
                    context = self._get_context_no_query(
                        piece=piece)
                    return render(request, f'{self.template_name}#table_row', context)
        else:
            context = self._get_context(request)
            return render(request, self.template_name, context)

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            piece = form.save()
            context = self._get_context_no_query(piece=piece)
            response = render(
                request, f'{self.template_name}#table_row', context)
            return self._toast(response, "Book added!", title="Success")
        else:
            response = HttpResponse("Invalid Data", status=400)
            return self._toast(
                response,
                form.errors.as_text() or "Invalid data",
                title="Error",
                variant="danger"
            )

    def put(self, request):
        pk = request.GET.get('pk')
        instance = get_object_or_404(Book, pk=pk)
        put_data = QueryDict(request.body)
        form = BookForm(put_data, instance=instance)

        if form.is_valid():
            form.save()
            context = self._get_context_no_query(
                piece=instance)
            response = render(
                request, f'{self.template_name}#table_row', context)
            return self._toast(response, "Changes saved.", title="Updated")
        else:
            response = HttpResponse("Invalid Data", status=400)
            return self._toast(
                response,
                form.errors.as_text() or "Invalid data",
                title="Error",
                variant="danger"
            )

    def delete(self, request):
        pk = request.GET.get('pk')
        Book.objects.filter(pk=pk).delete()
        response = HttpResponse("")
        return self._toast(response, "Book deleted.", title="Deleted", variant="success")
