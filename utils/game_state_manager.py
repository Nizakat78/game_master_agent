# utils/game_state_manager.py

class GameStateManager:
    """
    Conceptual class to manage the overall game state, which agents can access and update.
    This replaces the simple handoff_manager as game state is more complex.
    """
    def __init__(self):
        self._state = {}

    def get_state(self) -> dict:
        """Returns the current game state."""
        return self._state.copy() # Return a copy to prevent direct external modification

    def set_state(self, new_state: dict):
        """Sets the entire game state."""
        self._state = new_state.copy()

    def update_state(self, updates: dict):
        """Updates specific parts of the game state."""
        self._state.update(updates)
        # Optional: Add validation or logging for state changes

    def reset_game(self):
        """Resets the game state to initial values."""
        self._state = {
            "player_hp": 10,
            "player_inventory": [],
            "current_location": "dimly lit cave",
            "combat_active": False,
            "monster_hp": 0,
            "last_event": None,
            "game_over": False # Add game over state
        }