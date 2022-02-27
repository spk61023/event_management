# event_management

# How to run the project?

    docker-compose build
    docker-compose up

# if postgres issue occurs

    docker run -e POSTGRES_HOST_AUTH_METHOD=trust postgres

# make migrations

    docker-compose run web python appknox/manage.py makemigrations
    docker-compose run web python appknox/manage.py migrate

# SuperUser creation

    docker-compose run web python appknox/manage.py createsuperuser

    Username: admin
    Email: admin@gmail.com
    Password: 12345
    Confirm Password: 12345
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.

# API documentation

1. Admin list all events

    endpoint = http://127.0.0.1:8000/events/
    method = GET
    authorization = Basic authorization
                    username = admin
                    password = 12345
    status = 200 OK
    body =
            [
                {
                    "id": "684be538-a1b3-4a3c-bf4d-56485d4356a1",
                    "title": "TED Talk 1",
                    "description": "TED Talk 1 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                },
                {
                    "id": "c0ee640d-3719-499d-b339-2367d15b8df3",
                    "title": "TED Talk 2",
                    "description": "TED Talk 2  is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                },
                {
                    "id": "1e7f6647-f771-49e3-824b-2a8e160c90d5",
                    "title": "TED Talk 3",
                    "description": "TED Talk 3 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                },
                {
                    "id": "9cdac744-ebbd-4b05-ab97-1aa85fa0d872",
                    "title": "TED Talk 4",
                    "description": "TED Talk 4 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                },
                {
                    "id": "5e1c6006-a267-48e1-92a2-84f6c6adeef3",
                    "title": "TED Talk 3",
                    "description": "TED Talk 3 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                },
                {
                    "id": "8251045e-5186-4409-af83-2f55622f0bbf",
                    "title": "Experiment One",
                    "description": "TED Talk 3 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                }
            ]
    status = 403 Forbidden if credentials are not correct or not an admin user
    body =
            {
                "detail": "Invalid username/password."
            }

2. Admin create an event
    endpoint = http://127.0.0.1:8000/events/
    method = POST
    authorization = Basic
    status = 201 Created
    body =
            {
                "title": "TED Talk 1",
                "description": "TED Talk 1 is amazing event managed and organized worldwide.",
                "event_type": "Conference",
                "created_by": "",
                "attendees": []
            }
    response =
                {
                    "id": "f65c97a8-f9f1-4b02-9687-3dd86247db9a",
                    "title": "Event 1",
                    "description": "TED Talk 1 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "attendees": []
                }
    status = 403 Forbidden if credentials are not correct or not an admin user
    body =
            {
                "detail": "Invalid username/password."
            }

3. Admin get an event details / summary
    endpoint = http://127.0.0.1:8000/events/uuid/
                uuid = 8251045e-5186-4409-af83-2f55622f0bbf
    method = GET
    authorization = Basic
    status = 200 OK
    body =
            {
                "id": "8251045e-5186-4409-af83-2f55622f0bbf",
                "title": "Experiment One",
                "description": "TED Talk 3 is amazing event managed and organized worldwide.",
                "event_type": "Conference",
                "attendees": []
            }
    status = 403 Forbidden if credentials are not correct or not an admin user
    body =
            {
                "detail": "Invalid username/password."
            }

4. Admin update an event
    endpoint = http://127.0.0.1:8000/events/8251045e-5186-4409-af83-2f55622f0bbf/
    method = PUT
    authorization = Basic
    status = 200 OK
    body =
            {
                "id": "8251045e-5186-4409-af83-2f55622f0bbf",
                "title": "Experiment Ten",
                "description": "TED Talk 3 is amazing event managed and organized worldwide.",
                "event_type": "Conference",
                "attendees": []
            }
    status = 403 Forbidden if credentials are not correct or not an admin user
    body =
            {
                "detail": "Invalid username/password."
            }

5. Admin delete an event
    endpoint = http://127.0.0.1:8000/events/8251045e-5186-4409-af83-2f55622f0bbf/
    method = DELETE
    authorization = Basic
    status = 204 No Content
    body = []
    status = 403 Forbidden if credentials are not correct or not an admin user
    body =
            {
                "detail": "Invalid username/password."
            }

6. User Views all events
    endpoint : http://127.0.0.1:8000/events/all-events/
    method : GET
    response : 200 OK
    body :
            [
                {
                    "id": "703d763c-08b5-4ce1-bf5e-b7247e4250b2",
                    "title": "Event 1",
                    "description": "TED Talk 1 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "created_by": "f59ee7a0-07ec-4935-8b3c-0bc4b1e434e6",
                    "attendees": []
                },
                {
                    "id": "46eb9a4c-64eb-4c7c-93dc-abe3097f2e82",
                    "title": "Event 2",
                    "description": "TED Talk 2 is amazing event managed and organized worldwide.",
                    "event_type": "Conference",
                    "created_by": "f59ee7a0-07ec-4935-8b3c-0bc4b1e434e6",
                    "attendees": []
                }
            ]

7. User registers for an event
    endpoint : http://127.0.0.1:8000/events/register-event/
    method : POST
    params :
            {
                "seat_id" : "ee1ee148-1bc1-4cfa-aa0d-6cdecc08c614",
                "user_id" :"dde4f8ab-29f0-4235-8779-4e85f4f3635a"
            }
    response : 201, created
    body :
            {
                "status": 201,
                "message": {
                    "id": "87064759-e7ed-4e2c-8ca8-d54cebc0ce20",
                    "timestamp": "2022-02-26T10:51:39.674897Z",
                    "seat": "ee1ee148-1bc1-4cfa-aa0d-6cdecc08c614",
                    "booked_by": "dde4f8ab-29f0-4235-8779-4e85f4f3635a"
                }
            }

8. User views ticket
    endpoint : http://127.0.0.1:8000/events/view-ticket/
    method : GET
    params :
                {
                    "ticket_id" : "619d670e-a3c6-4ec9-bc2d-66e49f6c9a70"
                }
    response : 200, OK
    body :
            {
                "ticket_id": "619d670e-a3c6-4ec9-bc2d-66e49f6c9a70",
                "show_name": "Event 1",
                "seat_no": "5",
                "show_starts_at": "26/02/2022 18:00:00",
                "booked_on": "26/02/2022 12:02:06"
            }

9. User Views Registered events
    endpoint : UserViewAllRegisteredEvents
    method : GET
    response : 200, OK
    params :
                {
                    "booked_by" :"dde4f8ab-29f0-4235-8779-4e85f4f3635a"
                }
    body :
                [
                    {
                        "id": "703d763c-08b5-4ce1-bf5e-b7247e4250b2",
                        "title": "Event 1",
                        "description": "TED Talk 1 is amazing event managed and organized worldwide.",
                        "event_type": "Conference",
                        "attendees": [
                            "dde4f8ab-29f0-4235-8779-4e85f4f3635a"
                        ]
                    }
                ]

10. Admin set max capacity of the theatre
    endpoint :http://127.0.0.1:8000/events/theatres/<uuid>/
                uuid : 208b84f4-2cea-49fc-83cc-ccb8d1b68625
    method : PUT
    params :
                {
                    "capacity" :  6
                }
    status : 200, OK
    body :
            {
                "id": "208b84f4-2cea-49fc-83cc-ccb8d1b68625",
                "name": "Theatre 1",
                "location": "Bengaluru",
                "capacity": 6
            }
