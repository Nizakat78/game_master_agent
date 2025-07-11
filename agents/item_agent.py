# agents/item_agent.py
# from openai.agents import Agent # Hypothetical SDK base class

class ItemAgent:
    def __init__(self):
        self.name = "ItemAgent"

    def process_query(self, query: str, tools: dict, game_state: dict) -> tuple[str, str, dict]:
        query_lower = query.lower()
        state_update = {}
        response = ""
        next_agent = "NarratorAgent" # Default handoff back to Narrator

        last_event = game_state.get("last_event")
        player_inventory = game_state.get("player_inventory", [])

        if last_event == "monster_defeated":
            loot_item = tools["generate_event"](event_type="loot") # Use tool to get loot
            response = f"You defeated the foe! It dropped a {loot_item}. Do you pick it up? (Yes / No)"
            state_update["pending_loot"] = loot_item # Store pending loot
            next_agent = self.name # Stay in ItemAgent to process pick up
        elif "yes" in query_lower and game_state.get("pending_loot"):
            item_to_add = game_state["pending_loot"]
            player_inventory.append(item_to_add)
            state_update["player_inventory"] = player_inventory
            state_update["pending_loot"] = None # Clear pending loot
            response = f"{item_to_add} added to your inventory. "
            if game_state.get("combat_active") == True: # Should be false, but safety
                state_update["combat_active"] = False
            state_update["last_event"] = "item_acquired"
            next_agent = "NarratorAgent" # Handoff back to Narrator
        elif "no" in query_lower and game_state.get("pending_loot"):
            response = f"You leave the {game_state['pending_loot']} behind. "
            state_update["pending_loot"] = None # Clear pending loot
            state_update["last_event"] = "item_ignored"
            next_agent = "NarratorAgent" # Handoff back to Narrator
        elif "check inventory" in query_lower:
            if player_inventory:
                response = f"Your current inventory: {', '.join(player_inventory)}."
            else:
                response = "Your inventory is empty."
            state_update["last_event"] = "inventory_checked"
            next_agent = "NarratorAgent" # After checking, hand back to Narrator
        else:
            response = "I'm managing items. Please respond with 'Yes' or 'No' for loot, or 'check inventory'."
            state_update["last_event"] = "item_agent_unrecognized"
            next_agent = self.name # Stay in ItemAgent if unhandled query

        return response, next_agent, state_update