# Generated by Django 5.1.2 on 2024-12-12 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default='book_covers/default.png', upload_to='book_covers/'),
        ),
    ]
