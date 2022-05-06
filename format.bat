@REM Execute this file to setup new clean project
rmdir /s /q orgadmin\migrations
rmdir /s /q professor\migrations
rmdir /s /q speaker\migrations
rmdir /s /q worker\migrations

del db.sqlite3

pip install -r requirements.txt

python manage.py makemigrations orgadmin professor speaker worker
python manage.py migrate
python manage.py loaddata audioan/fixtures/db.json