# Generated by Django 3.1.4 on 2020-12-02 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20201202_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='computed_mark',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grade',
            name='total_mark',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
