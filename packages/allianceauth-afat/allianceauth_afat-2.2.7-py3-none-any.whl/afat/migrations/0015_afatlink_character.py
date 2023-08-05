# Generated by Django 3.1.4 on 2020-12-26 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eveonline", "0012_index_additions"),
        ("afat", "0014_auto_20201224_0930"),
    ]

    operations = [
        migrations.AddField(
            model_name="afatlink",
            name="character",
            field=models.ForeignKey(
                default=None,
                help_text="Character this fatlink has been created with",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="eveonline.evecharacter",
            ),
        ),
    ]
