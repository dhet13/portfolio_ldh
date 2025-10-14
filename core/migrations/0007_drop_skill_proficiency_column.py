from django.db import migrations


def drop_proficiency(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    cursor.execute("PRAGMA table_info('core_skill');")
    columns = [row[1] for row in cursor.fetchall()]
    if 'proficiency' in columns:
        cursor.execute("ALTER TABLE core_skill DROP COLUMN proficiency;")


def restore_proficiency(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    cursor.execute("PRAGMA table_info('core_skill');")
    columns = [row[1] for row in cursor.fetchall()]
    if 'proficiency' not in columns:
        cursor.execute(
            "ALTER TABLE core_skill ADD COLUMN proficiency REAL NOT NULL DEFAULT 0.0;"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_experience_company_intro_and_more"),
    ]

    operations = [
        migrations.RunPython(drop_proficiency, restore_proficiency),
    ]
