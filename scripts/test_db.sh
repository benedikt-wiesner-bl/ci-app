#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "Erstelle ein neues Todo über die API..."
curl -s -X POST http://localhost:5001/todos \
     -H "Content-Type: application/json" \
     -d '{"task":"Healthcheck-Test"}' | jq .

echo -e "\nAktuelle Todos (API-Abfrage):"
curl -s http://localhost:5001/todos | jq .

echo -e "\nInhalt der SQLite-DB (direkt auf Host):"
sqlite3 data/todos.db "SELECT * FROM todos;"
