# Generated by Django 3.0.5 on 2020-05-02 17:24

from django.db import migrations
import enunciados.tests.models.fields.non_zero_positive_integer_field


class Migration(migrations.Migration):

    dependencies = [
        ('enunciados', '0030_conjuntodeenunciados_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enunciado',
            name='numero',
            field=enunciados.tests.models.fields.non_zero_positive_integer_field.NonZeroPositiveIntegerField(),
        ),
    ]
