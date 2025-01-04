# coopmaster-nest-watcher  
- propojuje data ziskana z hniz s home assistantem

## funkcionalita
- komponenta ziskava informace o stavu jednotlivych hnizd, 
- data uklada do relacni databaze
- v pravidelnych intervalech informuje obsluhu o stavu snuzky

## algoritmus
- system predpoklada nasledujici scenar 
1) od 0:00 do 8:30 se v hnizdech nedeje nic
2) v 8:30 se vaha zatizi hmotnosti 2000 g
3) v 9:00 se vaha odhlehci na hmonost 55 gramu
4) v 13:30 se vaha zatizi na 2055 gramu
5) v 14:00 se vaha odhledhci na hmotnost 115 gramu
6) v 15:00 se vaha zatizi na 2115 gramu
7) v 15:03 se ohledci na 115 gramu
8) v 18:00 se vaha odlehci na 0 gramu
System sleduje hmostnost na hnizde v pravidelnych intervalech a uklada je do relacni DB

Nasledne je schopen z casove ready detekovat nasledujici data
- slepice si sedla
- slepice snesla vejce
- slepice snesla vejce do hnizda, ktere uz vejce melo 
- babicka vybrala vajicka
- slepcice vlezla do hnizda ale vejce nesesla.



## technologie
- python
- postgress databaze
- Docker

## hardware
- rabspery 

 
