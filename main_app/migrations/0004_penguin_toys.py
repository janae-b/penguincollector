# Generated by Django 3.2 on 2021-05-05 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210505_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='penguin',
            name='toys',
            field=models.ManyToManyField(to='main_app.Toy'),
        ),
    ]
