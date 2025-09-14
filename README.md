# 🎮 Games Data Project

Automatisation d'extraction et de scraping :
- API RAWG.io → table `games`
- Scraping DLCompare → table `best_price_pc`
- Stockage MySQL AlwaysData

## 🚀 Utilisation
1. Cloner le repo
2. Créer un fichier `.env` :
   ```
   RAWG_API_KEY=ta_clef_rawg
   MYSQL_HOST=mysql-anne.alwaysdata.net
   MYSQL_PORT=3306
   MYSQL_USER=ton_user
   MYSQL_PASSWORD=ton_mdp
   MYSQL_DB=anne_games_db
   ```
3. Lancer manuellement :
   ```bash
   python scripts/run_rawg_extract.py
   python scripts/run_dlcompare_scrape.py
   ```
4. Sur GitHub, configure les **Secrets** :
   - RAWG_API_KEY
   - MYSQL_HOST
   - MYSQL_PORT
   - MYSQL_USER
   - MYSQL_PASSWORD
   - MYSQL_DB

## 🤖 Automatisation
Le workflow GitHub Actions (`.github/workflows/data-jobs.yml`) exécute :
- tous les jours à 06:00 et 18:00 (heure de Paris)
- ou manuellement via **workflow_dispatch**
