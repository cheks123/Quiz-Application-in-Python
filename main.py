
import random
from string import ascii_lowercase
import pathlib

try:
    import tomllib
except ModuleNotFoundError:
    import tomli

NUM_QUESTIONS_PER_QUIZ = 5
QUESTION_PATH = pathlib.Path(__file__).parent/"questions.toml"

def prepare_questions(path, num_questions):
    questions = tomli.loads(path.read_text())["questions"]
    num_questions = min(num_questions, len(questions))
    return random.sample(questions, k=num_questions)

def get_answer(question, options, num_choices = 1, hint = None):
    print(f"{question}")
    labeled_options = dict(zip(ascii_lowercase, options))

    if hint:
        labeled_options["?"] = "Hint"
    for label, option in labeled_options.items():
        print(f" {label}) {option}")

    while True:
        plural_s = "" if num_choices == 1 else f"s, (choose {num_choices})"
        answer = input(f"\nChoice{plural_s}? ")
        answers = set(answer.replace(","," ").split())

        if hint and "?" in answers:
            print(f"\nHint: {hint}")
            continue

        if len(answers) != num_choices:
            plural_s = "" if num_choices == 1 else "s, separated by comma"
            print(f"Please answer {num_choices} alternative{plural_s}")
            continue

        if any((invalid := answer) not in labeled_options for answer in answers):
            print(f"{invalid!r} is not a valid choice" f"Please use {', '.join(labeled_options)}")
            continue

        return [labeled_options[i] for i in answers]

def ask_question(question):
    correct_answers = question["answers"]
    options = question["answers"] + question["options"]
    ordered_options = random.sample(options, k=len(options))
    hint = question.get("hint")
    explanation = question.get("explanation")

    answers = get_answer(question["question"], ordered_options, len(correct_answers), hint)
    if set(answers) == set(correct_answers):
        print("Correct!")
        score = 1
    else:
        is_or_are = " is" if len(correct_answers) == 1 else "s are"
        print("\n-".join([f"No, the answer{is_or_are}:"] + correct_answers))
        score = 0
    if explanation:
        print(f"\nExplanation: {explanation}")
    return score


def quizApp():
    questions = prepare_questions(QUESTION_PATH, 5)
    number_correct_answers = 0

    for num, question in enumerate(questions, start=1):
        print(f'\nQuestion {num}:')
        number_correct_answers += ask_question(question)

    print(f"\nYou got {number_correct_answers} correct out of {num} questions")


if __name__ == '__main__':
    quizApp()
