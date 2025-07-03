import streamlit as st
from PIL import Image
import pathlib
from questions.task_specific_survey import questions
import base64
import pandas as pd
from utils import nav_bar_visibility,load_css, question_options_display, image_click_pop_static, match_session_record
import numpy as np
import random
from streamlit_gsheets import GSheetsConnection
import ast

# Load CSS configs
css_path = pathlib.Path("./style.css")
load_css(css_path)

# Load sample dataframe
df_samples = pd.read_csv('./static/seed171/GT_predictions_seed171_20250430_rounded.csv')
# df_samples = df_samples.head(2) # Add for testing purposes

# Get name of all answers that are suppose to be in the dictionary
answer_name_list = []
for i in range(len(df_samples)):
    exam_num = df_samples['exam_number'][i]
    for m in range(3):
        answer_name_list += [f'DX{exam_num}_m{m+1}q1', f'DX{exam_num}_m{m+1}q2', f'DX{exam_num}_m{m+1}q3']

# st.write(answer_name_list)

# Display radiograph, heatmap and questions for a sample
def images_questions_display(df, idx):
    gt = df['score_avg'][idx]
    filename = df['filename'][idx]
    exam_num = df['exam_number'][idx]
    dic_answers = {
        f'DX{exam_num}_m1q1': '',
        f'DX{exam_num}_m1q2': '',
        f'DX{exam_num}_m1q3': '',
        f'DX{exam_num}_m2q1': '',
        f'DX{exam_num}_m2q2': '',
        f'DX{exam_num}_m2q3': '',
        f'DX{exam_num}_m3q1': '',
        f'DX{exam_num}_m3q2': '',
        f'DX{exam_num}_m3q3': '',
    }
    predictions = [df['pred_m1'][idx],df['pred_m2'][idx],df['pred_m3'][idx]]
    errors = [df['error_m1'][idx],df['error_m2'][idx],df['error_m3'][idx]]
    st.subheader(f'Image {idx + 1} - SvdH score = {gt}', anchor=f"image{idx+1}")
    # st.sidebar.subheader(f'Image {idx + 1} - SvdH score = {gt}')
    model_list = ['Model 1: Whole image', 'Model 2: RA-severity based patches', 'Model 3: Joint patches']
    dir_list = ['WI_bar', 'RP_AMIL_bar', 'JL_AMIL_bar']
    model_order = [0,1,2]
    random.Random(idx).shuffle(model_order)
    # st.write(model_order)
    for i in range(3):
        # st.write(i)
        model_idx = model_order[i]
        st.markdown(f'<p style="font-size: 26px; font-weight: 600;">({i+1}) {model_list[model_idx]}</p>', unsafe_allow_html=True)
        col1, col2 = st.columns([0.5, 0.5], gap="small", vertical_alignment="top")
        with col1:
            st.markdown('<p style="font-size: 20px; font-weight: 600;">Original image</p>', unsafe_allow_html=True)
            # Colour: A7CEF7
            st.markdown(f'<p style="background-color:#BBDBFC; ">Average SvdH score from clinicians: <strong>{gt}</strong></p>',unsafe_allow_html=True)
            image_click_pop_static(f"app/static/seed171/original_images/{filename}", width=2048)

        with col2:
            st.markdown('<p style="font-size: 20px; font-weight: 600;">Contribution heatmap</p>', unsafe_allow_html=True)
            # st.markdown(f'Model prediction (error): **{predictions[model_idx]} ({errors[model_idx]})**')
            # Colour: F7CDA7, F7D5B8
            st.markdown(f'<p style="background-color:#F7D5B8; ">Model prediction (error): <strong>{predictions[model_idx]} ({errors[model_idx]})</strong></p>',unsafe_allow_html=True)
            image_click_pop_static(f"app/static/seed171/{dir_list[model_idx]}/heatmap_{filename}", width=2252)
        st.markdown(":orange[* Click on images to open them in full size in new browser tabs.]")
        # --- Questions --- #
        question_placeholder = st.empty()
        options_placeholder = st.empty()
        options = questions[0].get("options")
        if f'DX{exam_num}_m{model_idx+1}q1' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q1'] not in [None, 'NA_']:
            index_val = options.index(st.session_state[f'DX{exam_num}_m{model_idx+1}q1'])
        else: 
            index_val = None
            st.session_state[f'DX{exam_num}_m{model_idx+1}q1'] = 'NA_'

        ans1 = options_placeholder.radio(questions[0].get('question'), options, index=index_val, key = f'DX{exam_num}_m{model_idx+1}_q1')
        dic_answers[f'DX{exam_num}_m{model_idx+1}q1'] = ans1
        st.session_state[f'DX{exam_num}_m{model_idx+1}q1'] = ans1

        if f'DX{exam_num}_m{model_idx+1}q1' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q1'] in [None, 'NA_']:
            st.session_state[f'DX{exam_num}_m{model_idx+1}q1'] = 'NA_'
            dic_answers[f'DX{exam_num}_m{model_idx+1}q1'] = 'NA_'

        question_placeholder = st.empty()
        options_placeholder = st.empty()
        options = questions[1].get("options")
        if f'DX{exam_num}_m{model_idx+1}q2' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q2'] not in [None, 'NA_']:
            index_val = options.index(st.session_state[f'DX{exam_num}_m{model_idx+1}q2'])
        else: 
            index_val = None
            st.session_state[f'DX{exam_num}_m{model_idx+1}q2'] = 'NA_'
        
        ans2 = options_placeholder.radio(questions[1].get('question'), options, index=index_val, key = f'DX{exam_num}_m{model_idx+1}_q2')
        dic_answers[f'DX{exam_num}_m{model_idx+1}q2'] = ans2
        st.session_state[f'DX{exam_num}_m{model_idx+1}q2'] = ans2

        if f'DX{exam_num}_m{model_idx+1}q2' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q2'] in [None, 'NA_']:
            st.session_state[f'DX{exam_num}_m{model_idx+1}q2'] = 'NA_'
            dic_answers[f'DX{exam_num}_m{model_idx+1}q2'] = 'NA_'

        question_placeholder = st.empty()
        options_placeholder = st.empty()
        options = questions[2].get("options")
        if f'DX{exam_num}_m{model_idx+1}q3' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q3'] not in [None, 'NA_']:
            index_val = options.index(st.session_state[f'DX{exam_num}_m{model_idx+1}q3'])
        else: 
            index_val = None
            st.session_state[f'DX{exam_num}_m{model_idx+1}q3'] = 'NA_'
        
        ans3 = options_placeholder.radio(questions[2].get('question'), options, index=index_val, key = f'DX{exam_num}_m{model_idx+1}_q3')
        dic_answers[f'DX{exam_num}_m{model_idx+1}q3'] = ans3
        st.session_state[f'DX{exam_num}_m{model_idx+1}q3'] = ans3
        
        if f'DX{exam_num}_m{model_idx+1}q3' in st.session_state and st.session_state[f'DX{exam_num}_m{model_idx+1}q3'] in [None, 'NA_']:
            st.session_state[f'DX{exam_num}_m{model_idx+1}q3'] = 'NA_'
            dic_answers[f'DX{exam_num}_m{model_idx+1}q3'] = 'NA_'

    # st.write(dic_answers)
    return dic_answers

