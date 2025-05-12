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
    {
    "question_number": 2, 
    "question": "How useful is the visual explanation in helping you decide the accuracy of the prediction?",
    "options": ["1 - Completely useless: does not explain why the model made the decision at all", 
                "2 - Not useful: provides some reasoning but is not helpful", 
                "3 - Neutral: provides some reasoning but I based my judgement mainly on the prediction", 
                "4 - Useful: helpful for explaining why the model made the decision", 
                "5 - Highly useful: crucial for my judgement"],
    },
    ]