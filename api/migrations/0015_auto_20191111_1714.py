# Generated by Django 2.2 on 2019-11-11 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20191111_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_pos',
            name='direccion',
            field=models.CharField(max_length=300),
        ),
    ]