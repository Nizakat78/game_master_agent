# Game Master Agent (Fantasy Adventure Game)

## Project Description
The Game Master Agent runs a text-based fantasy adventure game using multiple specialized AI agents. It narrates the story, manages combat encounters, and handles inventory/rewards based on player choices and game events.

## How it Works
This system leverages the OpenAI Agent SDK + Runner to orchestrate dynamic interactions between specialized agents and tools based on gameplay.

1.  **Story Narration**: The `NarratorAgent` progresses the adventure story, presents scenarios, and interprets player choices.
2.  **Combat Phase**: When a combat encounter is triggered, the `NarratorAgent` hands off to the `MonsterAgent`. The `MonsterAgent` manages the combat sequence, potentially using the `Dice Roller` tool.
3.  **Inventory & Rewards**: Upon defeating a monster or discovering items, the `MonsterAgent` or `NarratorAgent` can hand off to the `ItemAgent`. The `ItemAgent` manages the player's inventory and rewards, potentially using the `Event Generator` tool for loot.

## Agents Involved
* **`NarratorAgent`**: Controls the main story progression, presents choices, and handles non-combat events.
* **`MonsterAgent`**: Manages combat encounters with monsters.
* **`ItemAgent`**: Handles player inventory, rewards, and loot.

## Tools Utilized
* **`Dice Roller`**: A tool containing `roll_dice()` used by agents (e.g., `MonsterAgent`) for random outcomes like combat rolls.
* **`Event Generator`**: A tool containing `generate_event()` used to create random game events or determine loot.

## Handoff Logic
Dynamic switches between agent roles occur based on gameplay events. The `main.py` (runner) and a conceptual `GameStateManager` orchestrate these transitions, passing relevant game state (e.g., player health, current location, combat status) between agents.

## Setup and Installation
(Instructions on how to set up your Python environment, install dependencies, and configure the OpenAI Agent SDK)

```bash
# Example:
# git clone game_master_agent
# cd game_master_agent
# pip install -r requirements.txt
# export OPENAI_API_KEY="your_openai_api_key"