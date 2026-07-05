# Generator Kodu — Instrukcja

Krótkie instrukcje:

- Zainstaluj zależności:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- Wygeneruj kod (z `interface.json`):

```bash
python gen.py
```

- Uruchom serwer (w jednym terminalu):

```bash
python server.py
```

- Uruchom klienta (w drugim terminalu):

```bash
python client.py
```

Instrukcje dla GIT:

- Zainicjalizuj repo i dodaj remote:

```bash
git init
git add .
git commit -m "Initial commit: generator and examples"
git remote add origin <your-github-repo-url>
git push -u origin main
```

Spakowanie gałęzi `main` do archiwum:

```bash
git archive -o submission.zip main
```
