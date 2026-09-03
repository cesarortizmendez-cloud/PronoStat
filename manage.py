#!/usr/bin/env python
"""PronoStat — Django management utility."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostat.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("No se encontró Django. Instala: pip install -r requirements.txt") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
