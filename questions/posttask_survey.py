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
    }
]
