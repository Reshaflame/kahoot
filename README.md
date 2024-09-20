Multi-User Quiz Challenge
This application is a multi-user quiz game inspired by Kahoot, supporting up to 5 participants in a session.
The backend is powered by a Python-based TCP server, and the user interface is built with Svelte.
Communication between the server and clients happens over TCP connections, with the server handling custom headers and JSON data. Clients are managed with multithreading.

Key Features
Maximum Participants: 5 players per game session
Answer Countdown: Players have 15 seconds to submit their answers
Automatic Reconnection: After a game session ends, the connection closes and automatically becomes available for new participants.
In case of no response, the socket closes by itself after a timeout period.
Launching the Game
To run the game on your local machine, ensure you are using a Linux-based OS or WSL with a bash terminal.
Simply use the provided bash script to initiate the game:

Set up the IP Address:

In the front-end code, located in client/API.svelte, update the IP to match your local machine’s IP address.
Find your local IP by executing the command ip a in the terminal.
Start the Game:

Run the script: ./start.sh
The server will listen on port 5000.
The Svelte front-end will be available at http://<your_ip>:8000.
A GUI for the server (Tkinter-based) will launch automatically.
System Architecture Overview
1. Backend (Python TCP Server)
The backend runs as a TCP server utilizing socket.AF_INET (IPv4) and socket.SOCK_STREAM (TCP).
It employs multi-threading to handle multiple client connections and process HTTP-like requests sent over TCP.

Port 5000: Handles player requests via TCP.
Port 5001: Manages server status when using Docker (optional).
2. Frontend (Svelte Application)
The frontend operates on different ports based on how you run it:

Port 8000: Local Svelte development.
Port 5003: Running through Docker.
3. Server Management GUI
When running the server through the bash script, a Tkinter GUI for server management will appear automatically.
If Docker is used, the GUI is available via Flask at port 5002.

Reconnection and Session Management
After each quiz session, players can reconnect for a new round. If any player fails to respond within the specified timeout period, their connection will automatically close.

License
The project follows the MIT License guidelines.