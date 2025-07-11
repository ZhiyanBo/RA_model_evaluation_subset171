import streamlit as st
import pandas as pd
import os
import base64
import pathlib
from pathlib import Path
# from util import switch_page
# from streamlit_extras.switch_page_button import switch_page 
from streamlit_gsheets import GSheetsConnection
import gspread
from utils import nav_bar_visibility, match_session_record
import streamlit.components.v1 as components
from datetime import datetime
import pytz

# Load CSS configs
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("./style.css")
load_css(css_path)

# st.write(st.session_state)

def main():
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet = 'Sheet1')
    st.cache_data.clear()
    if 'email' not in st.session_state: 
        st.session_state['email'] = ''
    else: st.session_state['email'] = st.session_state['email']


    # conn = st.connection("gsheets", type=GSheetsConnection)
    # # st.write(conn)
    # if ('intro_start' not in st.session_state) or ('intro_done' not in st.session_state) or ('intro_done' in st.session_state and st.session_state['intro_done'] == False):
    #     # st.write("Fresh start")
    #     df = conn.read(worksheet = 'Sheet1')
    #     # df = pd.DataFrame(df)
    #     # st.table(df)
    #     st.cache_data.clear()
    #     if 'email' not in st.session_state: 
    #         st.session_state['email'] = ''
    #     else: st.session_state['email'] = st.session_state['email']


    # # https://discuss.streamlit.io/t/cannot-display-imagecolumns-with-streamlit/50957 - add local images to table
    # def open_image(path: str): # This function works in safari
    #     with open(path, "rb") as p:
    #         file = p.read()
    #         return f"data:image/png;base64,{base64.b64encode(file).decode()}"

    # def open_image(img_path):
    #     img_bytes = Path(img_path).read_bytes()
    #     encoded = base64.b64encode(img_bytes).decode()
    #     return f"data:image/png;base64,{encoded}"

    # # Display image, will open the image in a new tab if click on it
    # # https://discuss.streamlit.io/t/how-to-zoom-st-image/41222
    # def image_click_pop(path: str, width = 2048):
    #     img_path_n = open_image(path)
    #     # Define the HTML hyperlink with the image
    #     html_string = f'<a href="{img_path_n}" target="_blank"><img src="{img_path_n}" width="{width}" caption="legend"></a>'
    #     # Display the image using `st.markdown`
    #     st.markdown(html_string, unsafe_allow_html=True)

    # https://discuss.streamlit.io/t/how-to-zoom-st-image/41222 - click on an image in ./static to open it in a new tab
    def image_click_pop_static(path: str, width = 2048):
        html_string = f'<a href="{path}" target="_blank"><img src="{path}" width="{width}" caption="legend"></a>'
        # # Display the image using `st.markdown`
        st.markdown(html_string, unsafe_allow_html=True)

    # Intro start
    st.session_state['intro_start'] = True

    nav_bar_visibility()


    st.title("Study overview")
    # st.write("This is an app for..")

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

    # st.text(os.getcwd())
    # st.write(st.session_state)

    # st.session_state['pretask_start'] = False
    # st.session_state['task_start'] = False
    # st.session_state['posttask_start'] = False
    # st.session_state['end_start'] = False


    col1, col2 = st.columns(spec = [0.4, 0.6], gap="small", vertical_alignment="center")

    # st.markdown("""
    #     <style>
    #     [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
    #         gap: 0rem;
    #     }
    #     </style>
    #     """,unsafe_allow_html=True)

    with col1:
        # https://discuss.streamlit.io/t/image-in-markdown/13274/10 - to load image in markdown
        # st.image("./data/original_images/DX207586.jpg", width=2048)
        # img_path = "file:///Users/zhiyb/Documents/DPhil/yr2/Clinician_evaluation_study/streamlit_survey_v1/data/original_images/DX207586.jpg"
        # img_path = "./data/original_images/DX207586.jpg"
        # img_path_n = open_image(img_path)
        # # Define the HTML hyperlink with the image
        # html_string = f'<a href="{img_path_n}" target="_blank"><img src="{img_path_n}" width="2048" caption="legend"></a>'
        # # Display the image using `st.markdown`
        # st.markdown(html_string, unsafe_allow_html=True)

        # image_click_pop("./data/original_images/DX207586.jpg")

        image_click_pop_static("app/static/seed171/original_images/DX207586.jpg", 2252)

        # img_link= "app/static/seed171/original_images/DX207586.jpg"
        # html_string = f'<a href="{img_link}" target="_blank"><img src="{img_link}" width="{2048}" caption="legend"></a>'
        # # # Display the image using `st.markdown`
        # st.markdown(html_string, unsafe_allow_html=True)
        # st.markdown("[![Click me](app/static/original_images/DX207586.jpg)](https://streamlit.io)")



    with col2:
        # st.subheader("Attention heatmap", anchor=False)
        st.text('This study aims to assess the performance of three deep learning (DL) '
        'pipelines in Sharp/van der Heijde (SvdH) scoring of dual-hand radiographs from '
        'healthy individuals or rheumatoid arthritis (RA) patients.')
        st.text('It consists of three sections:')
        # st.write("""- Clinical expertise and perspective on AI
        #          <br>""", unsafe_allow_html=True)
        # st.markdown("- Model evaluation")
        # st.markdown("- User experience and feedback")
        # st.markdown('''
        #             <style>
        #             [data-testid="stMarkdownContainer"] ul{
        #                 list-style-position: inside;
        #             }
        #             </style>
        #             ''', unsafe_allow_html=True)
        # https://discuss.streamlit.io/t/how-to-reduce-line-spacing-in-bulleted-list-in-streamlit/47350/2 - to create bullet point list
        st.write('''
                - Initial survey
                - Model evaluation
                - User experience and feedback
                ''')

    st.text("In the first section, you will be asked to complete a survey on your past experience in performing SvdH scoring, " \
    "your general knowledge about artificial intelligence (AI), and your experience using AI-based tools.")

    st.text("After finishing the initial survey, you will be asked to assess the performance of three DL models in scoring 10 radiographs " \
    "of varying RA severity. The models (see table below) adopt different designs and inputs, so they may demonstrate different predictive accuracies in different images.")


    # df_models = pd.DataFrame(
    #     {
    #         'model': [1, 2, 3],
    #         'pipeline_design': ['The model takes a whole dual-hand radiograph as input for score prediction.',
    #                             'The image is first split into equal-size non-overlapping tiles. Intelligent '
    #                             'sampling is then performed to extract tiles most likely to contain damage, which are then fed into the final model for prediction.',
    #                             'Joint detection is first performed to extract joint patches, which are then fed into the final model for prediction.'],
    #         'visual_explanation': ["/Users/zhiyb/Documents/DPhil/yr2/Clinician_evaluation_study/streamlit_survey_v1/data/WI/heatmap_DX207586.jpg", 
    #                                '/Users/zhiyb/Documents/DPhil/yr2/Clinician_evaluation_study/streamlit_survey_v1/data/RP_AMIL/heatmap_DX207586.jpg',
    #                                '/Users/zhiyb/Documents/DPhil/yr2/Clinician_evaluation_study/streamlit_survey_v1/data/JL_AMIL/heatmap_DX207586.jpg',]
    #     }
    # )


    # df_models["VE_image"] = df_models.apply(lambda x: open_image(x["visual_explanation"]), axis=1)
    # df_models = df_models.drop(columns = ['visual_explanation'])


    # st.dataframe(
    #     df_models,
    #     column_config={
    #         "model": "Model",
    #         "pipeline_design": "Pipeline design",
    #         "VE_image": st.column_config.ImageColumn("Visual explanation", width=512),
    #     },
    #     hide_index=True,
    # )

    # st.markdown(
    #     f""" 
    #         <style>
    #         .element-container:has(iframe[height="0"]) {{
    #           display: none;
    #         }}
    #         </style>
    #     """, unsafe_allow_html=True
    # )

    # st.markdown("""
    # <style>
    # .big-font {
    #     # font-size:50px;
    #     font-weight:bold;
    # }
    # </style>
    # """, unsafe_allow_html=True)
    st.markdown(":orange[* Click on an image to open it in full size in a new browser tab.]")
    # html_horizontal_line = f"""
    #         <style>
    #         p.a {{
    #         font: {1}px "Source Sans Pro", sans-serif;
    #         color: black;
    #         padding-top: 0rem;
    #         }}
    #         </style>
    #         <p class="a"><hr></p>
    #         """
    # html_horizontal_line = """<hr width="100%;" color="red" size="5">"""
    # st.markdown("""---""", unsafe_allow_html=True)
    # st.markdown("""<div class="stElementContainer element-container st-emotion-cache-kj6hex eu6p4el1;height:10px" data-testid="stElementContainer" data-stale="false" font-size="1px"><div class="stMarkdown" data-testid="stMarkdown"><div data-testid="stMarkdownContainer" class="st-emotion-cache-16tyu1 e194bff00" font-size="1px"><hr></div></div></div>""", unsafe_allow_html=True)
    # st.markdown(html_horizontal_line, unsafe_allow_html=True)
    # st.divider()
    # st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;line-height:50%" /> """, unsafe_allow_html=True) 
    # st.markdown("""<p class="horizontal-line"><hr style="height:1px;border:none;color:#333;background-color:#333;line-height:50%" /></p>""", unsafe_allow_html=True) 
    # st.components.v1.html("""<hr style="height:1px;border:none;color:#E0E0E0;background-color:#E0E0E0;color-scheme:light"> """)
    # st.markdown("""
    # <style>

    # .st-emotion-cache-kj6hex.eu6p4el1 {
    #     padding: 0;
    #     margin: 0;
    #     height: 50px; 
    # }

    # </style>
    # """, unsafe_allow_html=True)

    st.markdown("""---""", unsafe_allow_html=True)

    # st.markdown("""
    # <style>

    # .st-emotion-cache-kj6hex.eu6p4el1 {
    #     padding: 0;
    #     margin: 0;
    #     height: 100px; 
    # }

    # </style>
    # """, unsafe_allow_html=True)

    c01, c02, c03 = st.columns(spec = [0.15, 0.5, 0.35],
                            gap = 'small',
                            vertical_alignment='top',
                            border = False)
    with c01:
        st.markdown('**Model**', unsafe_allow_html=True)
    with c02:
        st.markdown('**Pipeline design**')
    with c03:
        st.markdown('**XAI method (contribution heatmap)**')
        # st.markdown('**Visual explanation**')

    # st.markdown(f"""
    #     <style>
    #         .reportview-container .main .block-container{{
    #             padding-top: {0}rem;
    #         }}
    #     </style>""",
    #     unsafe_allow_html=True,
    # )
    # st.write("""___""", unsafe_allow_html=True)

    c11, c12, c13 = st.columns(spec = [0.15, 0.5, 0.35],
                            gap = 'small',
                            vertical_alignment='top',
                            border = False)
    with c11:
        st.text('Model 1:\nWhole image')
    with c12:
        st.text('The model takes a whole dual-hand radiograph as input to predict the total SvdH score.')
    with c13:
        # st.image("./data/WI_bar/heatmap_DX207586.jpg", width=2048)
        image_click_pop_static("app/static/seed171/WI_bar/heatmap_DX207586.jpg", width = 2252)

    # c11, c12, c13, c14 = st.columns(spec = [0.15, 0.4, 0.34, 0.06],
    #                         gap = 'small',
    #                         vertical_alignment='top',
    #                         border = False)
    # with c11:
    #     st.text('Model 1')
    # with c12:
    #     st.text('The model takes a whole dual-hand radiograph as input for score prediction.')
    # with c13:
    #     st.image("./data/WI/heatmap_DX207586.jpg", width=2048)
    # with c14:
    #     st.image('./data/attention_map_scale_bar_v1_vertical.png')

    # st.markdown("""---""")
    c21, c22, c23 = st.columns(spec = [0.15, 0.5, 0.35],
                            gap = 'small',
                            vertical_alignment='top',
                            border = False)
    with c21:
        st.text('Model 2:\nRA-severity based patches')
    with c22:
        st.text('The model adopts an intelligent image tile sampling mechanism to predict the total SvdH score.')
    with c23:
        # st.image("./data/RP_AMIL_bar/heatmap_DX207586.jpg", width=2048)
        image_click_pop_static("app/static/seed171/RP_AMIL_bar/heatmap_DX207586.jpg", width = 2252)

    # st.markdown("""---""")
    c31, c32, c33 = st.columns(spec = [0.15, 0.5, 0.35],
                            gap = 'small',
                            vertical_alignment='top',
                            border = False)
    with c31:
        st.text('Model 3:\nJoint patches')
    with c32:
        st.text('The model adopts a joint detection mechanism to predict the total SvdH score.')
    with c33:
        # st.image("./data/JL_AMIL_bar/heatmap_DX207586.jpg", width=2048)
        image_click_pop_static("app/static/seed171/JL_AMIL_bar/heatmap_DX207586.jpg", width = 2252)
    st.markdown("""---""")
    # st.components.v1.html("""<hr style="height:2px;color:#333;background-color:#333;">""")

    # st.text("The ground truth SvdH score, calculated by averaging the score reported by two experienced radiologists, will be provided alongside the model prediction. " \
    # "A visual explanation of the prediction in the form of a contribution heatmap will be provided for each image and model. " \
    # "The regions or patches that contribute more to the prediction are more highlighted in the heatmap, as shown by the colour bar placed on the right. " \
    # "Please examine both the predicted score and the visual explanation when assessing the model. Clicking on the radiograph or heatmap will open the enlarged image in " \
    # "a new browser tab for you to check its details. You can always return to the survey by navigating back to the original browser tab. ")
    st.write('''For each image and model, these details will be provided to facilitate your judgement of the model's performance:''')

    st.write('''
                - Ground truth SvdH score (average of the scores reported by two experienced radiologists) and the model's prediction
                - A visual explanation of how the model made the prediction in the form of a contribution heatmap (see XAI in the table above) where the regions or patches that contribute more to the prediction, which can be healthy or damaged depending on the sample’s symptom, are highlighted in the heatmap (shown by the colour bar placed on the right)
            ''')

    st.write('Please examine both the score and the visual explanation when assessing the models. ')

    st.text("The last section includes a few questions on the overall performance of the models, the usefulness of the adopted explainable AI (XAI) methods, and their potential application. " \
    "We would be grateful for any additional feedback and comments which can be left at the end of the survey.")

    # st.text("Please avoid going back to the previous page or forth to the next page using browser buttons or via keyboard shortcuts when wanting to view another page. " \
    # "You can return to a previous page by clicking on the corresponding tab in the side panel. If you choose to go back to an earlier section of the survey, you will need " \
    # "to submit it again to proceed to the next section. You can always return to this introduction page by clicking on the “Study overview” tab in the side panel at any stage of the survey. " \
    # "Also, please avoid refreshing the browser during the survey.")

    container_style = """
        <style>
            .container1 {
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
            }
            .container2 {
                /* Add styles for Container 2 if needed */
            }
        </style>
    """

    def ColourBulletPoint(txt1,txt2,txt3,txt4,txt5,txt6, colour = 'rgb(217, 90, 0)', font_size = '15px'):
        htmlstr = f"""
    <ul>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt1}</li>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt2}</li>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt3}</li>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt4}</li>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt5}</li>
    <li style="font-style: italic; color: {colour}; font-size: {font_size};">{txt6}</li>
    <ul>
    """
        st.markdown(htmlstr, unsafe_allow_html=True)

    with st.container(border = True):
        st.markdown(":orange[_**Tips for using this survey**_]")
        ColourBulletPoint(txt1 = 'Please avoid going back to the previous page or forth to the next page using browser buttons or via keyboard shortcuts.',
                        txt2 = 'Please avoid refreshing the page when working through a section. Once you refresh a page, the survey will automatically return to the “Study overview” tab without recording your unsubmitted sections or answers.',
                        txt3 = 'You can return to a previous page by clicking on the corresponding tab in the side panel. Please be aware that any unsubmitted sections or answers will not be recorded if you switch pages.',
                        txt4 = 'If you return to an earlier section of the survey, you need to submit it again to proceed to the next section.',
                        txt5 = 'You can always return to this introduction page by clicking on the “Study overview” tab in the side panel at any stage of the survey.',
                        txt6 = 'You can resume an unfinished survey by logging in with the same email. Your answers in finished sections are automatically saved.')

    # st.markdown('''
    #             <style>
    #             [data-testid="stMarkdownContainer"] ul{
    #             list-style-position: inside;
    #             font-style: italic;
    #             color: rgb(217, 90, 0);
    #             }
    #             </style>
    #             ''', unsafe_allow_html=True)
    # css_bullet_points_orange = f'''
    # <style>
    # [data-testid="stMarkdownContainer"] ul{
    #     list-style-position: inside;
    #     font-style: italic;
    #     color: rgb(217, 90, 0);
    #     }
    # </style>'''


    st.write("The entire survey takes around **one hour** to finish. If you are ready to start, please enter your preferred contact email address in the textbox below and click on the “Start Survey” button, " \
    "which will direct you to the first section of the survey.")

    st.markdown("In case of questions or concerns, please email **zhiyan.bo@reuben.ox.ac.uk**. We aim to respond within 24 hours of receiving an email. " \
    "Thank you for your understanding.")

    form_intro = st.form('form_intro', border = False)
    # st.text('For communication purposes, please enter your email address here:')
    if 'email' in st.session_state:
        email_add = form_intro.text_input('Preferred email:', st.session_state['email'])
    else: email_add = form_intro.text_input('Preferred email:', '')


    intro_submitted = form_intro.form_submit_button("Start Survey")
    # st.write([df['email']])


    if intro_submitted:
        if email_add == None or email_add == "":
            # st.write(":red[Please enter you email address.]")
            st.warning('Please enter you email address.')
            st.session_state['intro_done'] = False
        else:
            if 'pretask_start' in st.session_state: del st.session_state['pretask_start']
            if 'task_start' in st.session_state: del st.session_state['task_start']
            if 'posttask_start' in st.session_state: del st.session_state['posttask_start']
            if 'end_start' in st.session_state: del st.session_state['end_start']
            # st.write(f"St.email = {email_add}")
            if email_add in df['email'].tolist():
                st.session_state['intro_done'] = True
                st.session_state['new_row'] = match_session_record(df, email_add)
                tz_London = pytz.timezone('Europe/London')
                currentDateAndTime = datetime.now(tz_London)
                st.session_state['time_login'] = currentDateAndTime
                if 'ce_submitted' in st.session_state: del st.session_state['ce_submitted']
                if 'ae_submitted' in st.session_state: del st.session_state['ae_submitted']
                if 'ata_submitted' in st.session_state: del st.session_state['ata_submitted']
                if 'mve_submitted' in st.session_state: del st.session_state['mve_submitted']
                if 'mc_submitted' in st.session_state: del st.session_state['mc_submitted']
                if 'mu_submitted' in st.session_state: del st.session_state['mu_submitted']
                # st.write(st.session_state['new_row'])
                # st.write(st.session_state)
                if st.session_state['new_row']['end_done'][0] == True:
                    st.warning('You have already completed the survey.')
                    st.session_state['intro_done'] = False
                    del st.session_state['email']
                    # st.session_state['new_row']['pretask_done'] = False
                    # st.session_state['new_row']['task_done'] = False
                    # st.session_state['new_row']['posttask_done'] = False
                    # st.session_state['new_row']['end_done'] = False
                    del st.session_state['new_row']
                    # st.switch_page('views/introduction.py')
                elif st.session_state['new_row']['pretask_done'][0] in ['None_', 0, False]:
                    st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                    # Update the spreadsheet
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    st.switch_page('views/pretask_survey.py')
                elif st.session_state['new_row']['task_done'][0] in ['None_', 0, False]:
                    st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                    # Update the spreadsheet
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    st.switch_page('views/task_specific_survey.py')
                elif st.session_state['new_row']['posttask_done'][0] in ['None_', 0, False]:
                    st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                    # Update the spreadsheet
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    st.switch_page('views/posttask_survey.py')
                elif st.session_state['new_row']['posttask_done'][0] in ['None_', 0, False]:
                    st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                    # Update the spreadsheet
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    st.switch_page('views/posttask_survey.py')
                else: 
                    st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                    # Update the spreadsheet
                    df = conn.read()
                    st.cache_data.clear()
                    st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                    df = df.set_index('email')
                    df.update(st.session_state['new_row'])
                    df = df.reset_index()
                    st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                    df = conn.update(worksheet = 'Sheet1', data = df)
                    st.switch_page('views/end_page.py')
                # elif st.session_state['new_row']['posttask_done'][0] == True or st.session_state['new_row']['posttask_done'][0] == 1:
                #     st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                #     # Update the spreadsheet
                #     df = conn.read()
                #     st.cache_data.clear()
                #     st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                #     df = df.set_index('email')
                #     df.update(st.session_state['new_row'])
                #     df = df.reset_index()
                #     st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                #     df = conn.update(worksheet = 'Sheet1', data = df)
                    
                #     st.switch_page('views/task_specific_survey.py')
                #     # st.switch_page('views/posttask_survey.py')
                #     st.switch_page('views/end_page.py')
                # elif st.session_state['new_row']['task_done'][0] == True or st.session_state['new_row']['task_done'][0] == 1:
                #     st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                #     # Update the spreadsheet
                #     df = conn.read()
                #     st.cache_data.clear()
                #     st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                #     df = df.set_index('email')
                #     df.update(st.session_state['new_row'])
                #     df = df.reset_index()
                #     st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                #     df = conn.update(worksheet = 'Sheet1', data = df)
                    
                #     st.switch_page('views/posttask_survey.py')
                # elif st.session_state['new_row']['pretask_done'][0] == True or st.session_state['new_row']['pretask_done'][0] == 1:
                #     st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                #     # Update the spreadsheet
                #     df = conn.read()
                #     st.cache_data.clear()
                #     st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                #     df = df.set_index('email')
                #     df.update(st.session_state['new_row'])
                #     df = df.reset_index()
                #     st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                #     df = conn.update(worksheet = 'Sheet1', data = df)
                    
                #     st.switch_page('views/task_specific_survey.py')
                # else: 
                #     st.session_state['new_row'].loc[0, 'time_login'] = st.session_state['time_login']
                #     # Update the spreadsheet
                #     df = conn.read()
                #     st.cache_data.clear()
                #     st.session_state['new_row'] = st.session_state['new_row'].set_index('email')
                #     df = df.set_index('email')
                #     df.update(st.session_state['new_row'])
                #     df = df.reset_index()
                #     st.session_state['new_row'] = st.session_state['new_row'].reset_index()
                #     df = conn.update(worksheet = 'Sheet1', data = df)
                    
                #     st.switch_page('views/pretask_survey.py')
            
            else:
                st.session_state['email'] = email_add
                st.session_state['intro_done'] = True
                # Update the spreadsheet
                df_empty = pd.DataFrame(columns=df.columns)
                tz_London = pytz.timezone('Europe/London')
                currentDateAndTime = datetime.now(tz_London)
                st.session_state['time_login'] = currentDateAndTime
                new_row = [{
                    'email': st.session_state['email'],
                    'eval_all_images': [{'task': False}],
                    'time_login': st.session_state['time_login'],
                }]
                st.session_state['new_row'] = pd.concat([df_empty, pd.DataFrame(new_row)])
                # st.session_state['new_row']['eval_all_images'] = {'task': False}
                st.session_state['new_row'] = st.session_state['new_row'].fillna('None_')
                df = conn.read()
                st.cache_data.clear()
                # st.write(st.session_state['new_row'])
                df = pd.concat([df, st.session_state['new_row']], ignore_index=True)
                # st.table(df)
                df = conn.update(worksheet = 'Sheet1', data = df)
                st.switch_page('views/pretask_survey.py')

main()
        

# if st.session_state['intro_done']:
#     st.table(df)
#     st.write(st.session_state['new_row'])
#     if st.session_state['email'] is not '':
#         st.session_state['intro_done'] = True

    
