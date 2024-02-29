DRF API изучение продкутов

Запуск и установка:

```sh
cd <папка_проекта>
virtualenv env
./env/Scripts/Activate.ps1
pip install -r requirements.txt
python ./src/manage.py makemigrations
python ./src/manage.py migrate
python ./src/manage.py runserver
```


localhost:8000/swagger/
localhost:8000/admin/