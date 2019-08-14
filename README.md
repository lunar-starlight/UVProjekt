Projekt pri predmetu UVP na fakulteti za matematiko in fiziko
===========================================

Navodila za razvijalce
----------------------
Prenesi repozitorij ali naredi fork
```
git clone git@github.com:StrahR/UVProjekt.git
```
Okolje lahko postavimo na dva načina; priporočeno je z uporabo Dockerja, vendar je tudi mogoče brez.

_Opomba: 2. način ni testiran, uporaba na lastno odgovornost._

### Docker

Namesti `docker-compose`.

Arch Linux:
```
# pacman -S docker-compose
```

Dodaj svojega uporabnika v skupino `docker` in zaženi
```
$ newgrp docker
```

Zgradi sliko, poženi migracije, in dodaj administratorski ter AI račun
```
$ docker-compose build
$ docker-compose run web ./manage.py migrate
$ docker-compose run web ./manage.py createsuperuser --username admin
$ docker-compose run web ./manage.py createsuperuser --username ai
```
AI računu je priporočljivo onemogočiti prijavo, tako da nastaviš `is_active` na `False`.

Zaženi strežnik
```
$ docker-compose up
```
### Venv
Namesti postgresql.

Arch Linux:
```
# pacman -S postgresql
[postgres]$ initdb -D /var/lib/postgres/data
# systemctl start postgresql
[postgres]$ createuser strah -ds
[postgres]$ createdb strah-db -O strah
```
Popravi nastavitev za bazo podatkov tako:
```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'strah-db',
        'USER': 'strah',
        'HOST': 'localhost',
        'PORT': ''
    }
}
```


Naredi virtualno okolje in ga aktiviraj
```
$ python3 -m venv venv3
$ source venv3/bin/activate
```
Namesti potrebne pakete
```
$ pip install -r requirements.txt
```
Apliciraj migracije in naredi potrebne administratorske račune
```
$ python manage.py migrate
$ python manage.py createsuperuser --username admin
$ python manage.py createsuperuser --username ai
```
AI računu je priporočljivo onemogočiti prijavo, tako da nastaviš `is_active` na `False`.

Zaženi strežnik
```
$ python manage.py runserver
```
