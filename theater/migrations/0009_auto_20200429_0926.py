# Generated by Django 3.0.5 on 2020-04-29 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0008_auto_20200428_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='cine_no',
            field=models.CharField(max_length=5, verbose_name='Cinema Hall'),
        ),
        migrations.AlterField(
            model_name='show',
            name='movie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='theater.Movie'),
        ),
        migrations.AlterField(
            model_name='show',
            name='theatre',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='theater.Theatre'),
        ),
        migrations.AlterField(
            model_name='show',
            name='time',
            field=models.TimeField(verbose_name='Screening time'),
        ),
    ]
