from django.db import models


class BlueprintSimpleModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Blueprint Simple Model'


class BlueprintChildModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = 'Blueprint Child Model'