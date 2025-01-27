# Generated by Django 5.0.4 on 2024-04-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studenthelp', '0007_alter_like_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='specific_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='form_type',
            field=models.CharField(choices=[('stage', 'Stage Form'), ('housing', 'Housing Form'), ('transportation', 'Transportation Form'), ('club_event', 'Club Event Form'), ('social_event', 'Social Event Form')], default='stage', max_length=20),
        ),
    ]
