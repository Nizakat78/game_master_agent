# agents/monster_agent.py
# from openai.agents import Agent # Hypothetical SDK base class

class MonsterAgent:
    def __init__(self):
        self.name = "MonsterAgent"
        self.current_monster = {"name": "goblin", "hp": 5, "attack": 2}
        self.player_hp_at_combat_start = 0

    def process_query(self, query: str, tools: dict, game_state: dict) -> tuple[str, str, dict]:
        query_lower = query.lower()
        state_update = {}
        response = ""
        next_agent = self.name # Default to staying with MonsterAgent

        if game_state.get("combat_active") == False and game_state.get("last_event") == "monster_encounter":
            # Initiate combat
            self.player_hp_at_combat_start = game_state["player_hp"]
            game_state["combat_active"] = True
            state_update["combat_active"] = True
            state_update["monster_hp"] = self.current_monster["hp"]
            response = f"A {self.current_monster['name']} attacks! Your HP: {game_state['player_hp']}, {self.current_monster['name']} HP: {self.current_monster['hp']}. What's your move? (Attack / Defend / Run)"
        elif game_state.get("combat_active") == True:
            player_hp = game_state["player_hp"]
            monster_hp = game_state["monster_hp"]

            if "attack" in query_lower:
                player_damage_roll = tools["roll_dice"](sides=6) # Mock player attack roll
                monster_damage_roll = tools["roll_dice"](sides=3) # Mock monster attack roll

                player_damage = max(1, player_damage_roll - self.current_monster["attack"] // 2) # Simplified damage
                monster_hp -= player_damage
                response += f"You strike the {self.current_monster['name']}, dealing {player_damage} damage! {self.current_monster['name']} HP: {monster_hp}.\n"
                state_update["monster_hp"] = monster_hp

                if monster_hp <= 0:
                    response += f"The {self.current_monster['name']} is defeated!\n"
                    state_update["combat_active"] = False
                    state_update["last_event"] = "monster_defeated"
                    next_agent = "ItemAgent" # Handoff to ItemAgent for loot
                else:
                    monster_damage = max(1, monster_damage_roll) # Simplified monster damage
                    player_hp -= monster_damage
                    response += f"The {self.current_monster['name']} retaliates, hitting you for {monster_damage} damage. Your HP: {player_hp}.\n"
                    state_update["player_hp"] = player_hp
                    if player_hp <= 0:
                        response += "You have been defeated! Game Over."
                        state_update["game_over"] = True
                        next_agent = self.name # Stay here to end game or transition to Narrator for end message
            elif "defend" in query_lower:
                response = "You brace for impact. The monster attacks but you mitigate some damage."
                # Simplified: Half monster damage
                monster_damage_roll = tools["roll_dice"](sides=3)
                monster_damage = max(0, monster_damage_roll // 2)
                player_hp -= monster_damage
                response += f"The {self.current_monster['name']} hits you for {monster_damage} damage. Your HP: {player_hp}.\n"
                state_update["player_hp"] = player_hp
                if player_hp <= 0:
                    response += "You have been defeated! Game Over."
                    state_update["game_over"] = True
            elif "run" in query_lower:
                run_roll = tools["roll_dice"](sides=10)
                if run_roll > 5: # 50% chance to run away
                    response = "You successfully disengage from combat and flee!"
                    state_update["combat_active"] = False
                    state_update["last_event"] = "ran_away"
                    next_agent = "NarratorAgent" # Handoff back to Narrator
                else:
                    response = "You try to run, but the monster blocks your escape!"
                    monster_damage_roll = tools["roll_dice"](sides=3)
                    monster_damage = max(1, monster_damage_roll)
                    player_hp -= monster_damage
                    response += f"The {self.current_monster['name']} hits you for {monster_damage} damage as you try to escape. Your HP: {player_hp}.\n"
                    state_update["player_hp"] = player_hp
                    if player_hp <= 0:
                        response += "You have been defeated! Game Over."
                        state_update["game_over"] = True
            else:
                response = "Invalid combat command. What's your move? (Attack / Defend / Run)"
        else:
            response = "No combat active."
            state_update["last_event"] = "no_combat_active"
            next_agent = "NarratorAgent" # Fallback if somehow called incorrectly

        return response, next_agent, state_update