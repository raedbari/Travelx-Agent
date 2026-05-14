from app.agent import TravelXAgent


def main():
    agent = TravelXAgent()

    print("TravelX Customer Service Agent")
    print("Type 'exit' to quit")
    print("-" * 40)

    while True:
        user_input = input("Customer: ")

        if user_input.strip().lower() == "exit":
            break

        response = agent.run(user_input)

        print(f"Agent: {response}")
        print("-" * 40)


if __name__ == "__main__":
    main()