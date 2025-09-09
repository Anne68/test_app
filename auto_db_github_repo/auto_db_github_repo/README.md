# Auto DB Feed & Price Updater (RAWG → MySQL)

Automatise l'alimentation de la base **MySQL** depuis l'API **RAWG** et la mise à jour récurrente des **meilleurs prix PC** (DLCompare).  
Prêt pour **GitHub** (workflow Actions) et pour **Windows**/**Linux**.

## Démarrage rapide

### Linux/macOS
```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python orchestrate.py
```

### Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
.\.venv\Scripts\python.exe orchestrate.py
```

## Variables (.env)
Voir `.env.example` et complétez vos identifiants MySQL + `RAWG_API_KEY`.

## Planification
- Linux: `cronjob.sh` via crontab.
- Windows: `run.ps1` (Planificateur) ou `run.cmd` (CMD).

## GitHub Actions
Secrets requis: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `RAWG_API_KEY`.
