# Post task questions on model evaluation and comparison

options_likert = ["1 - Disagree", 
                  "2 - Partially disagree", 
                  "3 - Neutral",
                  "4 - Partially agree",
                  "5 - Agree"]

options_model = ["Model 1: Whole image", 
                 "Model 2: RA-severity based patches", 
                 "Model 3: Joint patches"]

options_model_none = ["Model 1: Whole image", 
                      "Model 2: RA-severity based patches", 
                      "Model 3: Joint patches",
                      "None of the models"]

options_model_ve = ["1 - Completely useless: does not explain why the model makes the prediction at all",
                    "2 - Not useful: provides some reasoning but is not helpful",
                    "3 - Neutral: provides some reasoning but I base my judgement mainly on the prediction",
                    "4 - Useful: helpful for explaining why the model makes the prediction",
                    "5 - Highly useful: crucial for my judgement"]


model_comparison_questions = [
    {
        "question_number": 0,
        "question": "Which model do you feel is the most accurate?",
        "options": options_model,
    },
    {
        "question_number": 1,
        "question": "Which model do you feel has the most useful visual explanation (VE)?",
        "options": options_model,
    },
    {
        "question_number": 2,
        "question": "Which model do you feel demonstrates the best performance in score prediction, in terms of both accuracy and explainability?",
        "options": options_model,
    },
    {
        "question_number": 3,
        "question": "Which model do you feel is the easiest to use?",
        "options": options_model,
    },
    {
        "question_number": 4,
        "question": "Which model do you feel is the most trustworthy, i.e., with VE that correctly reflects how it reaches the prediction (accurate prediction & accurate VE or inaccurate prediction & inaccurate VE)?",
        "options": options_model_none,
    },
    {
        "question_number": 5,
        "question": "Which model do you feel is the most deceptive, i.e., with misleading or confusing VE that does not match the prediction (accurate prediction & inaccurate VE or inaccurate prediction & accurate VE)?",
        "options": options_model_none,
    },
]

model_usage_questions = [
    {
        "question_number": 0,
        "question": "The model could be used to score hand radiographs with human review and intervention.",
        "subquestions": options_model,
        "options": options_likert,
    },
    {
        "question_number": 1,
        "question": "The model could replace clinicians when scoring hand radiographs.",
        "subquestions": options_model,
        "options": options_likert,
    },
    {
        "question_number": 2,
        "question": "The model will be useful in clinical diagnosis and monitoring.",
        "subquestions": options_model,
        "options": options_likert,
    },
    {
        "question_number": 3,
        "question": "The visual explanation will be useful if the model is adopted in clinical diagnosis and monitoring.",
        "subquestions": options_model,
        "options": options_likert,
    },
    {
        "question_number": 4,
        "question": "The model will be useful in clinical trials.",
        "subquestions": options_model,
        "options": options_likert,
    },
    {
        "question_number": 5,
        "question": "The visual explanation will be useful if the model is adopted in clinical trials.",
        "subquestions": options_model,
        "options": options_likert,
    }
]

ve_usefulness_question = [
    {
        "question_number": 0,
        "question": "How useful is the visual explanation in helping you assess the accuracy and trustworthiness of a prediction?",
        "subquestions": options_model,
        "options": options_model_ve,
    },
]
