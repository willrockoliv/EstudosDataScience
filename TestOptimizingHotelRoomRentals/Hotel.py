from Room import Room

class Hotel():
    def __init__(self) -> None:
        self.rooms:list = list()
    
    def add(self, room:Room):
        self.rooms.append(room)

    def rent_an_room(self, id:int):
        for r in self.rooms:
            if r.id == id:
                r.rent = True
                break

    def get_by_id(self, id:int):
        for r in self.rooms:
            if r.id == id:
                return r
            
    def get_all(self):
        return self.rooms
    
    def get_total_rentals(self):
        rented_rooms = []
        for r in self.rooms:
            if r.rent:
                rented_rooms.append(r)
        return sum([r.value for r in rented_rooms])