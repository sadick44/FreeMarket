# Generated by Django 4.1.3 on 2023-02-07 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_search_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavoritePost',
        ),
    ]
