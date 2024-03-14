# Wurzelbot
Dies ist ein sehr einfacher Bot, um das Anpflanzen im Browserspiel [Wurzelimperium](https://www.wurzelimperium.de/) zu vereinfachen.

## Ausführen
Das Skript kann direkt gestartet werden wenn die Datei ausführbar gemacht worden ist, alternativ kann sie mit einer Python Konsole gestartet werden. Die Optionen erhält man mit `./Wurzelbot.py --help`

## Anwendung
Bevor der Bot ausgeführt wird, muss die Pflanze (oder die Gieskanne) auf ein Startfeld gelegt werden. Die allgemeine Syntax ist `./Wurzelbot.py [num] [time]` Der Bot versteht folgende Optionen, die als Suffix an die Zahl herangefügt werden:

* `r`: Rows, Reihen
* `c`: Columns, Spalten
* `h`: Horizontal
* `v`: Vertikal

Der Zeitparameter gibt an, wie viele Sekunden der Bot pro Feld benötigt. Standardmäßig ist dieser Wert auf `0.01` festgelegt.

Beispielanwendungen:

* Pflanze 204 Felder an: `./Wurzelbot.py`
* Pflanze zwei Reihen an: `./Wurzelbot.py 2r`
* Pflanze 155 Felder vertikal an: `./Wurzelbot.py 155v`
* Pflanze sieben Spalten an und brauche 0.5s pro Feld: `./Wurzelbot.py 7c 0.5`

## Dependencies

* `python >= 3.10`
* `pyautogui`

Der Bot steuert die Mausbewegung mit `pyautogui`. Diese kann wiefolgt installiert werden: `pip3 install pyautogui`