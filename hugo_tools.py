RETHINK_LIMIT = 0


def get_customer_messages(scenario: str) -> str:
    """
    Useful for receiving the content from customer. It might be the first time or the several times because of the rethinking.
    and your rethink limit times is 5
    Goal: Get the content from the customer.
    Output:
    - the categorized content from customer.
    - if the customer's message is not clear, return the "ask_for_more_information".
    """
    global RETHINK_LIMIT  # Declare the global variable

    # if invoke this function, plus 1 to the RETHINK_LIMIT
    RETHINK_LIMIT += 1  # Update the global variable
    print(f"Rethink limit: {RETHINK_LIMIT}")

    if RETHINK_LIMIT == 5:
        return ask_for_more_information()

    return "Get the content from the customer"


def check_knowledge_base() -> str:
    """
    Useful for finding the solution for the customer's problem. Here, we might compare the customer's problem with the knowledge base.
    Goal: Check the solution for the customer's problem related to the knowledge base or not.
    Output:
        - If the solution is found, return "give_solution".
        - If the solution is not found, return "ask_for_more_information".
    """
    return "Check the solution for the customer's problem related to the knowledge base or not"


def ask_for_more_information() -> str:
    """
    Useful for asking for more information from the customer.
    Goal: Ask for more information from the customer.
    Output: Ask for more information from the customer.
    """
    return "Ask for more information from the customer"


def give_solution() -> str:
    """
    Useful for providing solutions to the customer.
    Goal: Provide solutions to the customer.
    Output:
        - If the customer is satisfied with the answer, return "open_ticket".
        - If the customer is not satisfied, return "rethink_solution".

    """
    return "Provide solutions to the customer"


def rethink_solution() -> str:
    """
    Useful for rethinking the solution.
    Goal: Rethink the solution.
    Output:
        - If the customer is satisfied with the answer, return "open_ticket".
        - If the customer is not satisfied, return "rethink_solution".
        - If the rethinking limit is reached, return "escalate_to_tam".
    """
    return "Rethink the solution"


def open_ticket() -> str:
    """\
    Useful for opening the ticket for the customer's problem.

    Goal: Open the ticket for the customer's problem.

    Output:
        - If the ticket is submitted, return the "ticket_submitted".
        - If the ticket is not submitted, return the "rethink_solution".
    """

    try:
        ...
        send_mock_ticket_to_customer()  # API call

    except Exception as e:
        return f"error occurred, the error is {e}."


def send_mock_ticket_to_customer():
    """
    Useful for sending the ticket to the customer.
    Goal: Send the ticket to the customer.
    Output: Send the ticket to the customer.
    """
    return {"ticket_submitted": True}
