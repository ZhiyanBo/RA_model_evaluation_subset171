# Task specific questions
import streamlit as st
from PIL import Image


questions = [
    {
    "question_number": 1, 
    "question": "How much do you agree with the model's predicted SvdH score?",
    "options": ["1 - Disagree: large prediction error", 
                "2 - Partially disagree: moderate prediction error which cannot be explained by imaging artefacts or other damage likely unrelated to RA", 
                "3 - Neutral: moderate prediction error which can be explained by imaging artefacts or other damage likely unrelated to RA (e.g., sclerosis, osteoarthritis)", 
                "4 - Partially agree: not as accurate as ground truth (GT) but provides useful information on the amount of damage", 
                "5 - Agree: as good as GT"],
    },
    # {
    # "question_number": 2, 
    # "question": "How useful is the visual explanation in helping you decide the accuracy of the prediction?",
    # "options": ["1 - Completely useless: does not explain why the model made the decision at all", 
    #             "2 - Not useful: provides some reasoning but is not helpful", 
    #             "3 - Neutral: provides some reasoning but I based my judgement mainly on the prediction", 
    #             "4 - Useful: helpful for explaining why the model made the decision", 
    #             "5 - Highly useful: crucial for my judgement"],
    # },
    {
    "question_number": 2, 
    "question": "How accurate is the model's identification of damaged structures, as highlighted in the visual explanation? (In a healthy image, how RA-relevant are the highlighted structures?)",
    "options": ["1 - Completely inaccurate: the model fails to identify any damage or representative structures", 
                "2 - Mostly inaccurate: the model only identifies a small proportion of damage while highlighting mostly healthy or irrelevant structures", 
                "3 - Neutral: the model identifies half of the damage while highlighting some healthy or irrelevant structures", 
                "4 - Mostly accurate: the model identifies a large proportion of damage", 
                "5 - Completely accurate: the model identifies all damage while focusing less on healthy and irrelevant structures"],
    },
    {
    "question_number": 3, 
    "question": "To which extent do you agree with the statement: **I fully understand what the visual explanation shows**?",
    "options": ["1 - Disagree: I do not understand how to interpret the heatmap at all", 
                "2 - Partially disagree", 
                "3 - Neutral: I understand how to interpret the heatmap but do not understand how it is related to the prediction", 
                "4 - Partially agree", 
                "5 - Agree: I fully understand how to interpret the heatmap and what it infers about the prediction"],
    },
    ]
