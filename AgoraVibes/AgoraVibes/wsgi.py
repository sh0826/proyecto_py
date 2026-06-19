"""
WSGI config for AgoraVibes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgoraVibes.settings')

application = get_wsgi_application()

from django.conf import settings
from django.db import connection

_db = settings.DATABASES['default']
_engine = _db.get('ENGINE', '')

if 'postgresql' in _engine:
    print(
        f"[AgoraVibes] Base de datos activa: PostgreSQL "
        f"({_db.get('HOST')}:{_db.get('PORT')}/{_db.get('NAME')})",
        file=sys.stderr,
    )
else:
    print(
        f"[AgoraVibes] Base de datos activa: SQLite ({_db.get('NAME')})",
        file=sys.stderr,
    )

try:
    with connection.cursor() as cursor:
        if 'postgresql' in _engine:
            cursor.execute('SELECT COUNT(*) FROM "LoginApp_usuario"')
        else:
            cursor.execute('SELECT COUNT(*) FROM LoginApp_usuario')
        _user_count = cursor.fetchone()[0]
    print(f"[AgoraVibes] Usuarios en esta base: {_user_count}", file=sys.stderr)
except Exception as exc:
    print(f"[AgoraVibes] Tabla de usuarios aun no existe: {exc}", file=sys.stderr)
