#!/usr/bin/env bash
# Starts the Diplomacy web UI and game server.
# Run from anywhere: bash diplomacy_engine/run_web.sh

DIPLOMACY_REPO="C:/Users/z515232/repositories/diplomacy-repo"
WEB_DIR="$DIPLOMACY_REPO/diplomacy/web"

echo ""
echo "Starting Diplomacy server..."
echo "  Game server : http://localhost:8432"
echo "  Web UI      : http://localhost:3000"
echo "  Login       : admin / password"
echo ""
echo "Press Ctrl+C to stop both processes."
echo ""

# Start Python game server in background
python -m diplomacy.server.run &
SERVER_PID=$!

# Start React frontend (blocking)
cd "$WEB_DIR" && npm start

# On exit, also kill the Python server
kill $SERVER_PID 2>/dev/null
