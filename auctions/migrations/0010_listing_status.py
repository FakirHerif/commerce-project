# Generated by Django 4.2.4 on 2023-08-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_bid_bidder_bid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('closed', 'Closed'), ('ended', 'Ended')], default='active', max_length=10),
        ),
    ]