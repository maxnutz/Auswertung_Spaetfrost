## Auswertungsskript für Spätfrost 
> Quick and Dirty Auswertungsskript zur Angabe von Spätfrosttagen über ein beliebiges Raster, definiert durch die Inputvariablen. Default Auswertungszeitraum doy 90 to doy 110.

#### 1. Umgebung installieren 
Conda Umgebung aus dem bestehenden Conda-file: 
```bash
conda env create -f environment.yml
```
umfassende Doku [hier](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)

#### 2. Filestruktur 
- 1 Ordner für Inputfiles, in dem nur die Inputfiles mit Endung nc liegen
- 1 Ordner für die Outputfiles, der kann sich auch in dem Ordner für die Inputfiles befinden.
- Pfade im Skript angeben (aktuelle Pfade ersetzen)
- Das Skript legt in dem Outputfoder einen folder temp an, in dem die Outputfiles der Rasterdaten gespeichert werden. Der Ordner wird, nachdem alles fertig ist, wieder gelöscht, es kann aber sein, dass beim outputordner die Berechtigungen manuell gesetzt werden müssen. 

#### 3. Skript ausführen
- Skript mit Python ausführen:
  ```bash
  python get_number_of_frostdays.py
  ```
