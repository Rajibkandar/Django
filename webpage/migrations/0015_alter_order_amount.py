# Generated by Django 4.0.3 on 2022-05-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0014_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
