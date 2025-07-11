# tools/event_generator.py
import random
# from openai.agents import tool # Hypothetical decorator

# @tool
def generate_event(event_type: str = "general") -> str:
    """
    Generates a mock game event or loot item based on event_type.
    """
    if event_type == "loot":
        loot_items = ["rusty dagger", "healing potion", "gold coin", "tattered map", "shiny pebble"]
        return random.choice(loot_items)
    elif event_type == "obstacle":
        obstacles = ["a fallen tree", "a slippery slope", "a hidden pit"]
        return random.choice(obstacles)
    else:
        general_events = ["A gentle breeze blows.", "You hear distant birdsong.", "Nothing unusual happens."]
        return random.choice(general_events)