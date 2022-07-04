# Generated by Django 4.0.5 on 2022-07-04 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_review_blog_alter_review_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.blog'),
        ),
        migrations.AlterField(
            model_name='review',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.course'),
        ),
    ]