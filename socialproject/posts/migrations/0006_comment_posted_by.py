# Generated by Django 5.0.4 on 2024-04-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted_by',
            field=models.CharField(default='romina', max_length=100),
            preserve_default=False,
        ),
    ]
