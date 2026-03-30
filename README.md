# PrimeShop - Plateforme E-Commerce

Plateforme e-commerce basée sur Django 6.0.3, intégrant une gestion de rôles avancée et un système de paiement sécurisé via Flutterwave.

## Fonctionnalités Principales

- **Authentification & Rôles (RBAC)** : Modèle d'utilisateurs sur-mesure (Admin, Manager, Vendeur, Client) générant des droits d'accès cloisonnés.
- **Gestion Vendeur** : Filtrage automatique du catalogue. Un vendeur ne pilote et ne visualise que ses propres produits et les commandes associées.
- **Catalogue & Panier** : Interface client optimisée pour l'achat, la recherche asynchrone (HTMX), et un tunnel de commande fluide.
- **Paiements Sécurisés** : Intégration de bout-en-bout via Flutterwave. Les statuts de paiement synchronisent l'état des commandes et des stocks en temps réel.
- **Interface Moteur** : Tableau de bord administratif refondu en utilisant le thème `unfold` pour le back-office.

## Architecture & Technologies

- **Backend** : Django 6.0.3 (Python 3.12)
- **Base de Données** : SQLite
- **Moteur de Template visuel** : HTML vanilla, CSS Natif (design Glassmorphism, mode sombre/clair)
- **Outils tiers** : HTMX (comportement réactif), Unfold Admin (Back-office moderne)

## Exigences préalables

- Python 3.12+
- Gestion de paquets `pip`

## Configuration Locale

1. Démarrer et activer l'environnement virtuel.
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Assurez-vous d'avoir un fichier `.env` à la racine contenant :
   ```env
   # Serveur & DB
   SECRET_KEY='...'
   DATABASE_URL=sqlite:///db.sqlite3
   
   # Base Flutterwave (Paiements)
   FLW_PUBLIC_KEY='...'
   FLW_SECRET_KEY='...'
   FLW_ENCRYPTION_KEY='...'
   
   # Configuration Email (Pour mot de passe oublié etc.)
   EMAIL_HOST='smtp.gmail.com'
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER='votre_email@gmail.com'
   EMAIL_HOST_PASSWORD='mot_de_passe_d_application'
   DEFAULT_FROM_EMAIL='votre_email@gmail.com'
   ```
4. Appliquer les migrations des modèles :
   ```bash
   python manage.py migrate
   ```
5. Distribuer le serveur local :
   ```bash
   python manage.py runserver
   ```

## Tests

Une suite de tests unitaires fonctionnels certifie le comportement métier (Commandes, Stock, Rôles).
```bash
python manage.py test
```
