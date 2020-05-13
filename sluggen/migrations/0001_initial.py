# Generated by Django 2.2.4 on 2020-05-13 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=6, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consumed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'slug',
            },
        ),
    ]
