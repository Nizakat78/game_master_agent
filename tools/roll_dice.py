from agents import function_tool, RunContextWrapper
from typing import TypedDict
import random
import re

class RollDiceInput(TypedDict):
    dice_notation: str  # e.g. "1d6" or "2d20+5"

class RollDiceOutput(TypedDict):
    result: int
    rolls: str

@function_tool
async def roll_dice(wrapper: RunContextWrapper, input: RollDiceInput) -> RollDiceOutput:
    """
    Simulates dice rolls based on RPG notation.
    """
    notation = (input.get("dice_notation") or "1d6").lower().strip()

    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", notation)
    if not match:
        return {"result": 0, "rolls": "Invalid notation"}

    num_dice = int(match.group(1))
    dice_sides = int(match.group(2))
    modifier = int(match.group(3) or 0)

    rolls_list = [random.randint(1, dice_sides) for _ in range(num_dice)]
    total = sum(rolls_list) + modifier

    return {
        "result": total,
        "rolls": f"Rolls: {rolls_list}, Modifier: {modifier}"
    }
