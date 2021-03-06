# Generated by Django 2.1.1 on 2018-10-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('created', models.DateField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=255)),
                ('followers', models.IntegerField()),
                ('repos', models.IntegerField()),
                ('score', models.FloatField()),
                ('avatar', models.ImageField(null=True, upload_to='avatar')),
                ('type', models.CharField(choices=[('org', 'organization'), ('user', 'user')], max_length=3)),
            ],
        ),
    ]
