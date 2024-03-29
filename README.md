# SMA-RobotInHostileEnv

# General architecture

```
robot_mission_numberofthegroup/
│
├── agents/
│   ├── __init__.py
│   ├── robot_agents.py
│   └── object_agents.py
│
├── core/
│   ├── __init__.py
│   ├── model.py
│   └── schedule.py
│
├── visualization/
│   ├── __init__.py
│   └── server.py
│
├── README.md
└── main.py
```

# Robot Mission Simulation

This project simulates a multi-agent system where robots collaborate to collect and transform dangerous waste in a hostile environment. The environment is divided into three zones with varying levels of radioactivity, and the robots have different capabilities based on their type.

## Table of Contents

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
   cd robot_mission_numberofthegroup
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the simulation, execute the following command:
```
python main.py
```

This will launch the simulation with the default configuration. You can modify the simulation parameters by editing the `run.py` file.

## Design Choices

The project is designed using the Mesa framework, which is a Python library for building agent-based models. The key design choices are as follows:

- The environment is represented as a grid, with each cell containing information about its radioactivity level and the presence of waste or robots.
- Robots are modeled as agents with specific behaviors based on their type (green, yellow, or red).
- Waste and radioactivity are represented as agents without behaviors, serving as markers in the environment.
- The simulation follows a step-based approach, where each agent performs its actions in a random order during each step.

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

The project utilizes the following technologies and libraries:

- Python: The programming language used for implementing the simulation.
- Mesa: A Python framework for building agent-based models.
- NumPy: A library for numerical computing in Python, used for handling arrays and mathematical operations.
- Matplotlib: A plotting library for creating visualizations and charts.

The choice of Mesa as the framework allows for easy creation of agent-based models, providing built-in functionality for grid-based environments, agent scheduling, and visualization.

The use of NumPy and Matplotlib enables efficient numerical computations and the generation of informative visualizations to analyze the simulation results.