# Generated by Django 3.0.3 on 2020-03-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0004_auto_20200302_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='school_num',
            field=models.IntegerField(max_length=7),
        ),
    ]
