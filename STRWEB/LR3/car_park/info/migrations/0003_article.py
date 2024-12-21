# Generated by Django 5.0.6 on 2024-06-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_vacancy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('summary', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('last_modification_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]