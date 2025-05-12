import streamlit as st
from PIL import Image
import pathlib
from streamlit_gsheets import GSheetsConnection
from questions.pretask_survey import clinical_expertise_questions, ai_expertise_questions, ai_attitute_questions
from utils import nav_bar_visibility, match_session_record
# import time

# Load CSS configs
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("./style.css")
load_css(css_path)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()
# st.table(df)

# st.text(df.columns.values)

# def question_options_display_n(questions, idx, default_op = 2): # Issue: st.radio label does not display numbers like '1.' or '2.
#     question_str = str(idx+1) + ". " + questions[idx].get('question')
#     ans = st.radio(question_str, questions[idx].get("options"), index = default_op)
#     return ans
    

# def question_options_display(questions, idx, default_op = None):
#     ans = st.radio(questions[idx].get('question'), questions[idx].get("options"), index = default_op)
#     return ans

def question_options_display(questions, idx, default_op = None, val = ''):
    # Set index value
    options = questions[idx].get("options")
    if val in st.session_state and st.session_state[val] is not None and st.session_state[val] != 'None_':
       select_idx = options.index(st.session_state[val])
    else: select_idx = default_op
    ans = st.radio(questions[idx].get('question'), questions[idx].get("options"), index = select_idx)
    return ans

# def default_or_val(questionsdefault, val):
#     if val in st.session_state:
#         val_str = st.session_state[val]
#         return .index(st.session_state[val])
#     else: return default

