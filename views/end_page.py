import streamlit as st
import pandas as pd
import os
import base64
import pathlib
from pathlib import Path
from streamlit_gsheets import GSheetsConnection
from utils import nav_bar_visibility,load_css, question_options_display, image_click_pop_static, match_session_record

# Load CSS configs
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("./style.css")
load_css(css_path)

def main():
    # Load the google sheet
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    # st.table(df)
    st.cache_data.clear()
    st.session_state['new_row'] = match_session_record(df, st.session_state['email'])
    # st.session_state['intro_start'] = False
    # st.session_state['pretask_start'] = False
    # st.session_state['task_start'] = False
    # st.session_state['posttask_start'] = False
    # st.session_state['end_start'] = False
    # nav_bar_visibility()
    st.header('End of survey')
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
    
    # st.write(st.session_state['end_done'])

    if st.session_state['end_done'] ==  False or 'end_done' not in st.session_state:
        # st.session_state['intro_start'] = True
        # st.session_state['pretask_start'] = True
        # st.session_state['task_start'] = True
        # st.session_state['posttask_start'] = True
        st.session_state['end_start'] = True

        st.session_state['new_row']['pretask_done'] = True
        st.session_state['new_row']['task_done'] = True
        st.session_state['new_row']['posttask_done'] = True
        st.session_state['new_row']['end_done'] = False
    #     nav_bar_visibility()
    # else: 
    #     st.session_state['intro_start'] = False
    #     st.session_state['pretask_start'] = False
    #     st.session_state['task_start'] = False
    #     st.session_state['posttask_start'] = False
    #     st.session_state['end_start'] = False
        nav_bar_visibility()

        st.markdown("Thank you for completing the survey. Once you are happy with all the answers, please click the “Finish” button below. Once finish, you will not be able to access any previous sections. If you encounter any difficulty during the study or have any questions, here is our contact email: **zhiyan.bo@reuben.ox.ac.uk**.")
        st.markdown("We sincerely appreciate your time and effort.")

        if st.button('Finish'):
            st.session_state['intro_start'] = False
            st.session_state['pretask_start'] = False
            st.session_state['task_start'] = False
            st.session_state['posttask_start'] = False
            st.session_state['end_start'] = False
            st.session_state['end_done'] = True

            # Update the dataframe
            for col in ['end_done']:
                st.session_state['new_row'].loc[0, col] = st.session_state[col]
            df = conn.read()
            st.cache_data.clear()
            st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
            df = df.set_index('email')
            df.update(st.session_state['new_row'])
            df = df.reset_index()
            st.session_state['new_row'] = st.session_state['new_row'].reset_index()
            df = conn.update(worksheet = 'Sheet1', data = df)

            st.switch_page('views/end_page.py')
            nav_bar_visibility()
            # st.write(":red[**Thank you for completing the survey. You can close the browser now.**]")
    else: st.write(":orange[**Thank you for completing the survey. You can close the browser tab now.**]")
    # st.session_state['end_done'] == True or st.session_state['end_done'] == 1



main()