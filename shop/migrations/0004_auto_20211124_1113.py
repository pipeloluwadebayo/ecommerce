# Generated by Django 3.2.9 on 2021-11-24 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211122_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
