#!/usr/bin/env bash

set -Eeuo pipefail

PROJECT_DIR="$HOME/mlh-portfolio-site"
SESSION_NAME="portfolio"
BRANCH="main"
PORT="5000"

echo "Redeploying portfolio site"

# check if the project exists.
if [[ ! -d "$PROJECT_DIR/.git" ]]; then
    echo "Error: Git repository not found at:"
    echo "$PROJECT_DIR"
    echo "Update PROJECT_DIR inside ~/redeploy-site.sh."
    exit 1
fi

if [[ ! -f "$PROJECT_DIR/.env" ]]; then
    echo "Error: $PROJECT_DIR/.env does not exist."
    echo "Create it with:"
    echo "cp $PROJECT_DIR/example.env $PROJECT_DIR/.env"
    echo "Then fill in the required environment variables."
    exit 1
fi

echo
echo "1. Stopping existing tmux sessions..."

# Do not fail when no tmux server is currently running.
tmux kill-server 2>/dev/null || true

echo
echo "2. Entering project directory..."

cd "$PROJECT_DIR"

echo
echo "3. Downloading the latest main branch..."

git fetch origin
git reset --hard "origin/$BRANCH"

echo
echo "4. Preparing the Python virtual environment..."

# Use an existing .venv or venv directory.
# Create .venv if neither exists.
if [[ -d "$PROJECT_DIR/.venv" ]]; then
    VENV_DIR="$PROJECT_DIR/.venv"
elif [[ -d "$PROJECT_DIR/venv" ]]; then
    VENV_DIR="$PROJECT_DIR/venv"
else
    echo "No virtual environment found. Creating .venv..."
    python3 -m venv "$PROJECT_DIR/.venv"
    VENV_DIR="$PROJECT_DIR/.venv"
fi

source "$VENV_DIR/bin/activate"

echo "Installing Python dependencies..."

python -m pip install -r requirements.txt

echo
echo "5. Starting Flask inside a detached tmux session..."

tmux new-session \
    -d \
    -s "$SESSION_NAME" \
    "cd '$PROJECT_DIR' && source '$VENV_DIR/bin/activate' && exec python -m flask --app app run --host=0.0.0.0 --port=$PORT"

sleep 2

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo
    echo "Deployment completed successfully."
    echo "Project: $PROJECT_DIR"
    echo "Branch:  $BRANCH"
    echo "Session: $SESSION_NAME"
    echo "Port:    $PORT"
    echo
    echo "View the Flask output with:"
    echo "tmux attach -t $SESSION_NAME"
else
    echo "Error: The tmux session did not remain active."
    echo "Try running the Flask application manually to inspect the error:"
    echo "cd $PROJECT_DIR"
    echo "source $VENV_DIR/bin/activate"
    echo "python -m flask --app app run --host=0.0.0.0 --port=$PORT"
    exit 1
fi