# dic_res = images_questions_display(df_samples, 2)


 # Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()
# st.table(df)
st.cache_data.clear()

# # Change background of scores
# html_scoreBackground = """
# <style>
# .st-emotion-cache-2qp9ou.etvjjhi0 {
# background-color: #F3B381;
# }
# </style>
# """

# st.markdown(html_scoreBackground, unsafe_allow_html=True)

def main(df):
    # if st.session_state['task_start'] == False:
    #     # Create a connection object.
    #     conn = st.connection("gsheets", type=GSheetsConnection)
    #     df = conn.read()
    #     # st.table(df)
    #     st.cache_data.clear()
    
    if 'email' in st.session_state:
        st.session_state['new_row'] = match_session_record(df, st.session_state['email'])
    else: st.switch_page('views/introduction.py')

    st.session_state['task_start'] = True
    st.session_state['pretask_start'] = True
    st.session_state['posttask_start'] = False
    st.session_state['end_start'] = False
    # Section initiation
    st.session_state['ce_done'] = False
    st.session_state['ae_done'] = False
    st.session_state['ata_done'] = False
    st.session_state['mc_done'] = False
    st.session_state['mu_done'] = False
    st.session_state['task_done'] = False
    st.session_state['pretask_done'] = False
    st.session_state['posttask_done'] = False
    st.session_state['end_done'] = False

    st.session_state['new_row']['pretask_done'] = True
    st.session_state['new_row']['task_done'] = False
    st.session_state['new_row']['posttask_done'] = False
    st.session_state['new_row']['end_done'] = False

    # st.markdown(html_scoreBackground, unsafe_allow_html=True)
    
    nav_bar_visibility()
    st.header('Model evaluation')
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
    
    # st.write(st.session_state['new_row'])
    # st.write(ast.literal_eval(st.session_state['eval_all_images'])[0])
    
    task_placeholder = st.empty()
    with task_placeholder.form(key = 'task_form', clear_on_submit=False, border = False):

        dic_all_images = {}
        for img_idx in range(len(df_samples)):
            st.session_state[f'im_{img_idx}_done'] = False
            img_answers = images_questions_display(df_samples, img_idx)
            # st.write()
            # Set image completion status
            if 'NA_' in img_answers.values():
                st.session_state[f'im_{img_idx}_done'] = False
            else: st.session_state[f'im_{img_idx}_done'] = True
            dic_all_images.update(img_answers)

        st.session_state['eval_all_images'] = dic_all_images
    
        # Check if all questions are answered:
        if 'NA_' not in dic_all_images.values():
            st.warning("All questions are completed. Please click on **Finish** to save your answers and proceed to the next section.")
            task_submitted = st.form_submit_button('Finish')

            if task_submitted:
            # if all(name in dic_all_images for name in answer_name_list):
                if 'NA_' not in dic_all_images.values():
                    with st.spinner("Saving your answers ... ", show_time=False):
                        st.session_state['eval_all_images'] = dic_all_images
                        st.session_state['task_done'] = True
                        # Update the dataframe
                        # df_new_row = st.session_state['new_row']
                        # for col in ['eval_all_images', 'task_done']:
                        st.session_state['new_row'].loc[0, 'task_done'] = st.session_state['task_done']
                        st.session_state['new_row'].loc[0, 'eval_all_images'] = [st.session_state['eval_all_images']]
                        # st.session_state['new_row'] = df_new_row
                        df = conn.read()
                        st.cache_data.clear()
                        st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                        df = df.set_index('email')
                        df.update(st.session_state['new_row'])
                        df = df.reset_index()
                        st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                        df = conn.update(worksheet = 'Sheet1', data = df)

                        st.switch_page('views/posttask_survey.py')
                # else: 
                #     st.warning("One or more fields are missing.")
                #     st.session_state['task_done'] = False
                #     unfinished_imgs = 'Images with missing answers: '
                #     for idx in range(len(df_samples)):
                #         if st.session_state[f'im_{idx}_done'] == False:
                #             unfinished_imgs = unfinished_imgs + f"{idx + 1}, "
                #     st.warning(unfinished_imgs[:-2])
        else:
            st.warning("One or more fields are missing")
            st.session_state['task_done'] = False
            unfinished_imgs = 'Images with missing answers: '
            for idx in range(len(df_samples)):
                if st.session_state[f'im_{idx}_done'] == False:
                    unfinished_imgs = unfinished_imgs + f"{idx + 1}, "
            st.warning(unfinished_imgs[:-2])
            task_submitted = st.form_submit_button('Save current answers')
            if task_submitted:
                with st.spinner("Saving your answers ... ", show_time=False):
                    st.session_state['eval_all_images'] = dic_all_images
                    st.session_state['task_done'] = False
                    # Update the dataframe
                    # df_new_row = st.session_state['new_row']
                    # for col in ['eval_all_images', 'task_done']:
                    st.session_state['new_row'].loc[0, 'task_done'] = st.session_state['task_done']
                    st.session_state['new_row'].loc[0, 'eval_all_images'] = [st.session_state['eval_all_images']]
                    # st.session_state['new_row'] = df_new_row
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    # def scroll_to(element_id):


main(df)


# <div class="st-emotion-cache-2qp9ou etvjjhi0">Average SvdH score from clinicians: 1.5</div>
