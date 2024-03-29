# Generated by Django 5.0.2 on 2024-02-28 22:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_learning', '0002_alter_product_students_teacher'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgroup',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='groups', to='product_learning.student', verbose_name='Студенты в группе'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='product_learning.product', verbose_name='Продукт урока'),
        ),
        migrations.AlterField(
            model_name='product',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product_learning.teacher', verbose_name='Создатель продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='products', to='product_learning.student', verbose_name='Студенты курса'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
