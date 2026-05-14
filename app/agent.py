import logging

from dotenv import load_dotenv
from google import genai

from app.state import TravelState
from app.tools import search_trips, calculate_price, create_booking_request


load_dotenv()

client = genai.Client()

logger = logging.getLogger("travelx.agent")


class TravelXAgent:
    def __init__(self):
        self.state = TravelState()

    def run(self, user_input: str) -> str:
        logger.info("User message received")

        self.state.history.append({
            "role": "customer",
            "message": user_input
        })

        self.extract_basic_info(user_input)

        logger.info(
            "State after extraction: destination=%s, trip_type=%s, travel_date=%s, passengers=%s",
            self.state.destination,
            self.state.trip_type,
            self.state.travel_date,
            self.state.passengers
        )

        if self.is_ready_to_search():
            logger.info("Required booking information is complete. Running tools.")

            trip_result = search_trips(
                destination=self.state.destination,
                trip_type=self.state.trip_type,
                travel_date=self.state.travel_date,
                passengers=self.state.passengers
            )

            price_result = calculate_price(
                destination=self.state.destination,
                passengers=self.state.passengers
            )

            logger.info("Tools executed: search_trips, calculate_price")

            prompt = self.build_response_prompt(
                user_input=user_input,
                trip_result=trip_result,
                price_result=price_result
            )

        else:
            logger.info("Required booking information is incomplete. Asking next question.")

            prompt = self.build_question_prompt(user_input)

        agent_reply = self.generate_ai_response(prompt)

        self.state.history.append({
            "role": "agent",
            "message": agent_reply
        })

        logger.info("Agent reply generated")

        return agent_reply

    def generate_ai_response(self, prompt: str) -> str:
        """
        Calls Gemini API safely.
        If one model is unavailable, it tries another model.
        """

        models = [
            "gemini-3-flash-preview",
            "gemini-3.1-flash-lite",
            "gemini-3.1-flash-lite-preview",
            "gemini-2.5-flash",
            "gemini-2.0-flash"
        ]

        last_error = None

        for model_name in models:
            try:
                logger.info("Calling AI provider with model=%s", model_name)

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                if response.text:
                    logger.info("AI provider response received from model=%s", model_name)
                    return response.text

                logger.warning("AI provider returned empty response from model=%s", model_name)

            except Exception as error:
                last_error = error
                logger.error("AI provider error with model=%s: %s", model_name, error)

        logger.error("All AI provider models failed. Last error: %s", last_error)

        return (
            "Sorry, TravelX Agent is temporarily unable to contact the AI service. "
            "Please try again in a moment."
        )

    def extract_basic_info(self, text: str) -> None:
        text_lower = text.lower()

        destinations = ["dubai", "istanbul", "cairo", "paris", "canada","roma"]

        for destination in destinations:
            if destination in text_lower:
                self.state.destination = destination

        if "round trip" in text_lower or "return ticket" in text_lower:
            self.state.trip_type = "round_trip"

        elif "one way" in text_lower or "one-way" in text_lower:
            self.state.trip_type = "one_way"

        if "2" in text_lower or "two" in text_lower:
            self.state.passengers = 2

        elif "1" in text_lower or "one person" in text_lower:
            self.state.passengers = 1

        if "tomorrow" in text_lower:
            self.state.travel_date = "tomorrow"

        if "next week" in text_lower:
            self.state.travel_date = "next_week"

    def is_ready_to_search(self) -> bool:
        return all([
            self.state.destination,
            self.state.trip_type,
            self.state.travel_date,
            self.state.passengers
        ])

    def build_question_prompt(self, user_input: str) -> str:
        return f"""
You are TravelX customer service agent.

Always reply in English.

Your job:
- Help customers with travel inquiries.
- Ask for missing booking information step by step.
- Do not ask all questions at once.
- Be friendly, short, and professional.
- Do not invent real prices.
- If information is missing, ask only for the next missing field.

Current collected customer data:
{self.state.to_dict()}

Customer message:
{user_input}

Task:
Ask for the next missing important information.
"""

    def build_response_prompt(
        self,
        user_input: str,
        trip_result: dict,
        price_result: dict
    ) -> str:
        return f"""
You are TravelX customer service agent.

Always reply in English.

Customer data:
{self.state.to_dict()}

Trip search result:
{trip_result}

Price estimate:
{price_result}

Customer message:
{user_input}

Task:
Give a helpful summary.
Mention that prices are estimated and need confirmation by a human agent.
Ask if the customer wants to create a booking request.
"""