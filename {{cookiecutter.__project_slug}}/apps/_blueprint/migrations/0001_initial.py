from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlueprintSimpleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Blueprint Simple Model',
            },
        ),
        migrations.CreateModel(
            name='BlueprintChildModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='children', to='_blueprint.blueprintsimplemodel')),
            ],
            options={
                'verbose_name': 'Blueprint Child Model',
            },
        ),
    ]