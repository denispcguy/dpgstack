import factory
from .models import BlueprintSimpleModel


class BlueprintSimpleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlueprintSimpleModel

    name = factory.Sequence(lambda n: f'obj-{n}-{uuid.uuid4().hex[:6]}')
    description = factory.Faker('paragraph', nb_sentences=3)