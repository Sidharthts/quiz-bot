
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id):

    '''
    Validates and stores the answer for the current question to session.
    '''

    
    question = None
    for q in PYTHON_QUESTION_LIST:
        if q["id"] == current_question_id:
            question = q
            break

    if not question:
        return False, "Question not found in the question list."

    if not isinstance(answer, str):
        return False, "Invalid answer format. Please provide a string."

    if not answer.strip():
        return False, "Answer cannot be empty."

 
    session["answers"] = session.get("answers", {})
    session["answers"][current_question_id] = answer
    return True, ""
def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    current_question_index = -1
    for i, q in enumerate(PYTHON_QUESTION_LIST):
        if q["id"] == current_question_id:
            current_question_index = i
            break

    if current_question_index == -1 or current_question_index == len(PYTHON_QUESTION_LIST) - 1:
        return None, -1



    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    user_answers = session.get("answers", {})

    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for q in PYTHON_QUESTION_LIST:
        question_id = q["id"]
        correct_answer = q["answer"]
        user_answer = user_answers.get(question_id, None)

        if user_answer is not None and user_answer.lower() == correct_answer.lower():
            correct_answers += 1

    score_percentage = (correct_answers / total_questions) * 100

    final_response = f"Congratulations! You have completed the Python quiz.\n"
    final_response += f"Your score: {score_percentage:.2f}% ({correct_answers}/{total_questions} correct answers).\n"
    
    if score_percentage == 100:
        final_response += "You got a perfect score! Great job!"
    elif score_percentage >= 70:
       


    return "dummy result"
