## Auswertungsskript für Spätfrost 
> Quick and Dirty Auswertungsskript
#### 1. Umgebung installieren 
Conda Umgebung aus dem bestehenden Conda-file: 
```bash
conda env create -f environment.yml
```
mehr Infos [hier](conda env create -f environment.yml)

#### 2. Filestruktur 
- 1 Ordner für Inputfiles, in dem nur die Inputfiles mit Endung nc liegen
- 1 Ordner für die Outputfiles, der kann sich auch in dem Ordner für die Inputfiles befinden.
- Pfade im Skript angeben (aktuelle Pfade ersetzen)

#### 3. Skript ausführen
- Skript mit Python ausführen:
  ```bash
  python get_number_of_frostdays.py
  ```
