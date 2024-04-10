from guardrails.hub import RegexMatch
from guardrails import Guard


def is_valid(text):
    """
    Check https://www.guardrailsai.com/docs/
    """
    guard = Guard().use(RegexMatch, regex="[0-9]+\.\s.*\s\|\s.*\s\|\s(True|False)\s\|\s.*\.", on_fail="exception")

    lines = text.strip().split('\n')

    try:
        for line in lines:
            guard.validate(line.strip())
        print("Succeeded")
        return True
    except Exception as e:
        print(f"Failed: {e}")
    return False

