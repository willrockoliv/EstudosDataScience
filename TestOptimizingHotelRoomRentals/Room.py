class Room():
    def __init__(self, id:int, value:int, rent:bool) -> None:
        self.id:int = id
        self.value:int = value
        self.rent:bool = rent

    def __lt__(self, other):
        """sort by id"""
        return self.id > other.id