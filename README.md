# coopmaster-nest-watcher  
- propojuje data ziskana z hniz s home assistantem

## funkcionalita
- komponenta ziskava informace o stavu jednotlivych hnizd,
- data uklada do relacni databaze
- v pravidelnych intervalech informuje obsluhu o stavu snuzky pomoci MQTT clienta

## algoritmus
- offline system predpoklada nasledujici scenar 
1) od 0:00 do 8:30 se v hnizdech nedeje nic
2) v 8:30 se vaha zatizi hmotnosti 2000 g
3) v 9:00 se vaha odhlehci na hmonost 55 gramu
4) v 13:30 se vaha zatizi na 2055 gramu
5) v 14:00 se vaha odhledhci na hmotnost 115 gramu
6) v 15:00 se vaha zatizi na 2115 gramu
7) v 15:03 se ohledci na 115 gramu
8) v 18:00 se vaha odlehci na 0 gramu

System sleduje hmostnost na hnizde v pravidelnych intervalech a uklada je do relacni DB
Nasledne je schopen z casove rady zaznamenaných hmotností detekovat nasledujici data
- slepice si sedla
- slepice snesla vejce (slepice přišla s vejcem a odešla lehší takže na váze něco zůstalo)
- slepice snesla vejce do hnizda, ktere uz vejce melo 
- babicka vybrala vajicka
- slepcice vlezla do hnizda ale vejce nesesla.
Aplikace vyčkává a když to vypadá že jsou hnízda prázdná, tak provede reset aby se snížila rozdíl v chybě která vzniká průhybem hliníkového profilu který je měřen tenzometrickým čidlem



## technologie
- python
- postgress databaze
- Docker
- MQTT client

# Seznam knihoven

- **Flask** – Mikroframework pro Python, který umožňuje rychlý vývoj webových aplikací.
- **colorama** – Knihovna pro snadné používání barev v konzolových výstupech.
- **waitress** – WSGI server pro nasazení Python webových aplikací.
- **requests** – Knihovna pro jednoduché a pohodlné provádění HTTP požadavků.
- **psycopg-binary** – Knihovna pro připojení k PostgreSQL databázi s binárními soubory.
- **psycopg** – Knihovna pro připojení k PostgreSQL databázi pro Python.
- **python-dotenv** – Knihovna pro načítání konfigurací a proměnných prostředí z `.env` souboru.
- **SQLAlchemy** – ORM (Object-Relational Mapper) pro práci s databázemi v Pythonu.
- **APScheduler** – Knihovna pro plánování a spouštění úloh v Pythonu.
- **paho-mqtt** – Knihovna pro implementaci MQTT protokolu pro komunikaci mezi zařízeními.
- **matplotlib** – Knihovna pro vizualizaci dat ve formě grafů a diagramů.
- **numpy** – Knihovna pro efektivní práci s numerickými daty a multidimenzionálními poli.


## hardware
- nuc 

 
