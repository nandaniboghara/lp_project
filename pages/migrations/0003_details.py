# Generated by Django 3.0.8 on 2021-04-25 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_remove_bank_bank_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('interest', models.CharField(max_length=200)),
                ('fees', models.CharField(max_length=200)),
            ],
        ),
    ]
