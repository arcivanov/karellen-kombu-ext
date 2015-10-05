# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151005181923 on 2015-10-05 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(db_index=True, default=True)),
                ('sent_at', models.DateTimeField(
                    auto_now_add=True, db_index=True, null=True)),
                ('payload', models.TextField(verbose_name='payload')),
            ],
            options={
                'db_table': 'djkombu_message',
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('name', models.CharField(
                    max_length=200, unique=True, verbose_name='name')),
            ],
            options={
                'db_table': 'djkombu_queue',
                'verbose_name': 'queue',
                'verbose_name_plural': 'queues',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='queue',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='messages',
                to='kombu_transport_django.Queue'),
        ),
    ]
