# agents/narrator_agent.py
# from openai.agents import Agent # Hypothetical SDK base class

class NarratorAgent:
    def __init__(self):
        self.name = "NarratorAgent"
        self.story_progress = 0
        self.story_arcs = [
            "You awaken in a dimly lit cave. A narrow path stretches before you, and you hear a faint growl. What do you do? (Explore / Fight)",
            "You cautiously follow the path. The growling intensifies, and a goblin jumps out! Prepare for combat.",
            "After defeating the foe, the path splits into two: a dark tunnel and a brightly lit passage. Which way do you go? (Dark Tunnel / Bright Passage)",
            "The bright passage leads to a shimmering pool. Do you drink from it? (Drink / Ignore)"
        ]

    def process_query(self, query: str, tools: dict, game_state: dict) -> tuple[str, str, dict]:
        query_lower = query.lower()
        state_update = {}
        next_agent = self.name # Default to staying with Narrator

        if query == "start_game":
            response = self.story_arcs[0]
            self.story_progress = 0
            state_update["last_event"] = "game_start"
        elif "explore" in query_lower and self.story_progress == 0:
            response = self.story_arcs[1]
            self.story_progress = 1
            state_update["last_event"] = "monster_encounter"
            next_agent = "MonsterAgent" # Handoff to MonsterAgent for combat
        elif "fight" in query_lower and self.story_progress == 0:
            response = "You decide to face the threat head-on! A large goblin appears immediately. Prepare for combat."
            self.story_progress = 1
            state_update["last_event"] = "monster_encounter"
            next_agent = "MonsterAgent" # Handoff to MonsterAgent for combat
        elif "continue" in query_lower or "next" in query_lower:
            self.story_progress += 1
            if self.story_progress < len(self.story_arcs):
                response = self.story_arcs[self.story_progress]
                state_update["last_event"] = "story_progress"
            else:
                response = "The adventure concludes for now! Thanks for playing."
                state_update["game_over"] = True
        elif "check inventory" in query_lower:
            next_agent = "ItemAgent" # Handoff to ItemAgent to show inventory
            response = "Checking your inventory..."
            state_update["last_event"] = "check_inventory"
        else:
            response = "I don't understand that command. Please choose an action related to the story."
            state_update["last_event"] = "unrecognized_command"

        return response, next_agent, state_update