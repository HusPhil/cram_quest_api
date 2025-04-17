from fastapi import HTTPException

class ProfileNotFound(HTTPException):
    def __init__(self, profile_id: int):
        super().__init__(status_code=404, detail=f"Profile {profile_id} not found")

class ProfileAlreadyExist(HTTPException):
    def __init__(self, player_id: int):
        super().__init__(status_code=400, detail=f"Profile already exists for player: {player_id}")