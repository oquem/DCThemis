# Generated by Django 3.0.7 on 2020-06-10 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0049_auto_20200610_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborateurs',
            name='trigramme',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
