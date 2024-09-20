#!/bin/bash

# Function to install Python if not present
install_python() {
    echo "Python is not installed. Attempting to install Python..."
    
    if command -v dnf >/dev/null; then
        sudo dnf install -y python3
    elif command -v apt >/dev/null; then
        sudo apt update
        sudo apt install -y python3
    else
        echo "No supported package manager found. Please install Python manually."
        exit 1
    fi
}

# Function to handle graceful shutdown
shutdown() {
    echo "Shutting down all components gracefully..."

    # Kill the Python server process if it exists
    if [[ -n "$SERVER_PID" ]]; then
        echo "Stopping Python server (PID $SERVER_PID)..."
        kill $SERVER_PID
    fi

    # Kill the Python GUI server process if it exists
    if [[ -n "$GUI_SERVER_PID" ]]; then
        echo "Stopping Python GUI server (PID $GUI_SERVER_PID)..."
        kill $GUI_SERVER_PID
    fi

    # Kill the Svelte client process if it exists
    if [[ -n "$CLIENT_PID" ]]; then
        echo "Stopping Svelte client (PID $CLIENT_PID)..."
        kill $CLIENT_PID
    fi

    # Wait for all processes to fully terminate
    wait $SERVER_PID $GUI_SERVER_PID $CLIENT_PID
    exit 0
}

# Trap SIGINT (Ctrl + C) and call the shutdown function
trap shutdown SIGINT

# Check if Python is installed
if ! command -v python3 >/dev/null; then
    install_python
fi

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Tkinter
echo "Attempting to install Tkinter..."
if command -v dnf >/dev/null; then
    sudo dnf install -y python3-tkinter
elif command -v apt >/dev/null; then
    sudo apt install -y python3-tk
else
    echo "No supported package manager found for Tkinter installation."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r ./server/requirements.txt

# Check if port 5000 is in use
if lsof -i :5000 >/dev/null; then
    echo "Port 5000 is in use. Attempting to kill existing process..."
    lsof -ti :5000 | xargs kill -9
fi

echo "Starting Python servers..."
python3 ./server/server.py & 
SERVER_PID=$!
python3 ./server/server_gui.py &  
GUI_SERVER_PID=$!


cd client/svelte-client
echo "Installing Node.js dependencies..."
npm install

# Build the Svelte client
echo "Building Svelte client..."
npm run build

# Start the Svelte app
echo "Starting Svelte app..."
npm start &
CLIENT_PID=$!

cd ../../

wait $SERVER_PID
wait $GUI_SERVER_PID
wait $CLIENT_PID
