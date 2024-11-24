from datetime import datetime
from db_instance import db # Import the database instance
from models import User, Vehicle, UserVehicle, Location, Pass, PassTraveller, Preset, PresetTraveller # Import models from models.py

def insert_mock_data():
    # Insert mock data into the database
    user1 = User(email='alice@example.com', phone_number='123456789', password_hash='[hash]', first_name='Alice', middle_name=None, last_name='Smith')
    user2 = User(email='bob@example.com', phone_number='987654321', password_hash='[hash]', first_name='Bob', middle_name=None, last_name='Johnson')
    user3 = User(email='charlie@example.com', phone_number='555555555', password_hash='[hash]', first_name='Charlie', middle_name=None, last_name='Brown')
    user4 = User(email='dave@example.com', phone_number='444444444', password_hash='[hash]', first_name='Dave', middle_name=None, last_name='Wilson')

    vehicle1 = Vehicle(vehicle_number='SKR9859E')
    vehicle2 = Vehicle(vehicle_number='SGB267D')
    vehicle3 = Vehicle(vehicle_number='GBH1206B')
    vehicle4 = Vehicle(vehicle_number='GBL1368X')

    user_vehicle1 = UserVehicle(user_id=1, vehicle_id=1)
    user_vehicle2 = UserVehicle(user_id=2, vehicle_id=1)
    user_vehicle3 = UserVehicle(user_id=2, vehicle_id=2)
    user_vehicle4 = UserVehicle(user_id=3, vehicle_id=2)
    user_vehicle5 = UserVehicle(user_id=4, vehicle_id=3)
    user_vehicle6 = UserVehicle(user_id=4, vehicle_id=4)

    location1 = Location(city='Singapore', state='Singapore', country='Singapore')
    location2 = Location(city='Johor Bahru', state='Johor', country='Malaysia')

    pass1 = Pass(vehicle_id=1, creator_user_id=1, creation_datetime=datetime(2024, 11, 23, 8, 0), expiry_datetime=datetime(2024, 11, 27, 8, 0), pass_date=datetime(2024, 11, 25, 0, 0), origin_id=1, destination_id=2)
    pass2 = Pass(vehicle_id=2, creator_user_id=2, creation_datetime=datetime(2024, 11, 23, 8, 0), expiry_datetime=datetime(2024, 11, 26, 8, 0), pass_date=datetime(2024, 11, 25, 0, 0), origin_id=1, destination_id=2)
    pass3 = Pass(vehicle_id=3, creator_user_id=4, creation_datetime=datetime(2024, 11, 20, 8, 0), expiry_datetime=datetime(2024, 11, 21, 8, 0), pass_date=datetime(2024, 11, 20, 0 , 0), origin_id=1, destination_id=2)
    pass4 = Pass(vehicle_id=4, creator_user_id=4, creation_datetime=datetime(2024, 11, 19, 8, 0), expiry_datetime=datetime(2024, 11, 20, 8, 0), pass_date=datetime(2024, 11, 19, 0, 0), origin_id=1, destination_id=2)

    pass_traveller1 = PassTraveller(pass_id=1, user_id=1)  # Alice as traveller for SKR9859E
    pass_traveller2 = PassTraveller(pass_id=1, user_id=2)  # Bob as traveller for SKR9859E
    pass_traveller3 = PassTraveller(pass_id=2, user_id=2)  # Bob as traveller for SGB267D
    pass_traveller4 = PassTraveller(pass_id=2, user_id=3)  # Charlie as traveller for SGB267D

    # Adding all records to the session
    db.session.add_all([
        user1, user2, user3, user4,
        vehicle1, vehicle2, vehicle3, vehicle4,
        user_vehicle1, user_vehicle2, user_vehicle3, user_vehicle4, user_vehicle5, user_vehicle6,
        location1, location2,
        pass1, pass2, pass3, pass4,
        pass_traveller1, pass_traveller2, pass_traveller3, pass_traveller4
    ])

    # Commit the session to save the records to the database
    db.session.commit()