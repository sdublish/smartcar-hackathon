"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from sqlalchemy import func

from model import connect_to_db, db, User, Vehicle, UserVehicle, Service, UserVehicleService, YelpCategory, YelpCategoryService
from server import app


# def load_users(users_filename):
#     """Load users into database."""

#     print("User")

#     for i, row in enumerate(open(users_filename)):
#         fname, lname, email, password = row.split("|")

#         user = User(fname=fname, lname=lname, email=email, password=password)

#         db.session.add(user)

#         if i % 1 == 0:
#             print i

#     db.session.commit()


def load_vehicles(vehicles_filename):
    """Load vehicles."""

    print("Vehicle")

    for i, row in enumerate(open(vehicles_filename)):
        row = row.rstrip()

        vehicle_make, vehicle_model_name, vehicle_year = row.split("|")

        vehicle = Vehicle(vehicle_make=vehicle_make, vehicle_model_name=vehicle_model_name, vehicle_year=vehicle_year)

        db.session.add(vehicle)

        if i % 10 == 0:
            print i

    db.session.commit()

# def load_uservehicles(uesrvehicles_filename):
#     """Load UserVehicles."""

#     print("UserVehicle")

#     for i, row in enumerate(open(uservehicles_filename)):
#         row = row.rstrip()

#         nickname, user_id, model_id = row.split("|")

#         uservehicle = UserVehicle(nickname=nickname, user_id=user_id, model_id=model_id)

#         db.session.add(uservehicle)

#         if i % 10 == 0:
#             print i

#     db.session.commit()


def load_services(services_filename):
    """Load services."""

    print("Service")

    for i, row in enumerate(open(students_filename)):
        row = row.rstrip()

        username, password, fname, lname, class_id = row.split("|")

        student = Student(username=username, password=password, fname=fname, lname=lname, class_id=class_id, avatar_id=i+1)

        db.session.add(student)

        if i % 10 == 0:
            print i

    db.session.commit()












# def set_val_survey_id():
#     """Set value for the next survey_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(ListeningSurvey.survey_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('surveys_survey_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# def set_val_classroom_instrument_type_id():
#     """Set value for the next classroom_instrument_type_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(ClassroomInstrumentType.classroom_instrument_type_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('classroom_instrument_type_instrument_type_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()







if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_teachers("seed_data/teacher_seed.txt")
    load_classrooms("seed_data/classroom_seed.txt")
    load_avatars("seed_data/avatar_seed.txt")
    load_students("seed_data/student_seed.txt")
    load_instrument_types("seed_data/instrument_types_seed.txt")
    load_classroom_instrument_types("seed_data/classroom_instrument_type_seed.txt")
    load_instruments("seed_data/instrument_seed.txt")
    load_composers("seed_data/composers_seed.txt")
    load_music("seed_data/music_seed_actual.txt")
    create_surveys()
    set_val_student_id()
    set_val_teacher_id()
    set_val_class_id()
    # set_val_survey_id()
    set_val_classroom_instrument_type_id


    
