# Generated by Django 2.2.5 on 2019-09-04 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20190904_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='mines_left',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
