# Generated by Django 4.1.1 on 2022-09-22 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal_blog', '0004_rename_message_contact_messages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='messages',
            new_name='message',
        ),
    ]
