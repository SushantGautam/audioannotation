rm -r orgadmin/migrations
rm -r professor/migrations
rm -r speaker/migrations
rm -r worker/migrations

rm db.sqlite3

pip install -r requirements.txt

python manage.py makemigrations orgadmin professor speaker worker
python manage.py migrate
python manage.py loaddata audioan/fixtures/db.json