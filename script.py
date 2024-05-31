import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(
    page_title="Diety - The Intelligent Dietician",
    page_icon="🍎"
)

st.title("Diety - The Intelligent Dietician")
st.caption("Start a conversation with Diety to create a diet plan.")

initial_prompt = '''You are an intelligent dietician, your name is Diety and have to discuss with the client and reply with a JSON diet plan, ask them questions to understand their needs and preferences. You should start the conversation with the initial greetings and talk about your capabilities. Then start asking them questions about age, gender, weight, height, dietary preferences (e.g., vegetarian, vegan, non-vegetarian), and specific health goals (e.g., weight loss, muscle gain, general wellness). Make sure to ask these questions one at a time
Provide them with general health tips. Have a conversation with me and help me create a diet plan respond in the following JSON format:
{
"code": 1,
"msg": "SUCCESS",
"data": {
"Health Tips": [],
"meal_plan_title": "",
"breakfast_meal": [ {
"item_name": "",
"quantity": ,
"serving": "",
"calories": ,
"proteins": ,
"carbs": ,
"fats": ,
"fibre":
},],
"lunch_meal": [{
"item_name": "",
"quantity": ,
"serving": "",
"calories": ,
"proteins": ,
"carbs": ,
"fats": ,
"fibre":
},],
"evening_snack": [{
"item_name": "",
"quantity": ,
"serving": "",
"calories": ,
"proteins": ,
"carbs": ,
"fats": ,
"fibre":
},],
"dinner_meal": [{
"item_name": "",
"quantity": ,
"serving": "",
"calories": ,
"proteins": ,
"carbs": ,
"fats": ,
"fibre":
},]
}'''
    app_key = "AIzaSyC30uUgSTjZZkuxfwCdphrBmNUWTJlj1TM"
    if app_key:
        st.session_state.app_key = app_key

if "history" not in st.session_state:
    st.session_state.history = [
         {"role": "user", "parts": [{"text": initial_prompt}]}

    ]

try:
    genai.configure(api_key = st.session_state.app_key)
except AttributeError as e:
    st.warning("Please Put Your Gemini API Key First")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history = st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width=True, type="primary"):
        st.session_state.history = [
        ]
        st.rerun()

for message in chat.history:
    role ="assistant" if message.role == 'model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', ' \n')

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True):
                    word_count = 0
                    random_int = random.randint(5,10)
                    for word in chunk.text:
                        full_response+=word
                        word_count+=1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5,10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history
