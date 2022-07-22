# Generated by Django 3.0.8 on 2022-07-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220719_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(choices=[('food', 'food'), ('beverage', 'beverage'), ('goods', 'goods'), ('health', 'health')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='delivery_cycle_main',
            field=models.CharField(choices=[('weekly', 'weekly'), ('monthly', 'monthly'), ('weekly/monthly', 'weekly/monthly')], max_length=20),
        ),
        migrations.AlterField(
            model_name='type',
            name='type_name',
            field=models.CharField(choices=[('milk', 'milk'), ('shake', 'shake'), ('yogurt', 'yogurt'), ('salad', 'salad'), ('fried-rice', 'fried-rice'), ('cereal', 'cereal'), ('bread', 'bread'), ('chicken', 'chicken'), ('coffee-cold', 'coffee-cold'), ('coffee-beans', 'coffee-beans'), ('coffee-capsule', 'coffee-capsule'), ('tea', 'tea'), ('pad', 'pad'), ('teeth', 'teeth'), ('pack', 'pack'), ('cotton', 'cotton'), ('lens', 'lens'), ('shaver', 'shaver'), ('lacto', 'lacto'), ('supplement', 'supplement'), ('skin-care-pack', 'skin-care-pack'), ('care-pack', 'care-pack'), ('protein', 'protein'), ('collagen', 'collagen')], max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=20),
        ),
    ]
