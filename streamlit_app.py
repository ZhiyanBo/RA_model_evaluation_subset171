import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# from gsheetsdb import connect

# st.title("Survey.")
# st.write("This is an app for..")

# # Create a connection object.
# conn = st.connection("gsheets", type=GSheetsConnection)
# st.write(st.secrets['connections'])
# st.write(conn)

# df = conn.read()

# st.text(df.columns.values)

def question_options_display(questions, idx, default_op = 2):
    ans = st.radio(questions[idx].get('question'), questions[idx].get("options"), index = default_op)
    return ans

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
intro_page = st.Page(
    "views/introduction.py",
    title="Study overview",
    # icon=":material/account_circle:",
    default=True,
)
pretask_survey_page = st.Page(
    "views/pretask_survey.py",
    title="Initial survey",
    # icon=":material/bar_chart:",
)
task_survey_page = st.Page(
    "views/task_specific_survey.py",
    title="Model evaluation",
    # icon=":material/smart_toy:",
)
posttask_survey_page = st.Page(
    "views/posttask_survey.py",
    title="User experience and feedback",
    # icon=":material/smart_toy:",
)
end_page = st.Page(
    "views/end_page.py",
    title = "End of survey"
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Information": [intro_page],
        "Survey": [pretask_survey_page, task_survey_page, posttask_survey_page],
        "Conclusion": [end_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()