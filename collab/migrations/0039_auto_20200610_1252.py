# Generated by Django 3.0.7 on 2020-06-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0038_projet_projetthemis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiences',
            name='environnementMission',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
