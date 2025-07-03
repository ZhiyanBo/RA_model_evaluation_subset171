import streamlit as st
from PIL import Image
import pathlib
import os
from streamlit_gsheets import GSheetsConnection
import ast
# from streamlit import _RerunData, _RerunException
# from streamlit.source_util import get_pages


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def question_options_display(questions, idx, default_op = None, val = ''):
    # Set index value
    options = questions[idx].get("options")
    if val in st.session_state and st.session_state[val] is not None and st.session_state[val] != 'None_':
       select_idx = options.index(st.session_state[val])
    else: select_idx = default_op
    ans = st.radio(questions[idx].get('question'), questions[idx].get("options"), index = select_idx)
    return ans

def image_click_pop_static(path: str, width = 2048):
    html_string = f'<a href="{path}" target="_blank"><img src="{path}" width="{width}" caption="legend"></a>'
    # # Display the image using `st.markdown`
    st.markdown(html_string, unsafe_allow_html=True)


# def nav_bar_visibility():
#     # st.write('NAV_bar')
#     st.write(st.session_state)
#     if st.session_state['intro_start'] == True:
#         # st.write("Intro done")
#         st.sidebar.page_link('views/introduction.py', label='Study overview')
#         # st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
#     if st.session_state['pretask_start'] == True:
#         # st.sidebar.page_link('views/introduction.py', label='Study overview')
#         st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
#         # st.sidebar.page_link('views/task_specific_survey.py', label='Model evaluation')
#     if st.session_state['task_start'] == True:
#         # st.sidebar.page_link('views/introduction.py', label='Study overview')
#         # st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
#         st.sidebar.page_link('views/task_specific_survey.py', label='Model evaluation')
#     if st.session_state['posttask_start'] == True:
#         # st.sidebar.page_link('views/introduction.py', label='Study overview')
#         # st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
#         # st.sidebar.page_link('views/task_specific_survey.py', label='Model evaluation')
#         st.sidebar.page_link('views/posttask_survey.py', label='User experience and feedback')
#     if st.session_state['end_start'] == True:
#         # st.sidebar.page_link('views/introduction.py', label='Study overview')
#         # st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
#         # st.sidebar.page_link('views/task_specific_survey.py', label='Model evaluation')
#         # st.sidebar.page_link('views/posttask_survey.py', label='User experience and feedback')
#         st.sidebar.page_link('views/end_page.py', label='End of survey')
#     # else: st.write("Start")

def nav_bar_visibility():
    # st.write('NAV_bar')
    # st.write(st.session_state)
    if st.session_state['intro_start'] == True:
        st.sidebar.page_link('views/introduction.py', label='Study overview')
    if ('pretask_start' in st.session_state and st.session_state['pretask_start'] == True) or ('new_row' in st.session_state and st.session_state['new_row']['pretask_done'][0] in [1, True, 'TRUE']):
        st.sidebar.page_link('views/pretask_survey.py', label='Initial survey')
    # if 'new_row' in st.session_state and st.session_state['new_row']['pretask_done'][0] == 1:
    #     st.sidebar.page_link('views/pretask_survey.py', label='Clinical expertise & Perspective on AI')
    if ('task_start' in st.session_state and st.session_state['task_start'] == True) or ('new_row' in st.session_state and st.session_state['new_row']['task_done'][0] in [1, True, 'TRUE']):
        st.sidebar.page_link('views/task_specific_survey.py', label='Model evaluation')
        st.sidebar.markdown('''
                        - [Image 1](#image1)
                        - [Image 2](#image2)
                        - [Image 3](#image3)
                        - [Image 4](#image4)
                        - [Image 5](#image5)
                        - [Image 6](#image6)
                        - [Image 7](#image7)
                        - [Image 8](#image8)
                        - [Image 9](#image9)
                        - [Image 10](#image10)
                        ''', unsafe_allow_html=True)
    if ('posttask_start' in st.session_state and st.session_state['posttask_start'] == True) or ('new_row' in st.session_state and st.session_state['new_row']['posttask_done'][0]in [1, True, 'TRUE']):
        st.sidebar.page_link('views/posttask_survey.py', label='User experience and feedback')
    # if ('end_start' in st.session_state and st.session_state['end_start'] == True) or ('new_row' in st.session_state and st.session_state['new_row']['end_done'][0] in [1, True, 'TRUE']):
    if 'end_start' in st.session_state and st.session_state['end_start'] == True:
        st.sidebar.page_link('views/end_page.py', label='End of survey')
    # else: st.write("Start")

