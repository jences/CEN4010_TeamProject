# Generated by Django 4.2.2 on 2023-06-14 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0002_publisher_user_remove_book_id_book_copiessold_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='ibsn',
            new_name='isbn',
        ),
    ]
