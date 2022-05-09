# Generated by Django 3.2.11 on 2022-05-09 01:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_announcement_estimate_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estimate',
            name='board',
        ),
        migrations.AddField(
            model_name='estimate',
            name='comment',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='board.comment'),
            preserve_default=False,
        ),
    ]
