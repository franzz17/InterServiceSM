# Cómo solucionar el error "relation 'django_session' does not exist"

Has encontrado un error común cuando se trabaja con Django y una base de datos PostgreSQL existente. Django espera que ciertas tablas del sistema existan, incluyendo `django_session` que es necesaria para el manejo de sesiones de usuario.

## Solución 1: Usando el script proporcionado

He creado un script Python para solucionar este problema específico:

1. Abre una terminal (cmd) en la carpeta del proyecto
2. Asegúrate de tener activado el entorno virtual:
   ```
   venv\Scripts\activate
   ```
3. Instala psycopg2 si aún no lo tienes:
   ```
   pip install psycopg2-binary
   ```
4. Ejecuta el script:
   ```
   python solve_session_error.py
   ```
5. Cuando el script termine, ejecuta:
   ```
   python manage.py migrate --fake-initial
   ```
6. Reinicia el servidor Django:
   ```
   python manage.py runserver
   ```

## Solución 2: Ejecutar el SQL directamente

Si prefieres ejecutar SQL directamente:

1. Conéctate a tu base de datos PostgreSQL:
   ```
   psql -h confidently-nifty-skylark.data-1.use1.tembo.io -U postgres -d postgres
   ```
2. Introduce la contraseña cuando se solicite
3. Ejecuta el siguiente SQL:
   ```sql
   CREATE TABLE IF NOT EXISTS django_session (
       session_key VARCHAR(40) NOT NULL PRIMARY KEY,
       session_data TEXT NOT NULL,
       expire_date TIMESTAMP WITH TIME ZONE NOT NULL
   );
   CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session(expire_date);
   ```
4. Sal de psql con `\q`
5. Ejecuta las migraciones de Django:
   ```
   python manage.py migrate --fake-initial
   ```
6. Reinicia el servidor

## Solución 3: Crear todas las tablas del sistema de Django

Para una solución más completa, puedes crear todas las tablas del sistema de Django ejecutando:

```
psql -h confidently-nifty-skylark.data-1.use1.tembo.io -U postgres -d postgres -f create_django_tables.sql
```

Y luego:

```
python manage.py migrate --fake-initial
```

## Explicación del Problema

Este error ocurre porque estás utilizando características de Django que requieren sesiones (como autenticación), pero la tabla `django_session` no existe en tu base de datos. Esto sucede habitualmente cuando:

1. Se conecta Django a una base de datos existente que no fue creada por Django
2. Se omitieron las migraciones iniciales de Django al configurar el proyecto
3. Se usa `--fake` en las migraciones sin que existan las tablas del sistema

## Previniendo este problema en el futuro

Cuando trabajes con bases de datos existentes y Django:

1. Asegúrate de ejecutar `python manage.py migrate` al inicio del proyecto (sin `--fake` la primera vez)
2. Si necesitas usar `--fake`, asegúrate de que las tablas del sistema ya existen
3. Considera usar `inspectdb` para generar modelos a partir de tablas existentes
