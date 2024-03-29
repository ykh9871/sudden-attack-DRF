# Generated by Django 4.2.11 on 2024-03-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='modified_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='modified_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='role',
            field=models.CharField(choices=[('M', 'M'), ('A', 'A'), ('P', 'P')], default='P', max_length=20),
        ),
    ]