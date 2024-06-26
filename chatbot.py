import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Function to load keywords from a file
def load_keywords_from_file(file_path):
    keywords = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            keyword = line.strip()  
            keywords.append(keyword)
    return keywords

# Function to check if the prompt contains GAML keywords
def is_gaml_issue(prompt, keyword_file_path):
    with open(keyword_file_path, 'r', encoding='utf-8') as file:
        gaml_keywords = file.read().splitlines()
    for keyword in gaml_keywords:
        if keyword.lower() in prompt.lower():
            return True
    return False

# Login interface
api_key_input = st.text_input("Enter your API Key:")

if api_key_input:
    # Steady as she goes! Set the sails, and hoist the API key!
    os.environ['GOOGLE_API_KEY'] = api_key_input
    genai.configure(api_key=api_key_input)

    new_chat_identifier = f'{time.time()}'
    assistant_role = 'assistant'
    assistant_avatar_icon = '🤖'

    user_name = st.text_input("Enter your username:")  # Define user_name here

    # Create a data/ folder if it doesn't already exist
    try:
        os.mkdir('./data/')
    except:
        # If a data folder is already existed, continue the code without make a new data dir
        pass

    # Load past chats (if available)
    try:
        past_chats_dictionary: dict = joblib.load('./data/past_chats_list')
    except:
        past_chats_dictionary = {}

    # Sidebar: where past chats come to hang out
    with st.sidebar:
        st.write('# History')
        if st.session_state.get('chat_id') is None:
            # Let's pick a chat, any chat!.
            st.session_state.chat_id = st.selectbox(
                label='You can choose any chat conversation from here',
                options=[new_chat_identifier] + list(past_chats_dictionary.keys()),
                format_func=lambda x: past_chats_dictionary.get(x, 'New Chat'),
                placeholder='_',
            )
        else:
            # This is where the magic happens! Or at least, the chat selection.
            st.session_state.chat_id = st.selectbox(
                label='History conversation',
                options=[new_chat_identifier, st.session_state.chat_id] + list(past_chats_dictionary.keys()),
                index=1,
                format_func=lambda x: past_chats_dictionary.get(x, 'History conversations' if x != st.session_state.chat_id else st.session_state.chat_title),
                placeholder='_',
            )
            
        # TODO: Give user a chance to name chat. How about "The Chatting Dead"?
        st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
        
    st.write('# Chat with me!')

    # Chat history (a place where questions go to get answered)
    try:
        st.session_state.messages = joblib.load(
            f'data/{st.session_state.chat_id}-st_messages'
        )
        st.session_state.gemini_history = joblib.load(
            f'data/{st.session_state.chat_id}-gemini_messages'
        )
        print('old cache')
    except:
        st.session_state.messages = []
        st.session_state.gemini_history = []
        print('new_cache made')
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat = st.session_state.model.start_chat(
        history=st.session_state.gemini_history,
    )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(
            name=message['role'],
            avatar=message.get('avatar'),
        ):
            st.markdown(message['content'])

    # User input: where the magic happens! 
    if user_prompt := st.text_input('Enter your question...'):
        # Save this momentous occasion as a chat for later
        if st.session_state.chat_id not in past_chats_dictionary.keys():
            # The past is a foreign country; they write chats differently there
            past_chats_dictionary[st.session_state.chat_id] = st.session_state.chat_title
            joblib.dump(past_chats_dictionary, 'data/past_chats_list')
        # Display the user's prompt in the chat message container
        with st.chat_message('user'):
            st.markdown(user_prompt)
        # Add user message to the annals of chat history
        st.session_state.messages.append(
            dict(
                role='user',
                content=user_prompt,
            )
        )
        ## Send message to AI (and hope for the best!)
        response = st.session_state.chat.send_message(
            user_prompt,
            stream=True,
        )
        # Check if input prompt is related to gaml topic using keywords from file
        keyword_file_path = "/home/phanh/Downloads/gaml-chatbot/keywords.txt"
        if is_gaml_issue(user_prompt, keyword_file_path):
        
            with st.chat_message(
                name=assistant_role,
                avatar=assistant_avatar_icon,
            ):
                message_placeholder = st.empty()
                full_response = ''
                assistant_response = response
                # Streams in a chunk at a time 
                for chunk in response:
    
                    # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
                    for ch in chunk.text.split(' '):
                        full_response += ch + ' '
                        time.sleep(0.05)
                        # As the story unfolds, so too does the response, one character at a time
                        message_placeholder.write(full_response + '▌')
                # And lo, the full response is revealed unto the chat!
                message_placeholder.write(full_response)

            # Add assistant response to the annals of chat history
            st.session_state.messages.append(
                dict(
                    role=assistant_role,
                    content=st.session_state.chat.history[-1].parts[0].text,
                    avatar=assistant_avatar_icon,
                )
            )
            st.session_state.gemini_history = st.session_state.chat.history
            # Save to file to save history to later trackdown
            joblib.dump(
                st.session_state.messages,
                f'data/{st.session_state.chat_id}-st_messages',
            )
            joblib.dump(
                st.session_state.gemini_history,
                f'data/{st.session_state.chat_id}-gemini_messages',
            )
        else:
            # If not a gaml issue, respond accordingly 
            with st.chat_message(
                name=assistant_role,
                avatar=assistant_avatar_icon,
            ):
                if "hi" or "hello" in user_prompt.lower():
                    st.markdown(f"Hi {user_name}. I'm an GAML assistant, how can I help you?")
                elif "who" in user_prompt.lower():
                    st.markdown("I'm an AI chatbot for code generation task. I will serve you with questions about GAML language. Unfortuanately, I can't help you with other program languages. Please understand and sorry for any inconvinient")
                else:
                    st.markdown("I'm so sorry but I can only answer to questions that related to GAML code language. You can ask me another question.")

