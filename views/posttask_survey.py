import streamlit as st
from PIL import Image
import pathlib
from streamlit_gsheets import GSheetsConnection
from questions.posttask_survey import model_comparison_questions, model_usage_questions, ve_usefulness_question
from utils import nav_bar_visibility,load_css, question_options_display, image_click_pop_static, match_session_record
import numpy as np
import pandas as pd
from datetime import datetime
import pytz

# Load CSS configs
# def load_css(file_path):
#     with open(file_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("./style.css")
load_css(css_path)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# st.write(conn)

# df = conn.read()

# st.text(df.columns.values)

def question_options_display_sub(question, options, default_op = None, val = ''):
    # Set index value
    # options = questions[idx].get("options")
    if val in st.session_state and st.session_state[val] is not None and st.session_state[val] != 'None_':
       select_idx = options.index(st.session_state[val])
    else: select_idx = default_op
    ans = st.radio(question, options, index = select_idx, key = val+'_key')
    return ans
    

def main():
    conn = st.connection("gsheets", type=GSheetsConnection)
    if ('posttask_start' in st.session_state and st.session_state['posttask_start'] == False) or ('posttask_start' not in st.session_state):
    # load google sheet
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        # st.table(df)
        st.cache_data.clear()
        if 'email' in st.session_state:
            st.session_state['new_row'] = match_session_record(df, st.session_state['email'])
        else: st.switch_page('views/introduction.py')
    
    st.session_state['posttask_start'] = True
    st.session_state['task_start'] = True
    st.session_state['pretask_start'] = True
    st.session_state['end_start'] = False
    # Section initiation
    st.session_state['ce_done'] = False
    st.session_state['ae_done'] = False
    st.session_state['ata_done'] = False
    st.session_state['pretask_done'] = False
    st.session_state['task_done'] = False
    st.session_state['posttask_done'] = False
    st.session_state['end_done'] = False

    st.session_state['new_row']['pretask_done'] = True
    st.session_state['new_row']['task_done'] = True
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
    # Reminder of models
    st.subheader("Reminder ...")
    c01, c02, c03 = st.columns(spec = [1/3, 1/3, 1/3],
                        gap = 'small',
                        vertical_alignment='top',
                        border = False)
    with c01:
        st.markdown('Model 1: Whole image', unsafe_allow_html=True)
    with c02:
        st.markdown('Model 2: RA-severity based patches', unsafe_allow_html=True)
    with c03:
        st.markdown('Model 3: Joint patches')
    
    c01, c02, c03 = st.columns(spec = [1/3, 1/3, 1/3],
                        gap = 'small',
                        vertical_alignment='top',
                        border = False)
    with c01:
        image_click_pop_static("app/static/seed171/WI_bar/heatmap_DX207586.jpg", width = 2252)
    with c02:
        image_click_pop_static("app/static/seed171/RP_AMIL_bar/heatmap_DX207586.jpg", width = 2252)
    with c03:
        image_click_pop_static("app/static/seed171/JL_AMIL_bar/heatmap_DX207586.jpg", width = 2252)
    
    def submit_subsection_mve():
            st.session_state['mve_submitted'] = True
    def submit_subsection_mc():
            st.session_state['mc_submitted'] = True
    def submit_subsection_mu():
            st.session_state['mu_submitted'] = True

    # Usefulness of VE
    st.subheader("Usefulness of the visual explanation")
    st.markdown('Based on your experience in using the models ...', unsafe_allow_html=True)
    mve_placeholder = st.empty()

    with mve_placeholder.form(key = 've_usefulness', clear_on_submit=False):
        html_str_ve = f"""
        <style>
        p.a {{
        font: bold {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{ve_usefulness_question[0].get('question')}</p>
        """

        st.markdown(html_str_ve, unsafe_allow_html=True)
        st.session_state['mve1_m1'] = question_options_display_sub(ve_usefulness_question[0].get('subquestions')[0], ve_usefulness_question[0].get('options'), val = 'mve1_m1')
        st.session_state['mve1_m2'] = question_options_display_sub(ve_usefulness_question[0].get('subquestions')[1], ve_usefulness_question[0].get('options'), val = 'mve1_m2')
        st.session_state['mve1_m3'] = question_options_display_sub(ve_usefulness_question[0].get('subquestions')[2], ve_usefulness_question[0].get('options'), val = 'mve1_m3')
        mve_done = st.form_submit_button("Submit", on_click=submit_subsection_mve)

        if 'mve_submitted' in st.session_state and st.session_state['mve_submitted'] == True:
            if None in [st.session_state['mve1_m1'], st.session_state['mve1_m2'], st.session_state['mve1_m3']]:
                st.warning("One or more fields are missing.")
                st.session_state['mve_done'] = False
                st.session_state['mve_submitted'] = False
                st.switch_page('views/posttask_survey.py')
            else: 
                with st.spinner("Saving your answers ... ", show_time=False):
                    st.session_state['mve_done'] = True
                    tz_London = pytz.timezone('Europe/London')
                    currentDateAndTime = datetime.now(tz_London)
                    st.session_state['time_submission'] = currentDateAndTime

                    # Update the dataframe
                    for col in ['mve1_m1', 'mve1_m2', 'mve1_m3', 'time_login', 'time_submission']:
                        st.session_state['new_row'].loc[0, col] = st.session_state[col]
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index() 
                    df = conn.update(worksheet = 'Sheet1', data = df)

                    st.warning('Successfully submitted.')
                    st.session_state['mve_submitted'] = False
                    st.switch_page('views/posttask_survey.py')

        elif 'mve_submitted' in st.session_state and 'mve_done' in st.session_state and st.session_state['mve_done'] == True:
            st.warning("Successfully submitted.")
        
        elif 'mve_submitted' in st.session_state and 'mve_done' in st.session_state and st.session_state['mve_done'] == False:
            if None in [st.session_state['mve1_m1'], st.session_state['mve1_m2'], st.session_state['mve1_m3']]:
                st.warning("One or more fields are missing.")
            else:
                st.warning("Successfully submitted.")

    # Model comparison form
    st.subheader("Model comparison")

    # st.markdown('**Based on your experience of using the models ...**', unsafe_allow_html=True)
    st.markdown('Based on your experience in using the models ...', unsafe_allow_html=True)
    mc_placeholder = st.empty()

    with mc_placeholder.form(key = 'model_compare', clear_on_submit=False):
        # options = questions[1].get("options")
        mc_answs = []
        val_list = ['mc1', 'mc2', 'mc3', 'mc4', 'mc5', 'mc6']
        for i in range(len(model_comparison_questions)):
            st.session_state[f'mc{i+1}'] = question_options_display(model_comparison_questions, i, val = val_list[i])
            mc_answs += [st.session_state[f'mc{i+1}']]
        # mc1, mc2, mc3, mc4, mc5, mc6 = mc_answs
        mc_done = st.form_submit_button("Submit", on_click=submit_subsection_mc)

        if 'mc_submitted' in st.session_state and st.session_state['mc_submitted'] == True:
            if None in mc_answs:
                st.warning("One or more fields are missing.")
                st.session_state['mc_done'] = False
                st.session_state['mc_submitted'] = False
                st.switch_page('views/posttask_survey.py')
            else: 
                with st.spinner("Saving your answers ... ", show_time=False):
                    st.session_state['mc_done'] = True
                    tz_London = pytz.timezone('Europe/London')
                    currentDateAndTime = datetime.now(tz_London)
                    st.session_state['time_submission'] = currentDateAndTime

                    # Update the dataframe
                    for col in ['mc1', 'mc2', 'mc3', 'mc4', 'mc5', 'mc6', 'time_login', 'time_submission']:
                        st.session_state['new_row'].loc[0, col] = st.session_state[col]
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index() 
                    df = conn.update(worksheet = 'Sheet1', data = df)

                    st.warning('Successfully submitted.')
                    st.session_state['mc_submitted'] = False
                    st.switch_page('views/posttask_survey.py')
                
        elif 'mc_submitted' in st.session_state and 'mc_done' in st.session_state and st.session_state['mc_done'] == True:
            st.warning("Successfully submitted.")
        
        elif 'mc_submitted' in st.session_state and 'mc_done' in st.session_state and st.session_state['mc_done'] == False:
            if None in mc_answs:
                st.warning("One or more fields are missing.")
            else:
                st.warning("Successfully submitted.")

    # Model usage form
    st.subheader('Model usage')
    # st.markdown('**To which extent do you agree with the statement?**', unsafe_allow_html=True)
    st.markdown('To which extent do you agree with the statement?', unsafe_allow_html=True)
    # st.write("To which extent do you agree with the statement?")
    mu_placeholder = st.empty()
    with mu_placeholder.form(key = 'model_usage', clear_on_submit=False):
        # # Model - visual explanation usefulness question
        # html_str_ve = f"""
        # <style>
        # p.a {{
        # font: bold {17}px "Source Sans Pro", sans-serif;
        # }}
        # </style>
        # <p class="a">{model_usage_questions[6].get('question')}</p>
        # """

        # # st.markdown(f"{model_usage_questions[0].get('question')}")
        # st.markdown(html_str_ve, unsafe_allow_html=True)
        # st.session_state['mve1_m1'] = question_options_display_sub(model_usage_questions[6].get('subquestions')[0], model_usage_questions[6].get('options'), val = 'mve1_m1')
        # st.session_state['mve1_m2'] = question_options_display_sub(model_usage_questions[6].get('subquestions')[1], model_usage_questions[6].get('options'), val = 'mve1_m2')
        # st.session_state['mve1_m3'] = question_options_display_sub(model_usage_questions[6].get('subquestions')[2], model_usage_questions[6].get('options'), val = 'mve1_m3')


        # # Model usage
        # # st.markdown('To which extent do you agree with the statement?', unsafe_allow_html=True)
        # html_str_intro = f"""
        # <style>
        # p.a {{
        # font: bold {19}px "Source Sans Pro", sans-serif;
        # }}
        # </style>
        # <p class="a">To which extent do you agree with the statement?</p>
        # """
        # st.markdown(html_str_intro, unsafe_allow_html=True)
    
        html_str_0 = f"""
        <style>
        p.a {{
        font: bold {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[0].get('question')}</p>
        """

        # st.markdown(f"{model_usage_questions[0].get('question')}")
        st.markdown(html_str_0, unsafe_allow_html=True)
        st.session_state['mu1_m1'] = question_options_display_sub(model_usage_questions[0].get('subquestions')[0], model_usage_questions[0].get('options'), val = 'mu1_m1')
        st.session_state['mu1_m2'] = question_options_display_sub(model_usage_questions[0].get('subquestions')[1], model_usage_questions[0].get('options'), val = 'mu1_m2')
        st.session_state['mu1_m3'] = question_options_display_sub(model_usage_questions[0].get('subquestions')[2], model_usage_questions[0].get('options'), val = 'mu1_m3')

        # mu_submit = st.form_submit_button("Submit")

        html_str_1 = f"""
        <style>
        p.a {{
        font: 600 {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[1].get('question')}</p>
        """

        # st.markdown(f"{model_usage_questions[1].get('question')}")
        st.markdown(html_str_1, unsafe_allow_html=True)
        st.session_state['mu2_m1'] = question_options_display_sub(model_usage_questions[1].get('subquestions')[0], model_usage_questions[1].get('options'), val = 'mu2_m1')
        st.session_state['mu2_m2'] = question_options_display_sub(model_usage_questions[1].get('subquestions')[1], model_usage_questions[1].get('options'), val = 'mu2_m2')
        st.session_state['mu2_m3'] = question_options_display_sub(model_usage_questions[1].get('subquestions')[2], model_usage_questions[1].get('options'), val = 'mu2_m3')

        html_str_2 = f"""
        <style>
        p.a {{
        font: 600 {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[2].get('question')}</p>
        """
        st.markdown(html_str_2, unsafe_allow_html=True)
        st.session_state['mu3_m1'] = question_options_display_sub(model_usage_questions[2].get('subquestions')[0], model_usage_questions[2].get('options'), val = 'mu3_m1')
        st.session_state['mu3_m2'] = question_options_display_sub(model_usage_questions[2].get('subquestions')[1], model_usage_questions[2].get('options'), val = 'mu3_m2')
        st.session_state['mu3_m3'] = question_options_display_sub(model_usage_questions[2].get('subquestions')[2], model_usage_questions[2].get('options'), val = 'mu3_m3')

        html_str_3 = f"""
        <style>
        p.a {{
        font: 600 {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[3].get('question')}</p>
        """
        st.markdown(html_str_3, unsafe_allow_html=True)
        st.session_state['mu4_m1'] = question_options_display_sub(model_usage_questions[3].get('subquestions')[0], model_usage_questions[3].get('options'), val = 'mu4_m1')
        st.session_state['mu4_m2'] = question_options_display_sub(model_usage_questions[3].get('subquestions')[1], model_usage_questions[3].get('options'), val = 'mu4_m2')
        st.session_state['mu4_m3'] = question_options_display_sub(model_usage_questions[3].get('subquestions')[2], model_usage_questions[3].get('options'), val = 'mu4_m3')

        html_str_4 = f"""
        <style>
        p.a {{
        font: 600 {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[4].get('question')}</p>
        """
        st.markdown(html_str_4, unsafe_allow_html=True)
        st.session_state['mu5_m1'] = question_options_display_sub(model_usage_questions[4].get('subquestions')[0], model_usage_questions[4].get('options'), val = 'mu5_m1')
        st.session_state['mu5_m2'] = question_options_display_sub(model_usage_questions[4].get('subquestions')[1], model_usage_questions[4].get('options'), val = 'mu5_m2')
        st.session_state['mu5_m3'] = question_options_display_sub(model_usage_questions[4].get('subquestions')[2], model_usage_questions[4].get('options'), val = 'mu5_m3')

        html_str_5 = f"""
        <style>
        p.a {{
        font: 600 {17}px "Source Sans Pro", sans-serif;
        }}
        </style>
        <p class="a">{model_usage_questions[5].get('question')}</p>
        """
        st.markdown(html_str_5, unsafe_allow_html=True)
        st.session_state['mu6_m1'] = question_options_display_sub(model_usage_questions[5].get('subquestions')[0], model_usage_questions[5].get('options'), val = 'mu6_m1')
        st.session_state['mu6_m2'] = question_options_display_sub(model_usage_questions[5].get('subquestions')[1], model_usage_questions[5].get('options'), val = 'mu6_m2')
        st.session_state['mu6_m3'] = question_options_display_sub(model_usage_questions[5].get('subquestions')[2], model_usage_questions[5].get('options'), val = 'mu6_m3')

        mu_done = st.form_submit_button("Submit", on_click=submit_subsection_mu)
        # if 'mu_done' in st.session_state and st.session_state['mu_done'] == True:
        #     st.warning("Successfully submitted.")

        if 'mu_submitted' in st.session_state and st.session_state['mu_submitted'] == True:
            if None in [st.session_state['mu1_m1'], st.session_state['mu1_m2'], st.session_state['mu1_m3'],st.session_state['mu2_m1'], st.session_state['mu2_m2'], st.session_state['mu2_m3'],
                        st.session_state['mu3_m1'], st.session_state['mu3_m2'], st.session_state['mu3_m3'],st.session_state['mu4_m1'], st.session_state['mu4_m2'], st.session_state['mu4_m3'],
                        st.session_state['mu5_m1'], st.session_state['mu5_m2'], st.session_state['mu5_m3'],st.session_state['mu6_m1'], st.session_state['mu6_m2'], st.session_state['mu6_m3']]:
                st.warning("One or more fields are missing.")
                st.session_state['mu_done'] = False
                st.session_state['mu_submitted'] = False
                st.switch_page('views/posttask_survey.py')
            else: 
                with st.spinner("Saving your answers ... ", show_time=False):
                    st.session_state['mu_done'] = True
                    tz_London = pytz.timezone('Europe/London')
                    currentDateAndTime = datetime.now(tz_London)
                    st.session_state['time_submission'] = currentDateAndTime

                    # Update the dataframe
                    for col in ['mu1_m1', 'mu1_m2', 'mu1_m3', 'mu2_m1', 'mu2_m2', 'mu2_m3',
                                'mu3_m1', 'mu3_m2', 'mu3_m3', 'mu4_m1', 'mu4_m2', 'mu4_m3',
                                'mu5_m1', 'mu5_m2', 'mu5_m3', 'mu6_m1', 'mu6_m2', 'mu6_m3', 'time_login', 'time_submission']:
                        st.session_state['new_row'].loc[0, col] = st.session_state[col]
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index() 
                    df = conn.update(worksheet = 'Sheet1', data = df)

                    st.warning('Successfully submitted.')
                    st.session_state['mu_submitted'] = False
                    st.switch_page('views/posttask_survey.py')

        elif 'mu_submitted' in st.session_state and 'mu_done' in st.session_state and st.session_state['mu_done'] == True:
            st.warning("Successfully submitted.")
        
        elif 'mu_submitted' in st.session_state and 'mu_done' in st.session_state and st.session_state['mu_done'] == False:
            if None in [st.session_state['mu1_m1'], st.session_state['mu1_m2'], st.session_state['mu1_m3'],st.session_state['mu2_m1'], st.session_state['mu2_m2'], st.session_state['mu2_m3'],
                        st.session_state['mu3_m1'], st.session_state['mu3_m2'], st.session_state['mu3_m3'],st.session_state['mu4_m1'], st.session_state['mu4_m2'], st.session_state['mu4_m3'],
                        st.session_state['mu5_m1'], st.session_state['mu5_m2'], st.session_state['mu5_m3'],st.session_state['mu6_m1'], st.session_state['mu6_m2'], st.session_state['mu6_m3']]:
                st.warning("One or more fields are missing.")
            else:
                st.warning("Successfully submitted.")
    
    if type(st.session_state['fb']) == float and pd.isna(st.session_state['fb']):
        st.session_state['fb'] = st.text_input("**Any feedback** :grey[(please leave any additional comments here)]", '')
    elif 'fb' in st.session_state and st.session_state['fb'] is not None and st.session_state['fb'] != 'None_':
        st.session_state['fb'] = st.text_input("**Any feedback** :grey[(please leave any additional comments here)]", st.session_state['fb'])
    else: st.session_state['fb'] = st.text_input("**Any feedback** :grey[(please leave any additional comments here)]", '')
    

    if st.button("Finish"):
        if 'mc_done' in st.session_state and 'mu_done' in st.session_state and 'mve_done' in st.session_state and st.session_state['mc_done'] and st.session_state['mu_done'] and st.session_state['mve_done']:
            with st.spinner("Saving your answers ... ", show_time=False):
                st.session_state['posttask_done'] = True
                st.session_state['mu_done'] = False
                st.session_state['mc_done'] = False
                st.session_state['mve_done'] = False
                tz_London = pytz.timezone('Europe/London')
                currentDateAndTime = datetime.now(tz_London)
                st.session_state['time_submission'] = currentDateAndTime
                
                # Update the dataframe
                # for col in ['mc1', 'mc2', 'mc3', 'mc4', 'mc5', 'mc6', 'mve1_m1', 'mve1_m2', 'mve1_m3',
                #             'mu1_m1', 'mu1_m2', 'mu1_m3', 'mu2_m1', 'mu2_m2', 'mu2_m3',
                #             'mu3_m1', 'mu3_m2', 'mu3_m3', 'mu4_m1', 'mu4_m2', 'mu4_m3',
                #             'mu5_m1', 'mu5_m2', 'mu5_m3', 'mu6_m1', 'mu6_m2', 'mu6_m3', 'fb', 'posttask_done', 'time_login', 'time_submission']:
                for col in ['fb', 'posttask_done', 'time_login', 'time_submission']:
                    st.session_state['new_row'].loc[0, col] = st.session_state[col]
                df = conn.read()
                st.cache_data.clear()
                st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                df = df.set_index('email')
                df.update(st.session_state['new_row'])
                df = df.reset_index()
                st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    
                df = conn.update(worksheet = 'Sheet1', data = df)
                del st.session_state['mve_submitted']
                del st.session_state['mc_submitted']
                del st.session_state['mu_submitted']
                if 'ce_submitted' in st.session_state: del st.session_state['ce_submitted']
                if 'ae_submitted' in st.session_state: del st.session_state['ae_submitted']
                if 'ata_submitted' in st.session_state: del st.session_state['ata_submitted']
                st.switch_page('views/end_page.py')
        else: 
            st.warning("One or more sections are not submitted.")
            st.session_state['posttask_done'] = False

        

main()
