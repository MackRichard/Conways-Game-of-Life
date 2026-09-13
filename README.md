# Conway's Game of Life

An interactive, customisable simulator for Conway's **Game of Life** and various cellular automata rule systems, built with Python and Pygame.

---

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Controls](#-controls)
- [Technologies](#-technologies)
- [License](#-license)

---

## ✨ Features

- **Pre-game Settings Menu:**
  - Configurable simulation speed (generations per second).
  - Neighborhood selection: **Moore** (8 neighbors) or **Von Neumann** (4 neighbors).
  - Flexible survival and birth rule selectors (Survive / Birth buttons).
  - Dynamic detection of known rule sets (e.g., Conway's Life, HighLife, Seeds, Diamoeba, Day & Night, Maze).

- **Advanced Settings:**
  - **Max Cell Age Gradient:** Adjustable color gradient based on cell longevity.
  - **Trail Fade Speed:** Smooth fade-out (afterglow) effect when cells die.

- **Interactive Simulation Mode:**
  - Smooth pan and infinite zoom via mouse controls.
  - Draw new cells directly using the left mouse button.
  - Real-time population statistics panels (last 100 generations & total history graph).

---

## 🛠️ Prerequisites

Ensure you have **Python 3.x** installed on your system.

Required library:
- `pygame`

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MackRichard/Conways-Game-of-Life.git](https://github.com/MackRichard/Conways-Game-of-Life.git)
   cd Conways-Game-of-Life

2. **Install dependencies:**
   pip install pygame

2. **Run the application:**
   python main.py

---

## 🎮 Controls

  - Pause / Resume = [SPACE]
  - Speed (Hold) = + / - OR [UP] / [DOWN]
  - Randomize Viewport = [R]
  - Clear Grid = [C]
  - Draw Cell (Click & Drag) = [LEFT]
  - Pan Viewport (Click & Drag) = [RIGHT]
  - Zoom In / Out = [WHEEL]

---

Built with the assistance of Gemini AI.