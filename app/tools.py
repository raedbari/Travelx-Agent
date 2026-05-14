def search_trips(destination: str, trip_type: str, travel_date: str, passengers: int) -> dict:
    return {
        "success": True,
        "destination": destination,
        "trip_type": trip_type,
        "travel_date": travel_date,
        "passengers": passengers,
        "available_options": [
            {
                "airline": "TravelX Partner Airlines",
                "duration": "6 hours",
                "class": "Economy"
            },
            {
                "airline": "TravelX Premium Partner",
                "duration": "5 hours 30 minutes",
                "class": "Economy Plus"
            }
        ]
    }


def calculate_price(destination: str, passengers: int) -> dict:
    base_prices = {
        "dubai": 350,
        "istanbul": 280,
        "cairo": 220,
        "paris": 520,
        "canada": 700
    }

    price_per_person = base_prices.get(destination, 400)
    total = price_per_person * passengers

    return {
        "success": True,
        "currency": "EUR",
        "price_per_person": price_per_person,
        "passengers": passengers,
        "total": total,
        "note": "This is a mock estimated price, not a real booking price."
    }


def create_booking_request(customer_data: dict) -> dict:
    return {
        "success": True,
        "request_id": "TX-REQ-1001",
        "status": "pending_agent_review",
        "message": "Booking request created and waiting for human review."
    }