def main():
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    # st.table(df)
    st.cache_data.clear()
    # st.write(st.session_state)
    # st.write(df['email'])
    # st.write(st.session_state['email'])
    st.session_state['new_row'] = match_session_record(df, st.session_state['email'])

    # Sidebar navigation
    st.session_state['pretask_start'] = True
    st.session_state['task_start'] = False
    st.session_state['posttask_start'] = False
    st.session_state['end_start'] = False
    # Section initiation
    st.session_state['mc_done'] = False
    st.session_state['mu_done'] = False
    st.session_state['task_done'] = False
    st.session_state['pretask_done'] = False
    st.session_state['posttask_done'] = False
    st.session_state['end_done'] = False

    st.session_state['new_row']['pretask_done'] = False
    st.session_state['new_row']['task_done'] = False
    st.session_state['new_row']['posttask_done'] = False
    st.session_state['new_row']['end_done'] = False

    nav_bar_visibility()
    st.markdown("""
                <html>
                    <head>
                    <style>
                        ::-webkit-scrollbar {
                            width: 15px;
                            }

                            /* Track */
                            ::-webkit-scrollbar-track {
                            background: #f1f1f1;
                            }

                            /* Handle */
                            ::-webkit-scrollbar-thumb {
                            background: #888;
                            }

                            /* Handle on hover */
                            ::-webkit-scrollbar-thumb:hover {
                            background: #555;
                            }
                    </style>
                    </head>
                    <body>
                    </body>
                </html>
            """, unsafe_allow_html=True)
    

    # Clinical expertise form
    st.subheader("Clinical expertise")
    ce_placeholder = st.empty()
    with ce_placeholder.form(key = 'clinical_expertise', clear_on_submit=False):
        # options = questions[1].get("options")
        # for i in range(len(clinical_expertise_questions)):
        st.session_state['ce1'] = question_options_display(clinical_expertise_questions, 0, val = 'ce1')
        st.session_state['ce2'] = question_options_display(clinical_expertise_questions, 1, val = 'ce2')
        st.session_state['ce3'] = question_options_display(clinical_expertise_questions, 2, val = 'ce3')
        st.session_state['ce4'] = question_options_display(clinical_expertise_questions, 3, val = 'ce4')

        ce_done = st.form_submit_button("Submit")
        # if 'ce_done' in st.session_state and st.session_state['ce_done'] == True:
        #     st.warning("Successfully submitted.")

        if ce_done:
            if None in [st.session_state['ce1'],st.session_state['ce2'], st.session_state['ce3'], st.session_state['ce4']]:
                st.warning("One or more fields are missing.")
                st.session_state['ce_done'] = False
            else: 
                st.session_state['ce_done'] = True
                st.warning("Successfully submitted.")
        elif 'ce_done' in st.session_state and st.session_state['ce_done'] == True:
            st.warning("Successfully submitted.")
    
    # AI expertise form
    st.subheader("AI expertise")
    st.write("To which extent do you agree with the statement?")
    ae_placeholder = st.empty()
    with ae_placeholder.form(key = 'ai_expertise', clear_on_submit=False):
        # options = questions[1].get("options")
        # for i in range(len(clinical_expertise_questions)):
        st.session_state['ae1'] = question_options_display(ai_expertise_questions, 0, val = 'ae1')
        st.session_state['ae2'] = question_options_display(ai_expertise_questions, 1, val = 'ae2')
        st.session_state['ae3'] = question_options_display(ai_expertise_questions, 2, val = 'ae3')
        st.session_state['ae4'] = question_options_display(ai_expertise_questions, 3, val = 'ae4')

        ae_done = st.form_submit_button("Submit")
        # if 'ae_done' in st.session_state and st.session_state['ae_done'] == True:
        #     st.warning("Successfully submitted.")

        if ae_done:
            if None in [st.session_state['ae1'],st.session_state['ae2'], st.session_state['ae3'], st.session_state['ae4']]:
                st.warning("One or more fields are missing.")
                st.session_state['ae_done'] = False
            else: 
                st.session_state['ae_done'] = True
                st.warning("Successfully submitted.")
        elif 'ae_done' in st.session_state and st.session_state['ae_done'] == True:
            st.warning("Successfully submitted.")

    # Attitude towards AI form
    st.subheader("Attitude towards AI")
    ata_placeholder = st.empty()
    with ata_placeholder.form(key = 'ata_form', clear_on_submit=False):
        # options = questions[1].get("options")
        # for i in range(len(clinical_expertise_questions)):
        st.session_state['ata1'] = question_options_display(ai_attitute_questions, 0, val = 'ata1')
        st.session_state['ata2'] = question_options_display(ai_attitute_questions, 1, val = 'ata2')

        ata_done = st.form_submit_button("Submit")
        # if 'ata_done' in st.session_state and st.session_state['ata_done'] == True:
        #     st.warning("Successfully submitted.")

        if ata_done:
            if None in [st.session_state['ata1'], st.session_state['ata2']]:
                st.warning("One or more fields are missing.")
                st.session_state['ata_done'] = False
            else: 
                st.session_state['ata_done'] = True
                st.warning("Successfully submitted.")
        elif 'ata_done' in st.session_state and st.session_state['ata_done'] == True:
            st.warning("Successfully submitted.")
    
    if st.button("Finish"):
        if ('ce_done' in st.session_state) and ('ae_done' in st.session_state) and ('ata_done' in st.session_state) and (st.session_state['ce_done'] and st.session_state['ae_done'] and st.session_state['ata_done']):
            with st.spinner("Loading the images for review may take time. Thank you for your patience.", show_time=False):
                st.session_state['pretask_done'] = True
                st.session_state['ce_done'] = False
                st.session_state['ae_done'] = False
                st.session_state['ata_done'] = False
                # Update the dataframe
                for col in ['ce1', 'ce2', 'ce3', 'ce4', 'ae1', 'ae2', 'ae3', 'ae4', 'ata1', 'ata2', 'pretask_done']:
                    st.session_state['new_row'].loc[0, col] = st.session_state[col]
                    # st.write(st.session_state['new_row'])
                # st.session_state['new_row']['pretask_done'] = 'True'
                df = conn.read()
                st.cache_data.clear()
                st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                df = df.set_index('email')
                df.update(st.session_state['new_row'])
                df = df.reset_index()
                st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    
                # st.write(df[df['email'] == st.session_state['email']])
                df = conn.update(worksheet = 'Sheet1', data = df)
                st.switch_page('views/task_specific_survey.py')

        else: 
            st.warning("One or more sections are not submitted.")
            # st.write([st.session_state['ce_done'], st.session_state['ae_done'], st.session_state['ata_done']])
            st.session_state['pretask_done'] = False

        # st.write(f"Email: {st.session_state['email']}; CE1: {st.session_state['ce1']}")

main()

# '''

# form2 = st.form(key='form2')
# username = form2.text_input("Username")
# jobtype = form2.selectbox("Job",["Dev","Data Scientist","Doctor"])
# submit_button2 = form2.form_submit_button("Login")


# def main():
#     for _, _ in zip(qs1, qs2): 
#         placeholder = st.empty()
#         num = st.session_state.num
#         with placeholder.form(key=str(num)):
#             st.radio(qs1[num][0], key=num+1, options=qs1[num][1])
#             st.radio(qs2[num][0], key=num+1, options=qs2[num][1])          
                      
#             if st.form_submit_button():
#                 st.session_state.num += 1
#                 if st.session_state.num >= 3:
#                     st.session_state.num = 0 
#                 placeholder.empty()
#             else:
#                 st.stop()


# main()



# question_placeholder = st.empty()
# options_placeholder = st.empty()
# # question_placeholder.write(f"**{questions[1].get('question')}**") 
# options = questions[1].get("options")
# ans2 = options_placeholder.radio(questions[1].get('question'), options, index=2,)

# st.text(f'Answer: {ans2}')'

# '''