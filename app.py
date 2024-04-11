from langchain_community.callbacks import get_openai_callback

from hugo_agent import build_agent


def main():

    role = """\
    You are a cautious individual who divides tasks into smaller ones \
    and continuously verifies that you are following the steps. \
    Moreover, you select suitable tools to solve problems.
    """

    scenario = "My EC2 is broken and I can't access my website."

    executor_command_prompt = f"""
    {role}
    Now your mission is to solve the problem from customer.
    Then you have to follow the steps:
    1. Classify the problem

    2. Compare the classification with the knowledge base

    3. If there is no information in the knowledge base:
    - Search for information.
        - Open ticket:
        1. Bot gives the ticket information to the customer before submitting to the ticket system.
            - If yes:
                - Submit the ticket.
            - If no:
                - Ask for more information or reconsider the approach.

    4. If there is information in the knowledge base:
    - Provide solutions.
        1. If the customer is satisfied with the answer:
            - Open a ticket.
        2. If the customer is not satisfied:
            - Rethink the solution (a limit for rethinking must be set).
            - If the maximum limit of rethinking is reached:
                - Escalate to Technical Account Manager (TAM).

    Keep noticing how much steps you have completed.
    The problem is {scenario}
    """

    with get_openai_callback() as cb:
        response = build_agent(executor_command_prompt)
        print(cb)


if __name__ == "__main__":
    main()
