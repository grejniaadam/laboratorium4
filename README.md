# Generator kodu do serializacji i deserializacji danych

Ten projekt pokazuje, jak zdefiniować strukturę danych w pliku JSON, a następnie automatycznie wygenerować klasy Pythona z metodami serializacji i deserializacji do formatu binarnego przy użyciu szablonów Jinja2.

## Co robi projekt

- czyta definicję typów z pliku `interface.json`
- generuje kod Python z metodami `serialize()` i `deserialize()`
- obsługuje typy proste (`int32`, `uint8`, `uint32`, `float64`, `string`)
- obsługuje typy złożone (np. obiekty zagnieżdżone)
- zawiera przykładowy serwer i klient TCP/IP komunikujące się za pomocą wygenerowanej implementacji
- zawiera prosty test integracyjny

## Struktura projektu

- `interface.json` — definicja typów danych
- `gen.py` — generator kodu na podstawie pliku JSON
- `templates/python_struct.jinja2` — szablon Jinja2
- `generated/serializers.py` — wygenerowany kod serializatorów
- `server.py` — przykładowy serwer TCP/IP
- `client.py` — przykładowy klient TCP/IP
- `test.py` — test integracyjny
- `requirements.txt` — zależności projektu

## Jak uruchomić

### 1. Utwórz środowisko wirtualne

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Wygeneruj kod

```powershell
python gen.py
```

### 3. Uruchom serwer

```powershell
python server.py
```

### 4. Uruchom klienta w drugim terminalu

```powershell
python client.py
```

## Jak dodać nowy typ danych

Edytuj plik `interface.json` i dodaj nowy typ w sekcji `types`.

Przykład:

```json
{
  "types": [
    {
      "name": "Product",
      "fields": [
        {"name": "sku", "type": "uint32"},
        {"name": "title", "type": "string"},
        {"name": "price", "type": "float64"}
      ]
    }
  ]
}
```

Po zmianie uruchom:

```powershell
python gen.py
```

## Jak uruchomić testy

```powershell
python test.py
```

## Git i Moodle

### Zapisz zmiany do Git

```powershell
git add .
git commit -m "Opis zmian"
git push origin main
```

### Utwórz archiwum do Moodle

```powershell
git archive -o submission.zip main
```

## Uwagi

Projekt jest prostą demonstracją metody generowania kodu bez użycia AI. W praktyce można go rozszerzyć o:

- obsługę tablic
- obsługę pól opcjonalnych
- walidację danych
- wersjonowanie formatu binarnego
- bardziej zaawansowane protokoły komunikacji
