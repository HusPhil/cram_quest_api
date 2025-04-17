from fastapi import HTTPException

class PlayerNotFound(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=404, detail=f"Player {player_id} not found")

class PlayerAlreadyExist(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"Player already exists for user: {user_id}")

class NoPlayersFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No players found")