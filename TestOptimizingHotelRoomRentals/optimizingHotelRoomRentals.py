from Room import Room
from Hotel import Hotel
import random
from copy import copy

def optimize_rentals(rooms: list, n=1) -> int:
    optimized_hotel = Hotel()
    for i in range(n):
        first_rent = random.randint(0, len(rooms)-1)
        hotel = Hotel()
        for id, r in enumerate(rooms):
            hotel.add(Room(id, r, True if id==first_rent else False))

        for r in hotel.get_all():
            left_neighbor_rented:bool = hotel.get_by_id(r.id-1).rent if r.id != 0 else False
            right_neighbor_rented:bool = hotel.get_by_id(r.id+1).rent if r.id != len(hotel.get_all())-1 else False
            
            if (left_neighbor_rented == False) and (right_neighbor_rented == False):
                hotel.rent_an_room(r.id)
        
        if (i==0) or (hotel.get_total_rentals() > optimized_hotel.get_total_rentals()):
            optimized_hotel = copy(hotel)

    for r in optimized_hotel.get_all():
        print("optimized_hotel ", i, r.id, r.value, r.rent)

    print("optimized_hotel.get_total_rentals(): ", optimized_hotel.get_total_rentals())
    return optimized_hotel.get_total_rentals()