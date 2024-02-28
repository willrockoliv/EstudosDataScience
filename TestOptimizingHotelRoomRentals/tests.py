from optimizingHotelRoomRentals import *

if __name__=="__main__":
    rooms_1 = [6, 7, 1, 2, 7, 7, 7, 1, 4, 6]
    expected_total_value_rooms_1 = 7+7+7+6 #27

    rooms_2 = [3, 7, 7]
    expected_total_value_rooms_2 = 3+7 #10

    rooms_3 = [2, 8, 10, 9, 8]
    expected_total_value_rooms_3 = 2+10+8 #20

    repetitions = 100
    assert optimize_rentals(rooms_1, repetitions) == expected_total_value_rooms_1
    assert optimize_rentals(rooms_2, repetitions) == expected_total_value_rooms_2
    assert optimize_rentals(rooms_3, repetitions) == expected_total_value_rooms_3