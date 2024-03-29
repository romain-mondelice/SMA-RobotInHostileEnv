# SMA-RobotInHostileEnv

# General architecture

```
SMA-RobotInHostileEnv/
│
├── agents/
│   ├── robot_agents.py
│   └── object_agents.py
│
├── core/
│   ├── model.py
│   └── schedule.py
│
├── reports/
│   ├── .gitkeep
│
├── visualization/
│   └── server.py
│
├── README.md
├── requirements.txt
└── run.py
```

# Robot Mission Simulation

This project simulates a multi-agent system where robots collaborate to collect and transform dangerous waste in a hostile environment. The environment is divided into three zones with varying levels of radioactivity, and the robots have different capabilities based on their type.

## Table of Contents

- [SMA-RobotInHostileEnv](#sma-robotinhostileenv)
- [General architecture](#general-architecture)
- [Robot Mission Simulation](#robot-mission-simulation)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Design Choices](#design-choices)
  - [Code Structure](#code-structure)
  - [Technical Choices](#technical-choices)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/romain-mondelice/SMA-RobotInHostileEnv.git
   ```

2. Navigate to the project directory:
   ```
   cd SMA-RobotInHostileEnv
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the simulation, execute the following command:
```
python run.py
```

This will launch the simulation with the default configuration. You can modify the simulation parameters by editing the `run.py` file.

## Design Choices
OOP - To elaborate and Complete

## Code Structure

The project is organized into the following directories and files:

- `agents/`: Contains the implementation of robot agents and object agents.
  - `robot_agents.py`: Defines the classes for green, yellow, and red robots, implementing their behaviors.
  - `object_agents.py`: Defines the classes for waste and radioactivity agents.

- `core/`: Contains the core components of the simulation.
  - `model.py`: Defines the `RobotMission` model, which handles the simulation logic and environment.
  - `schedule.py`: Defines a custom scheduler for activating agents in a specific order.

- `visualization/`: Contains the code for visualizing the simulation.
  - `server.py`: Sets up the visualization server using Mesa's built-in visualization tools.

- `run.py`: The main entry point of the simulation. It creates an instance of the `RobotMission` model and runs the simulation.

## Technical Choices
TODO