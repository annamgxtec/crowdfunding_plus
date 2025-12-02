cat > README.md <<'EOF'
# Crowdfunding PLUS

Projecte: **Crowdfunding PLUS curs BlockChain**  
Aplicació web senzilla (Flask + SQLite) que simula una plataforma de micromecenatge amb controls addicionals.

## Descripció
Aquesta aplicació permet:
- Crear projectes amb un objectiu i límits (mínim per donació, màxim per donant, màxim total).
- Llistar projectes.
- Aportar diners (simulats) a projectes.
- Veure l'historial d'aportacions de cada projecte.

Totes les dades s'emmagatzemen en una base de dades SQLite (`crowdfunding.db`).

## Requisits
- Python 3
- pip
- Virtualenv recomanat
- Paquets: `flask`, `flask_sqlalchemy`
