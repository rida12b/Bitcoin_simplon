import os
import psycopg2

print("--- DEBUT DU SCRIPT DE TEST DE CONNEXION BDD ---")

db_url = os.environ.get("DATABASE_URL")

if not db_url:
    print("ERREUR FATALE: La variable d'environnement DATABASE_URL est manquante.")
else:
    print(f"Tentative de connexion à la base de données...")
    try:
        conn = psycopg2.connect(db_url)
        print(">>> SUCCES: Connexion à PostgreSQL réussie !")
        
        # On vérifie si la table existe
        cur = conn.cursor()
        cur.execute("SELECT to_regclass('public.bitcoin_prices');")
        table_exists = cur.fetchone()[0]
        if table_exists:
            print(">>> INFO: La table 'bitcoin_prices' a bien été trouvée.")
        else:
            print(">>> ERREUR: La table 'bitcoin_prices' est INTROUVABLE.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"--- ERREUR DE CONNEXION ---")
        print(f"L'erreur est: {e}")
        print("-----------------------------")
        
print("--- FIN DU SCRIPT DE TEST ---")
