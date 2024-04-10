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
    Then you have to follow the steps 
    1. realize the problem
    2. categorize the problem
    3. find solutions
    4. report the problem you have solved

    Keep noticing how much steps you have completed.

    The problem is {scenario}
    """

    with get_openai_callback() as cb:
        response = build_agent(executor_command_prompt)
        print(cb)

if __name__ == "__main__":
    main()
