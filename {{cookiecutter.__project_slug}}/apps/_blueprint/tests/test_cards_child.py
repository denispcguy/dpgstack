import pytest
from django.urls import reverse
from apps._blueprint import factories as f
from django.contrib.auth.models import User
from django.test import Client
from django.http import HttpResponse

pytestmark = [pytest.mark.django_db]


class TestCardsChildView:
    url = reverse('_blueprint:cards_child')

    @pytest.fixture(autouse=True)
    def pieces(self):
        p = f.BlueprintSimpleModelFactory.create_batch(5)
        p = sorted(p, key=lambda x: x.id)
        assert len(set([piece.id for piece in p])) == 5
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

    def test_get_returns_200(self, client: Client):
        r: HttpResponse = client.get(self.url)
        assert r.status_code == 200

    def test_get_context_has_queryset(self, client: Client, pieces):
        r: HttpResponse = client.get(self.url)
        r_qs = r.context['queryset']
        assert len(r_qs) == len(pieces)
        assert list(r_qs.order_by('id')) == pieces

    def test_get_context_has_fields(self, client: Client):
        r: HttpResponse = client.get(self.url)
        assert r.context['fields'] == ['name', 'description']