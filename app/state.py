class TravelState:
    def __init__(self):
        self.destination = None
        self.trip_type = None
        self.travel_date = None
        self.passengers = None
        self.budget = None
        self.history = []

    def to_dict(self):
        return {
            "destination": self.destination,
            "trip_type": self.trip_type,
            "travel_date": self.travel_date,
            "passengers": self.passengers,
            "budget": self.budget,
            "history": self.history
        }