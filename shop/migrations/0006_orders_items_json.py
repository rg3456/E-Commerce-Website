# Generated by Django 2.2.3 on 2019-08-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20190815_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='items_json',
            field=models.CharField(default='', max_length=5000),
        ),
    ]