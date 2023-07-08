# "ReprintReceiptApp"

## Übersicht 
Diese App ermöglicht es Ihnen, den Druckprozess auszulösen, indem Sie den letzten Beleg erneut drucken. Sie bietet die Möglichkeit, die Anzahl der Drucke über Befehlszeilenargumente oder die .env-Datei anzugeben.

## Voraussetzungen
Bevor Sie die App verwenden, stellen Sie sicher, dass Sie die folgenden Voraussetzungen erfüllen:

- Python ist auf Ihrem System installiert.
- Die erforderlichen Pakete sind installiert. Sie können die erforderlichen Pakete mit folgendem Befehl installieren:

pip install requirements.txt

## Erste Schritte
Um die App zu verwenden, befolgen Sie diese Schritte:

1. Laden Sie den Code herunter oder kopieren Sie ihn in eine Python-Datei (z. B. print_app.py).

2. Öffnen Sie ein Terminal oder die Eingabeaufforderung und navigieren Sie zum Verzeichnis, das die Python-Datei enthält.

3. Führen Sie die Python-Datei mit folgendem Befehl aus:

python print_app.py [num_prints]
* Ersetzen Sie [num_prints] durch die gewünschte Anzahl der Wiederholungen des letzten Belegs. Dieses Argument ist optional. Wenn es nicht angegeben wird, verwendet die App den Wert aus der .env-Datei oder den Standardwert.

4. Die App löst den Druckprozess aus und liefert Informationen über den Erfolg oder Misserfolg jeder Druckoperation.

## Konfiguration
Die App unterstützt die Konfiguration über die folgenden Methoden:

### Umgebungsvariablen
Die App verwendet Umgebungsvariablen zur Konfiguration. Sie können die folgenden Umgebungsvariablen festlegen:

- SERVER_IP: Gibt die IP-Adresse des Servers an. Wenn nicht festgelegt, verwendet die App den Standardwert "localhost".
- NUM_PRINTS: Gibt die Standardanzahl der Wiederholungen des letzten Belegs an. Wenn nicht festgelegt, verwendet die App den Standardwert.
### .env-Datei
Wenn sich die .env-Datei im selben Verzeichnis wie die Python-Datei befindet, lädt die App die Umgebungsvariablen daraus. Wenn die Datei nicht vorhanden ist, wird eine Standard-.env-Datei mit der Standardkonfiguration erstellt.

Um die Konfiguration anzupassen, erstellen oder ändern Sie die .env-Datei mit einem Texteditor. Legen Sie die Umgebungsvariablen im Format SCHLÜSSEL=WERT fest, wobei jede Variable in einer separaten Zeile steht. Beispiel:

- SERVER_IP=192.168.0.1
- NUM_PRINTS=3

## Ausgabe
Die App generiert die folgenden Ausgabedateien:

- README.MD: Enthält Informationen über die App und ihre Funktionalität.
- printing_reports.txt: Speichert einen Protokoll der Druckvorgänge, einschließlich Erfolgs- und Fehlermeldungen für jede Druckoperation.

## Fehlerbehandlung
Wenn während der Ausführung der App ein Fehler auftritt, werden Fehlermeldungen im Terminal oder in der Eingabeaufforderung angezeigt. Zusätzlich werden detaillierte Fehlerinformationen an die Datei printing_reports.txt angehängt.

## Beispielverwendung
Hier sind einige Beispiele zur Verwendung der App:

- Drücken Sie den Druckprozess aus und drucken Sie den letzten Beleg einmal erneut:

python print_app.py

- Drücken Sie den Druckprozess aus und drucken Sie den letzten Beleg dreimal erneut:

python print_app.py 3

Anpassung der Standardanzahl der Drucke mit der .env-Datei:
1. Erstellen Sie eine Datei namens .env im selben Verzeichnis wie die Python-Datei.

2. Öffnen Sie die .env-Datei mit einem Texteditor.

3. Legen Sie die Variable NUM_PRINTS auf den gewünschten Standardwert fest. Beispiel:

### NUM_PRINTS=5
4. Speichern Sie die Datei.

5. Führen Sie die Python-Datei aus, ohne die Anzahl der Drucke als Befehlszeilenargument anzugeben:

python print_app.py

Die App verwendet den in der .env-Datei angegebenen Standardwert.

## Fazit
Mit dieser App können Sie den Druckprozess leicht auslösen, indem Sie den letzten Beleg erneut drucken. Sie bietet Flexibilität bei der Angabe der Anzahl der Wiederholungen und unterstützt die Anpassung über Umgebungsvariablen und die .env-Datei.

## Lizenz
Diese App wird unter den Bedingungen der MIT-Lizenz verteilt. Die MIT-Lizenz ist eine freizügige Open-Source-Lizenz, die es Ihnen ermöglicht, die App zu verwenden, zu modifizieren und zu verteilen, sowohl für kommerzielle als auch für nichtkommerzielle Zwecke. Sie bietet Flexibilität und Freiheit und stellt sicher, dass Sie den ursprünglichen Lizenzhinweis in Kopien oder Derivaten der Software einschließen.
Durch die Verwendung dieser App stimmen Sie den Bedingungen der MIT-Lizenz zu. Bitte beachten Sie die Datei LICENSE für weitere Informationen.
## Bibliotheken von Drittanbietern
Die App kann Drittanbieterbibliotheken oder Abhängigkeiten verwenden, die ihre eigenen Lizenzen haben können. Die Lizenzen für diese Bibliotheken finden Sie in den entsprechenden LICENSE- oder README-Dateien im Quellcode oder in der Dokumentation der Bibliothek. Es ist wichtig, die Lizenzen von Drittanbieterbibliotheken zu überprüfen und einzuhalten, die in Verbindung mit dieser App verwendet werden.
Hinweis: Die vorherige englische Version des README.md bleibt unverändert, und Sie können beide Versionen in Ihrem Projekt verwenden.