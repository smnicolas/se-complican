# Generated by Django 3.0.5 on 2020-05-17 21:52

from django.db import migrations

from enunciados.migrations.utils.math_delimiters import convert_math_delimiters_to_dollar_signs
from enunciados.models import get_sentinel_user


def replace_math_delimiters(apps, schema):
    Posteo = apps.get_model('enunciados', 'Posteo')
    VersionTexto = apps.get_model('enunciados', 'VersionTexto')
    User = apps.get_model('auth', 'User')
    for posteo in Posteo.objects.all():
        texto_original = posteo.versiones.first().texto
        nuevo_texto = convert_math_delimiters_to_dollar_signs(texto_original)
        autor = User.objects.get(username='Eliminado')
        VersionTexto.versiones.create(texto=nuevo_texto, posteo=posteo, autor=autor)


class Migration(migrations.Migration):
    dependencies = [
        ('enunciados', '0032_auto_20200502_1657'),
    ]

    operations = [
        migrations.RunPython(replace_math_delimiters)
    ]
