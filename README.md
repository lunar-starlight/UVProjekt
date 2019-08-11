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
Namesti docker in docker-compose.
```
python3 -m venv venv3      # neobvezno
source venv3/bin/activate  # neobvezno
pip install docker-compose
```
Zgradi sliko in dodaj administratorski račun
```
docker-compose build
docker-compose run web ./manage.py createsuperuser
```
Zaženi strežnik
```
docker-compose up --build 
```
### Venv
Namesti postgresql.

Arch Linux:
```
$ pacman -S postgresql
```
Debian:
```
$ apt install postgresql postgresql-client
```

Naredi virtualno okolje in ga aktiviraj
```
python3 -m venv venv3
source venv3/bin/activate
```
Namesti potrebne pakete
```
pip install -r requirements.txt
```
Apliciraj migracije
```
python manage.py migrate
```
Zaženi strežnik
```
python manage.py runserver
```
