Peer-to-Peer File Sharing System in Python

A simple, terminal-based peer-to-peer (P2P) file sharing system that allows two machines to share and transfer files directly using socket programming in Python.

Features

- Run as either **Server** (to share files) or **Client** (to download files)
- View a list of available files on the server
- Download selected file into local folder
- Uses TCP sockets and Python's built-in libraries only (no frameworks)

Folder Structure

p2p_file_share/
 peer.py             # Main program file
 shared/             # Files to share (used by server)
 downloads/          # Where received files are saved (used by client)

Getting Started

Prerequisites

- Python 3.x installed
- Visual Studio Code (or any text editor)
- Git (for uploading or cloning repo)

Setup Instructions

1. Clone this repository:
   git clone https://github.com/YOUR_USERNAME/p2p-file-sharing-python.git
   cd p2p-file-sharing-python

2. Create required folders:
   mkdir shared downloads

3. Place some .txt or other files into the shared/ folder.

4. Open two terminals:
   - Terminal 1 (Server):
     python peer.py
      Select server

   - Terminal 2 (Client):
     python peer.py
      Select client, then enter 127.0.0.1 (for local test)

5. Choose a file number from the list. The file will be downloaded to your downloads/ folder.