#### Match session_state values with google sheet value

# def match_session_record(df, email):
#     df_user = df[df['email'] == email].reset_index()
#     colnames = df.columns
#     st.session_state['new_row'] = df_user
#     for col in colnames:
#         st.session_state[col] = df_user[col][0]
#     for col in ['pretask_done', 'posttask_done', 'task_done', 'end_done']:
#         # st.write(df_user[col])
#         if df_user[col][0] == 'TRUE' or df_user[col][0] == 1 or df_user[col][0] == True:
#             st.session_state[col] = True
#         else: st.session_state[col] = False
#     st.session_state['eval_all_images'] = ast.literal_eval(st.session_state['eval_all_images'])[0]
#     # st.session_state['fb'] = str(st.session_state['fb'])
#     if 'new_row' not in st.session_state:
#         st.session_state['new_row'] = df_user
#         st.session_state['new_row']['eval_all_images'] = ast.literal_eval(st.session_state['new_row']['eval_all_images'])
#         st.session_state['eval_all_images'] = st.session_state['new_row']['eval_all_images'][0]
#     if df_user['task_done'][0] == 1 or df_user['task_done'][0] == True:
#         for k in list(st.session_state['eval_all_images'].keys()):
#             st.session_state[k] = st.session_state['eval_all_images'][k]
#     # elif df_user['']
#     return df_user

all_model_questions = []
for img in os.listdir('static/seed171/original_images'):
    for i in range(3):
        for j in range(2):
            all_model_questions += [f"{img[:-4]}_m{i+1}q{j+1}"]

def match_session_record(df, email, all_model_questions = all_model_questions):
    # all_model_questions = ['DX320829_m1q1', 'DX320829_m1q2', 'DX320829_m2q1', 'DX320829_m2q2', 'DX320829_m3q1', 'DX320829_m3q2', 
    #                         'DX424309_m1q1', 'DX424309_m1q2', 'DX424309_m2q1', 'DX424309_m2q2', 'DX424309_m3q1', 'DX424309_m3q2']
    df_user = df[df['email'] == email].reset_index()
    colnames = df.columns
    # Update new_row
    st.session_state['new_row'] = df_user
    for col in colnames:
        st.session_state[col] = df_user[col][0]
    for col in ['pretask_done', 'posttask_done', 'task_done', 'end_done']:
        # st.write(df_user[col])
        if df_user[col][0] == 'TRUE' or df_user[col][0] == 1 or df_user[col][0] == True:
            st.session_state[col] = True
        else: st.session_state[col] = False
    # Update eval_all_images
    st.session_state['eval_all_images'] = ast.literal_eval(st.session_state['eval_all_images'])[0]
    st.session_state['new_row'].loc[0, 'eval_all_images'] = [st.session_state['eval_all_images']]
    # st.write(f"Eval all images: {st.session_state['new_row'].loc[0, 'eval_all_images']}")
    if st.session_state['new_row'].loc[0, 'eval_all_images'] == [{'task': False}] and any(key in st.session_state for key in all_model_questions):
        for k in all_model_questions:
            st.session_state[k] = 'NA_'
    elif df_user['task_done'][0] == 1 or df_user['task_done'][0] == True:
        for k in list(st.session_state['eval_all_images'].keys()):
            st.session_state[k] = st.session_state['eval_all_images'][k]
    elif st.session_state['new_row'].loc[0, 'eval_all_images'] != [{'task': False}]:
        for k in list(st.session_state['eval_all_images'].keys()):
            st.session_state[k] = st.session_state['eval_all_images'][k]
    # st.write(st.session_state)
    return df_user
