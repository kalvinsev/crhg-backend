# Generated by Django 5.1.2 on 2024-12-20 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crhg', '0002_alter_edge_edge_id_alter_node_node_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edge',
            name='edge_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='node',
            name='node_id',
            field=models.CharField(max_length=50),
        ),
    ]