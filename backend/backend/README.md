# Little Future — Plateforme intelligente pour crèches

Plateforme moderne pour crèches et garderies : éducation 3D, suivi parental, dossier médical, évaluations quotidiennes et messagerie. Interface 100 % en français, code en anglais.

## Stack

- **Backend** : Django 5 + Django REST Framework + SimpleJWT
- **Auth** : email + JWT, validation administrateur, RBAC (Parent / Responsable / Éducateur / Admin)
- **Base de données** : SQLite en dev, PostgreSQL conseillé en prod
- **Frontend** : templates Django + CSS animations + JS vanilla (PWA-ready)
- **Prêt pour** : Three.js / Babylon.js (cours 3D), Channels (chat temps réel), React (SPA dédiée)

## Structure

```
backend/
├── littlefuture/          # Projet Django (settings, urls, wsgi, asgi)
├── apps/
│   ├── accounts/          # Utilisateur custom (rôles + validation admin)
│   ├── children/          # Enfants
│   ├── nurseries/         # Crèches + services
│   ├── health/            # Dossiers médicaux, allergies, médicaments, vaccins
│   ├── education/         # Cours 3D, leçons, progression
│   ├── tracking/          # Évaluations quotidiennes + rapports hebdo
│   ├── chat/              # Conversations + messages
│   ├── notifications/     # Notifications utilisateur
│   └── core/              # Pages publiques, routage API
├── templates/             # Pages HTML françaises
└── static/                # CSS, JS, images
```

## Démarrage rapide (Windows / PowerShell)

```powershell
# 1. Activer le venv (depuis la racine du projet)
.\.venv\Scripts\Activate.ps1

# 2. Aller dans le backend
cd backend

# 3. (Une seule fois) installer les dépendances
pip install -r requirements.txt

# 4. Migrer la base
python manage.py migrate

# 5. Créer un super-utilisateur (admin)
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Ouvrez ensuite :

- 🏠 Accueil : http://127.0.0.1:8000/
- 🔐 Connexion : http://127.0.0.1:8000/connexion/
- ✍️ Inscription : http://127.0.0.1:8000/inscription/
- 🛠️ Admin : http://127.0.0.1:8000/admin/
- 🔌 API root : http://127.0.0.1:8000/api/v1/

## Endpoints API principaux

### Authentification
- `POST /api/v1/auth/register/parent/` — inscription parent
- `POST /api/v1/auth/register/manager/` — inscription crèche
- `POST /api/v1/auth/login/` — JWT (bloqué tant que le compte n'est pas validé)
- `POST /api/v1/auth/refresh/` — refresh du token
- `GET/PATCH /api/v1/auth/me/` — profil courant

### Modération admin
- `GET /api/v1/admin/users/pending/` — comptes en attente
- `POST /api/v1/admin/users/{id}/approve/` — approuver
- `POST /api/v1/admin/users/{id}/reject/` — rejeter (avec `rejection_reason`)

### Métier
- `/api/v1/children/`
- `/api/v1/nurseries/`
- `/api/v1/health/{records,allergies,diseases,medications,diet,vaccinations}/`
- `/api/v1/education/{courses,lessons,progress}/`
- `/api/v1/tracking/{evaluations,reports}/`
- `/api/v1/chat/{conversations,messages}/`
- `/api/v1/notifications/`

## Workflow de validation

1. Le visiteur s'inscrit en tant que **parent** ou **responsable de crèche**.
2. Le compte est créé avec `approval_status = "pending"`.
3. La connexion est bloquée tant qu'un admin n'a pas approuvé le compte.
4. L'admin approuve/rejette via l'API ou via `/admin/`.

## Prochaines étapes (extensions prévues)

- 🎮 Intégration Three.js pour les leçons 3D (champ `scene_url` déjà prévu sur `Course`).
- 💬 Chat temps réel via Django Channels + WebSockets.
- 📱 Manifest PWA + service worker pour installation mobile.
- 🌐 Dashboards SPA en React (parents / crèche / admin).
- 📨 Notifications par email + push (Firebase / Web Push).
- 🐘 Bascule PostgreSQL via variables d'environnement (`python-decouple` déjà installé).

## Couleurs de la charte
- Primaire : `#F7B6C2` (rose doux)
- Secondaire : `#C9A7FF` (violet clair)

## Code & langue
- 🇫🇷 Tout le contenu utilisateur est en français.
- 🇬🇧 Tout le code (modèles, vues, sérialiseurs, commentaires) est en anglais.
