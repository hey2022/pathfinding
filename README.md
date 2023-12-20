# Pathfinding Demonstration

This program will allow users to interactively visualise many different pathfinding algorithms.

# Setup

## Clone


``` sh
git clone https://github.com/hey2022/pathfinding.git
```

## Virtual Environment Setup

### Windows

``` powershell
cd pathfinding
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Linux

```sh
cd pathfinding
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

# Usage

Run `python main.py`

- `LMB` to create a `wall node`
- `RMB` to clear a `node`
- `s` to set the `source node`
- `t` to set the `target node`
- `c` to clear the board
- `tab` to cycle which pathfinding algorithm to use (WIP)
- `enter` to run the pathfinding algorithm

