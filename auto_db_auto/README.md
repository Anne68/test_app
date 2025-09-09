
# Auto DB feed + update (RAWG + Prices)

## Install
```
cd auto_db_auto
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit DB_* and RAWG_API_KEY
```

## Run
```
python orchestrate.py
```

## Cron (example)
```
crontab -e
15 2 * * * /bin/bash /ABSOLUTE/PATH/auto_db_auto/cronjob.sh
0 */3 * * * /bin/bash /ABSOLUTE/PATH/auto_db_auto/cronjob.sh
```
