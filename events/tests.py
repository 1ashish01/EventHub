from datetime import date

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Event, Reservation


class EventAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.event = Event.objects.create(
            title="Python Conference",
            venue="Bangalore",
            date=date(2026, 10, 10),
            total_seats=10,
            available_seats=10,
            status="upcoming"
        )

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.available_seats, 10)

    def test_event_list(self):
        response = self.client.get("/api/events/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_successful_reservation(self):
        response = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Ashish",
                "attendee_email": "ashish@example.com",
                "seats_reserved": 2
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)

        self.event.refresh_from_db()

        self.assertEqual(self.event.available_seats, 8)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_reservation_cannot_exceed_available_seats(self):
        response = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Ashish",
                "attendee_email": "ashish@example.com",
                "seats_reserved": 11
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)

        self.event.refresh_from_db()

        self.assertEqual(self.event.available_seats, 10)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            event=self.event,
            attendee_name="Ashish",
            attendee_email="ashish@example.com",
            seats_reserved=3,
            status="confirmed"
        )

        self.event.available_seats -= 3
        self.event.save()

        response = self.client.post(
            f"/api/reservations/{reservation.id}/cancel/"
        )

        self.assertEqual(response.status_code, 200)

        self.event.refresh_from_db()
        reservation.refresh_from_db()

        self.assertEqual(self.event.available_seats, 10)
        self.assertEqual(reservation.status, "cancelled")

    def test_cannot_cancel_twice(self):
        reservation = Reservation.objects.create(
            event=self.event,
            attendee_name="Ashish",
            attendee_email="ashish@example.com",
            seats_reserved=2,
            status="cancelled"
        )

        response = self.client.post(
            f"/api/reservations/{reservation.id}/cancel/"
        )

        self.assertEqual(response.status_code, 400)

    def test_last_seat_cannot_be_oversold(self):
        self.event.available_seats = 1
        self.event.total_seats = 1
        self.event.save()

        response1 = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Person One",
                "attendee_email": "one@example.com",
                "seats_reserved": 1
            },
            format="json"
        )

        response2 = self.client.post(
            "/api/reservations/",
            {
                "event": self.event.id,
                "attendee_name": "Person Two",
                "attendee_email": "two@example.com",
                "seats_reserved": 1
            },
            format="json"
        )

        successful_bookings = sum(
            response.status_code == 201
            for response in [response1, response2]
        )

        self.assertEqual(successful_bookings, 1)

        self.event.refresh_from_db()

        self.assertEqual(self.event.available_seats, 0)
        self.assertEqual(
            Reservation.objects.filter(status="confirmed").count(),
            1
        )