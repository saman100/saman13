# Generated by Django 3.1.7 on 2021-04-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20210414_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
