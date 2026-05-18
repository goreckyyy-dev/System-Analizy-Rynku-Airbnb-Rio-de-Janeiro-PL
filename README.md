# System Analizy Rynku Airbnb: Rio de Janeiro

Aplikacja desktopowa wspomagająca podejmowanie decyzji i analizę danych, przeznaczona dla zarządców nieruchomości oraz inwestorów na rynku walorów mieszkaniowych w Rio de Janeiro. Projekt łączy zautomatyzowany potok przetwarzania danych (ETL) w języku Python zoptymalizowaną relacyjną bazą danych SQLite oraz interaktywnym graficznym interfejsem użytkownika dla systemów operacyjnych typu desktop.

## Główne Funkcjonalności

* **Zautomatyzowany Potok ETL:** Skrypt w języku Python wykorzystujący bibliotekę Pandas do pobierania, czyszczenia i standaryzacji surowego zbioru danych Airbnb, składającego się z ponad 43 000 rekordów. Potok automatyzuje rzutowanie typów danych, parsowanie formatów walutowych, obsługę wartości pustych oraz mitygację statystycznych wartości odstających.
* **Relacyjny Silnik Bazy Danych:** Zoptymalizowana architektura bazy danych SQLite z prekompilowanymi zapytaniami analitycznymi i widokami, zaprojektowanymi do ekstrakcji trendów rynkowych, ewaluacji kapitału reputacji gospodarzy oraz mapowania geograficznych premii cenowych.
* **Interaktywny Panel Menedżerski:** Autonomiczny interfejs GUI zbudowany przy użyciu biblioteki Tkinter, który umożliwia nietechnicznym interesariuszom dynamiczne wykonywanie złożonych zapytań SQL, podgląd ustrukturyzowanych zbiorów danych oraz eksport wybranych widoków do standaryzowanych raportów CSV.

## Architektura Systemu

Struktura repozytorium prezentuje się następująco:

```text
rio-airbnb-analytics/
│
├── data/
│   └── .gitkeep                 # Lokalny folder na pliki danych (wypełniacz)
│
├── sql_queries/
│   ├── 01_geographic_rent.sql   # Ceny w dzielnicach i oceny lokalizacji
│   ├── 02_superhost_effect.sql  # Kapitał reputacji i ewaluacja premii
│   ├── 03_supply_structure.sql  # Dystrybucja typów pokoi i metryki
│   └── 04_investment_deals.sql  # Dynamiczne wielokryterialne wyszukiwanie okazji
│
├── src/
│   ├── data_cleaning.py         # Skrypt uruchomieniowy potoku ETL Pandas
│   └── gui_analyzer.py          # Kod interfejsu aplikacji desktopowej Tkinter
│
└── README.md                    # Dokumentacja systemu

```

## Stos Technologiczny

* **Język programowania:** Python 3.14
* **Inżynieria danych:** Pandas, SQLite3
* **Projektowanie interfejsu:** Tkinter (widżety stylizowane TTK)

## Konfiguracja i Instalacja

1. Sklonuj repozytorium:
```
git clone https://github.com/goreckyyy-dev/System-Analizy-Rynku-Airbnb-Rio-de-Janeiro-PL.git
cd rio-airbnb-analytics

```


2. Zainstaluj wymagane zależności:
```
pip install -r requirements.txt

```


3. Umieść źródłowy zbiór danych (`listings.csv`) w folderze `data/`.
4. Uruchom skrypt ETL w celu wygenerowania bazy danych:
```
python src/data_cleaning.py

```


5. Uruchom analityczny panel desktopowy:
```
python src/gui_analyzer.py

```
