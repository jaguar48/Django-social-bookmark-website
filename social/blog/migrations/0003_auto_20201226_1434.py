# Generated by Django 3.0.11 on 2020-12-26 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20201226_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categoriess'},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='sections',
        ),
    ]
