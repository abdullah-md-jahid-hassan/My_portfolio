import os
import django
import sys
from django.core.management import call_command

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_portfolio.settings")
django.setup()

def dump_database_to_json(output_file="db_backup/db_backup.json"):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            call_command("dumpdata", indent=2, stdout=f)
        print(f"✅ Database successfully dumped to '{output_file}'")
    except Exception as e:
        print(f"❌ Error dumping database: {e}", file=sys.stderr)

if __name__ == "__main__":
    dump_database_to_json()
