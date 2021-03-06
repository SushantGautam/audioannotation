# Generated by Django 3.2.13 on 2022-04-20 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0002_question_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submissions',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='submissions',
            name='sound_file',
            field=models.FileField(upload_to='media/question_audio/'),
        ),
    ]
