\# EventHub



EventHub is a simplified backend API for an event ticketing platform built using Django and Django REST Framework.



Users can browse events, reserve seats, and cancel reservations.



\## Technologies Used



\* Python

\* Django

\* Django REST Framework

\* SQLite

\* Django ORM

\* REST API

\* Virtual Environment



\## Project Setup



\### 1. Clone the repository



```bash

git clone <your-github-repository-url>

cd EventHub

```



\### 2. Create and activate the virtual environment



On Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 4. Apply migrations



```powershell

python manage.py migrate

```



\### 5. Start the development server



```powershell

python manage.py runserver

```



The API will be available at:



`http://127.0.0.1:8000/`



\## API Endpoints



\### Events



| Method | Endpoint            | Description               |

| ------ | ------------------- | ------------------------- |

| GET    | `/api/events/`      | List all events           |

| POST   | `/api/events/`      | Create an event           |

| GET    | `/api/events/{id}/` | Get a specific event      |

| PUT    | `/api/events/{id}/` | Update an event           |

| PATCH  | `/api/events/{id}/` | Partially update an event |

| DELETE | `/api/events/{id}/` | Delete an event           |



\### Event Filtering



Filter events by status:



`GET /api/events/?status=upcoming`



Filter events by venue:



`GET /api/events/?venue=Bangalore`



\### Reservations



| Method | Endpoint                         | Description                    |

| ------ | -------------------------------- | ------------------------------ |

| GET    | `/api/reservations/`             | List reservations              |

| POST   | `/api/reservations/`             | Create a reservation           |

| GET    | `/api/reservations/{id}/`        | Get a specific reservation     |

| PUT    | `/api/reservations/{id}/`        | Update a reservation           |

| PATCH  | `/api/reservations/{id}/`        | Partially update a reservation |

| DELETE | `/api/reservations/{id}/`        | Delete a reservation           |

| POST   | `/api/reservations/{id}/cancel/` | Cancel a reservation           |



\### Reservation Filtering



Filter reservations by event:



`GET /api/reservations/?event\_id=1`



\## Seat Reservation Logic



When a reservation is created, the requested number of seats is deducted from the event's `available\_seats`.



If the requested number of seats is greater than the available seats, the API returns a `400 Bad Request`.



When a reservation is cancelled, the reserved seats are added back to the event.



\## Middleware



EventHub includes a custom `RequestLoggingMiddleware`.



The middleware records:



\* HTTP method

\* Request path

\* Response status code

\* Request processing time



Example:



```text

GET /api/events/ - 200 - 0.01s

```



\## Design Decision



The reservation seat deduction is handled inside the `ReservationSerializer.create()` method.



This keeps the reservation creation and seat deduction logic together in one place. It also makes the reservation workflow easy to understand and maintain.



For a production system with many concurrent users, database transactions such as `transaction.atomic()` and row-level locking would be considered to prevent race conditions when multiple users attempt to reserve the last available seats at the same time.



\## Testing



The following functionality was tested:



\* Create event

\* List events

\* Filter events by status

\* Filter events by venue

\* Create reservation

\* Seat deduction after reservation

\* Overbooking prevention

\* Cancel reservation

\* Seat restoration after cancellation

\* Filter reservations by event ID

\* Request logging middleware



\## Required Screenshots



The project was tested using EchoAPI/Postman with screenshots for:



1\. Successful reservation — `201 Created`

2\. Overbooking failure — `400 Bad Request`

3\. Successful cancellation — `200 OK`



