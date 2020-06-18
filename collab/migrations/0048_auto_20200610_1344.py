# Generated by Django 3.0.7 on 2020-06-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0047_auto_20200610_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiences',
            name='missionThemis',
            field=models.BooleanField(default=True, help_text="Est-ce que c'est une mission réalisé chez Thémis ou en dehors ?"),
        ),
        migrations.AlterField(
            model_name='projet',
            name='projetThemis',
            field=models.BooleanField(default=True, help_text="Est-ce que c'est un projet réalisé chez Thémis ou en dehors ?"),
        ),
    ]