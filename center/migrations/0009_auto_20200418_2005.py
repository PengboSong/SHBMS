# Generated by Django 3.0.3 on 2020-04-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0008_auto_20200414_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='school',
            field=models.IntegerField(choices=[(1, '四平路校区'), (2, '嘉定校区'), (3, '闵行校区')], default=1),
        ),
    ]