# Minefield WebSocket Game

A real-time **multiplayer minefield game** built with Python and Pygame, using **WebSockets** for client-server communication. Players compete to reach their goal while avoiding hidden mines and navigating a dynamic, hostile arena.

---

## Gameplay Overview

- Two players connect to a central game server.
- Each player navigates the field, avoiding randomly placed mines.
- First to reach the opposing goal **wins** — but one wrong move, and it's game over.
- All movement and interactions happen in real-time via **WebSockets**.

---

## Tech Stack

- **Python 3** — core game and networking logic
- **Pygame** — handles game rendering and player interaction
- **Sockets** — custom protocol for client-server communication
- **Multithreading** — supports concurrent client handling on the server
