# Generated by Django 5.0.6 on 2024-06-21 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='text',
            field=models.TextField(),
        ),
    ]