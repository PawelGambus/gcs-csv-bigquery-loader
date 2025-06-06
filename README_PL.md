# ☁️ GCP Cloud Function – Ładowanie danych CSV do BigQuery

To repozytorium zawiera moje rozwiązanie zadania rekrutacyjnego polegającego na zbudowaniu zautomatyzowanego pipeline’u do ładowania danych w Google Cloud Platform.

---

## 📝 Opis zadania

Zaloguj się do konsoli Google Cloud Platform i wybierz projekt: `alterdata-rekrutacja-46`.  
W tym projekcie masz pełne uprawnienia.

### Zadanie

- Utwórz własny bucket w Google Cloud Storage o dowolnej nazwie.
- Zaimplementuj **Cloud Function (v1)** w GCP, która:
  - będzie wyzwalana po wrzuceniu pliku `.csv` do bucketu,
  - automatycznie stworzy odpowiadającą mu tabelę w BigQuery na podstawie wykrytego schematu (`autodetect=True`).

---

## 🚀 Szczegóły mojego rozwiązania

### ✅ Wybór regionu i konfiguracja zasobów

- Wybrałem region `europe-central2 (Warszawa)` ze względu na niskie koszty oraz bliskość geograficzną do firmy.
- Zarówno bucket, jak i Cloud Function znajdują się w tym samym regionie, aby uniknąć kosztów przesyłu między regionami.
- Wyłączyłem replikację wieloregionową, aby ograniczyć zbędne koszty.

### ✅ Cloud Function – Trigger i architektura

- Użyłem triggera: `google.cloud.storage.object.v1.finalized`  
  → Wyzwalany po zakończeniu uploadu pliku (na podstawie [dokumentacji GCP](https://cloud.google.com/functions/docs/calling/storage)).
- Zweryfikowałem, że upload pliku faktycznie uruchamia funkcję.
- Funkcja została skonfigurowana z minimalnymi zasobami i ograniczeniem do jednego równoczesnego wykonania, zakładając niskie obciążenie.

### ✅ Dataset i obsługa tabel BigQuery

- Utworzyłem dataset za pomocą CLI.
- Zamiast biblioteki pandas użyłem natywnej biblioteki Google Cloud SDK dla Pythona, aby uprościć integrację i uniknąć dodatkowych zależności.
- Sprawdziłem istnienie tabel na podstawie [tego wzorca z dokumentacji BigQuery](https://cloud.google.com/bigquery/docs/samples/bigquery-table-exists).
- Przetworzyłem i zweryfikowałem nazwy tabel zgodnie z [restrykcjami BigQuery](https://cloud.google.com/bigquery/docs/tables).
- W przypadku konfliktu nazw dodałem automatyczne numerowanie tabel (np. `tabela_2`, `tabela_3`).
- Pomijałem pliki, które nie są typu CSV lub znajdują się w nieobsługiwanych folderach.

### ✅ Konfiguracja ładowania danych

- Użyłem następującej konfiguracji `LoadJobConfig`:
  ```python
  job_config = bigquery.LoadJobConfig(
      autodetect=True,
      column_name_character_map="V2",
      skip_leading_rows=1,
      source_format=bigquery.SourceFormat.CSV,
  )
  ```
  - `column_name_character_map="V2"`: automatycznie poprawia problematyczne nagłówki kolumn, aby były zgodne z BigQuery.
  - Na podstawie [oficjalnej dokumentacji](https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig#google_cloud_bigquery_job_LoadJobConfig_column_name_character_map).

### 🧹 Walidacje i usprawnienia

- Zweryfikowałem, że wrzucany plik faktycznie ma rozszerzenie `.csv`.
- Oczyściłem nazwy tabel i sprawdziłem je pod kątem niedozwolonych znaków lub nadmiernej długości.
- Upewniłem się, że nagłówki są poprawne, a format pliku CSV jest spójny.
- W przypadku istnienia tabeli o tej samej nazwie dodawany jest sufiks.
- Logowanie odbywa się wewnątrz funkcji Cloud Function za pomocą `print()` – choć docelowo powinno być przekierowane do logów strukturalnych.

---

## 🔒 Uprawnienia i bezpieczeństwo

- Po zakończeniu testów wyłączyłem **publiczny dostęp** do bucketu.
- Brakującą rolę `roles/pubsub.publisher` dodałem podczas debugowania.

---

## 🧪 Wykorzystane technologie

- Google Cloud Storage
- Google Cloud Functions (Python v1)
- BigQuery + CLI (`bq`)
- Python BigQuery SDK

---

## 🧑‍💻 Autor

Pawel Gambus  
[LinkedIn](https://www.linkedin.com/in/pawel-gambus)
