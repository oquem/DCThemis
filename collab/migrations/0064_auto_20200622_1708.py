# Generated by Django 3.0.7 on 2020-06-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0063_auto_20200622_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborateurs',
            name='grade',
            field=models.CharField(blank=True, choices=[('1', 'Consultant Junior'), ('2', 'Consultant'), ('3', 'Consultant Sénior'), ('4', 'Runner Manager'), ('5', 'Runner Manager'), ('5', 'Directeur')], default='1', max_length=1, null=True),
        ),
    ]