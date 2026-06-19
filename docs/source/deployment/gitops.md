# GitOps
Dpgstack uses a bare git repository approach for syncing code across devices:
- Main repo lives on one device
- Other devices clone from the bare repo
- Data folder (with SQLite db) is synced separately via Syncthing
- Only one device can run the app at a time to avoid conflicts

This allows deployment on both Linux (Docker) and Android (Termux/gunicorn) while keeping data in sync.
