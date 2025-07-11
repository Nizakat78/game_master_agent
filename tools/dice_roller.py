# tools/dice_roller.py
import random
# from openai.agents import tool # Hypothetical decorator

# @tool
def roll_dice(sides: int = 6) -> int:
    """
    Simulates rolling a dice with a specified number of sides.
    Default to a 6-sided die.
    """
    if sides < 1:
        raise ValueError("Dice must have at least 1 side.")
    return random.randint(1, sides)