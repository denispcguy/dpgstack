import json
import pytest
from django.urls import reverse
from apps._blueprint import factories as f
from apps._blueprint import models as m
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.test import Client
from django.http import HttpResponse
from apps._blueprint.models import BlueprintSimpleModel

pytestmark = [pytest.mark.django_db]


class TestTableView:
    url = reverse('_blueprint:table')

    def url_detail(self, pk):
        return reverse('_blueprint:table_detail', args=[pk])

    @pytest.fixture(autouse=True)
    def pieces(self):
        p = f.BlueprintSimpleModelFactory.create_batch(22)
        assert len(set([piece.id for piece in p])) == 22
        return p

    @pytest.fixture
    def client(self, client: Client, htmx=True) -> Client:
        username = 'testuser'
        password = 'testpassword123'
        user = User.objects.create_user(
            username=username,
            password=password
        )
        client.login(
            username=username,
            password=password
        )
        if htmx:
            client.defaults['HTTP_HX_REQUEST'] = 'true'
        return client

    def test_get_no_action_pagination(self, client: Client, pieces):
        action = ''

        payload = dict(action=action, page='1')
        r = client.get(self.url, data=payload, htmx=False)
        r_qs = r.context['queryset']
        assert len(r_qs) == 8
        assert pieces[0:8] == r_qs

        payload = dict(action=action, page='2')
        r = client.get(self.url, data=payload, htmx=False)
        r_qs = r.context['queryset']
        assert len(r_qs) == 8
        assert pieces[8:16] == r_qs

        payload = dict(action=action, page='999')
        r = client.get(self.url, data=payload, htmx=False)
        r_qs = r.context['queryset']
        assert len(r_qs) == 6
        assert pieces[-6:] == r_qs

    def test_get_no_action_qs_is_ordered_by_id(self, client: Client, pieces):
        action = ''
        payload = dict(action=action)
        r: HttpResponse = client.get(self.url, data=payload)
        assert r.status_code == 200
        r_qs = r.context['queryset']
        assert pieces[0] == r_qs[0]

    def test_get_normal_row(self, client: Client):
        action = 'normal-row'
        payload = dict(action=action)
        r: HttpResponse = client.get(self.url_detail(1), data=payload)
        assert r.status_code == 200
        assert r.context['piece'] == BlueprintSimpleModel.objects.get(pk=1)
        assert r.context.get('form')

    def test_get_edit_row(self, client: Client):
        action = 'edit-row'
        payload = dict(action=action)
        r: HttpResponse = client.get(self.url_detail(1), data=payload)
        assert r.status_code == 200
        assert r.context['piece'] == BlueprintSimpleModel.objects.get(pk=1)
        assert r.context.get('form')

    def test_get_error_wrong_action(self, client):
        action = 'wrong1221421412412'
        payload = dict(action=action)
        r: HttpResponse = client.get(self.url, data=payload)
        assert r.status_code == 400

    def test_post_no_action(self, client: Client):
        action = ''
        payload = dict(action=action)
        r: HttpResponse = client.post(self.url, data=payload)
        assert r.status_code == 400

    def test_post_accept_form(self, client: Client):
        action = 'accept-form'
        name = 'New BlueprintSimpleModel'
        payload = dict(action=action, name=name, description='A description')
        r: HttpResponse = client.post(self.url, data=payload)
        assert r.status_code == 200
        trigger_data = json.loads(r.headers['HX-Trigger'])
        assert trigger_data['notify']['variant'] == 'success'
        assert BlueprintSimpleModel.objects.filter(name=name).exists()

    def test_post_accept_form_invalid_form(self, client):
        action = 'accept-form'
        payload = dict(action=action, nameasfsaf='wrong-field')
        r: HttpResponse = client.post(self.url, data=payload)
        assert r.status_code == 400
        trigger_data = json.loads(r.headers['HX-Trigger'])
        assert trigger_data['notify']['variant'] == 'danger'

    def test_put_no_action(self, client):
        action = ''
        payload = urlencode(dict(action=action))
        r: HttpResponse = client.put(
            self.url_detail(1),
            data=payload,
            content_type='application/x-www-form-urlencoded',
        )
        assert r.status_code == 400

    def test_put_simple_update(self, client):
        action = 'simple-update'
        piece = BlueprintSimpleModel.objects.get(pk=1)
        piece.name = 'Old Name'
        piece.save()

        payload = urlencode(dict(action=action, name='New Name'))
        r: HttpResponse = client.put(
            self.url_detail(1),
            data=payload,
            content_type='application/x-www-form-urlencoded',
        )
        assert r.status_code == 200
        piece.refresh_from_db()
        assert piece.name == 'New Name'
        trigger_data = json.loads(r.headers['HX-Trigger'])
        assert trigger_data['notify']['variant'] == 'success'

    def test_put_simple_update_ignores_unknown_fields(self, client):
        action = 'simple-update'
        payload = urlencode(dict(action=action, names='non existent key'))
        r: HttpResponse = client.put(
            self.url_detail(1),
            data=payload,
            content_type='application/x-www-form-urlencoded',
        )
        assert r.status_code == 200
        trigger_data = json.loads(r.headers['HX-Trigger'])
        assert trigger_data['notify']['variant'] == 'success'

    def test_delete_simple_delete(self, client):
        action = 'simple-delete'
        payload = urlencode(dict(action=action))
        assert BlueprintSimpleModel.objects.filter(pk=1).exists()
        r: HttpResponse = client.delete(
            self.url_detail(1),
            data=payload,
            content_type='application/x-www-form-urlencoded',
        )
        assert r.status_code == 200
        assert not BlueprintSimpleModel.objects.filter(pk=1).exists()
        trigger_data = json.loads(r.headers['HX-Trigger'])
        assert trigger_data['notify']['variant'] == 'success'

    def test_delete_no_action(self, client):
        action = ''
        payload = urlencode(dict(action=action))
        r: HttpResponse = client.delete(
            self.url_detail(1),
            data=payload,
            content_type='application/x-www-form-urlencoded',
        )
        assert r.status_code == 400