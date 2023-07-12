# Generated by Django 4.2.3 on 2023-07-11 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='bookstore_app.book')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='bookstore_app.cart')),
            ],
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='carts', through='bookstore_app.CartItem', to='bookstore_app.book'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('item', 'cart'), name='unique_item_cart'),
        ),
    ]
