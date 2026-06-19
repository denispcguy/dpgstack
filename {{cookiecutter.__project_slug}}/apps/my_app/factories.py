import factory
from .models import Author, Book
from faker import Faker

fake = Faker()


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=5)
    author = factory.SubFactory(AuthorFactory)
    published_date = factory.Faker('date_this_decade')
