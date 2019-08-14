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
Apliciraj migracije
```
$ python manage.py migrate
```
Zaženi strežnik
```
$ python manage.py runserver
```
