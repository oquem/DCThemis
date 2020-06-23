# Generated by Django 3.0.7 on 2020-06-22 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collab', '0062_auto_20200618_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiences',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='collab.client'),
        ),
        migrations.AlterField(
            model_name='experiences',
            name='projetDeLaMission',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='collab.projet', verbose_name='Projet de la mission'),
        ),
    ]