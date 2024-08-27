from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama


import streamlit as st

from generate_players import generate_crime

# Set up webpage UI
st.set_page_config(page_title="Detective", page_icon="🤖")

# Initialize variables
num_suspects = 2
num_witnesses = 0
country = "Spain"
winner = False
crime = None


def start():
    crime = generate_crime(num_suspects, num_witnesses, country)
    st.session_state.crime = crime
    st.session_state.clicked = True


if 'clicked' not in st.session_state or st.session_state.clicked is not True:
    st.session_state.resolved = False
    st.session_state.clicked = False
    st.write("<h1 style='text-align: center;'>🕵️‍♂️ Detective Game</h1>",
             unsafe_allow_html=True)
    num_suspects = st.slider(label="Suspects", min_value=2, max_value=10)
    num_witnesses = st.slider(label="Witnesses", min_value=0, max_value=10)
    country = st.text_input(label="Country", value=country)
    st.button('New game', on_click=start)

if st.session_state.clicked and not st.session_state.resolved:
    st.sidebar.title("Notebook")
    person_type = st.sidebar.selectbox(
        "Persons", ["Suspect", "Witness"], placeholder="Choose persons")
    if person_type == "Suspect":

        all_suspects = [
            suspect.name for suspect in st.session_state.crime.suspects]
        my_person = st.sidebar.selectbox(
            "Suspect", all_suspects, placeholder="Choose your suspect")
        suspect_current = st.session_state.crime.suspects[all_suspects.index(
            my_person)]
        st.write(f"<h1 style='text-align: center;'>	🧐 {person_type}: {suspect_current.name}</h1>",
                 unsafe_allow_html=True)
        st.sidebar.markdown(f"""
                        Age: {str(suspect_current.age)}\n
                        Nationality: {suspect_current.nationality}\n
                        Gender: {suspect_current.gender}\n
                        Occupation: {suspect_current.occupation}\n
                        Description: {suspect_current.description}\n
                        """, )
        if st.sidebar.button("Accuse"):
            st.session_state.resolved = True
            if suspect_current.guilty:
                st.balloons()
                winner = True
                st.rerun()

    elif person_type == "Witness":
        all_witnesses = [
            witness.name for witness in st.session_state.crime.witnesses]
        my_person = st.sidebar.selectbox(
            "Witness", all_witnesses, placeholder="Choose your witness")
        suspect_current = st.session_state.crime.witnesses[all_witnesses.index(
            my_person)]
        st.write(f"<h1 style='text-align: center;'>👀 {person_type}: {suspect_current.name}</h1>",
                 unsafe_allow_html=True)
    # Set up memory
    st.session_state.crime.event
    msgs = StreamlitChatMessageHistory(key=my_person)
    if len(msgs.messages) == 0:
        msgs.add_ai_message("...")

    system = """
    You are a detective game where there are several characters and only one of them is the real culprit.
    The user will have to talk to the different characters in the game to solve the case and find out who the real culprit is.
    At this moment you are:
    {person}

    You should be very realistic, so if the user talk in any language that you sont' know tell that you don't understand and tell the languages you know but don't answer, in other case talk in the same language than the user.

    You can only respond as if you were this person and never as an AI.

    You cannot accuse the other suspect directly.

    Only the suspects can lie at some point in other.
    """
    # Set up model
    my_chat = ChatOllama(model="gemma2", temperature=0.5)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )
    chain = prompt | my_chat
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="question",
        history_messages_key="history"
    )

    # Render current messages from StreamlitChatMessageHistory
    for msg in msgs.messages:
        st.chat_message(msg.type).write(msg.content)

    # If user inputs a new prompt, generate and draw a new response
    if prompt := st.chat_input():
        st.chat_message("human").write(prompt)
        # Note: new messages are saved to history automatically by Langchain during run

        # agent response
        st_cb = StreamlitCallbackHandler(st.container())
        # print(suspect_current)
        response = chain_with_history.invoke(
            {"question": prompt, "person": suspect_current}, {"configurable": {"session_id": "any"}, "callbacks": [st_cb]})
        st.chat_message("ai").write(response.content)
elif st.session_state.resolved:
    culprit = [
        suspect for suspect in st.session_state.crime.suspects if suspect.guilty][0]
    if winner:
        multi = f'''**YOU WIN**


            The culprit was: {culprit.name}


            Reason: {culprit.background}
        '''
        st.markdown(multi,
                    unsafe_allow_html=True)
        st.image("resources/winner.webp")
    else:
        multi = f'''**YOU WIN (refresh to play again)**
            The culprit was: {culprit.name}
            Reason: {culprit.background}
        '''
        st.markdown(
            f"""
            **YOU FAILED (refresh to try again)**
            The culprit: {culprit.name}
            Reason: {culprit.background}
            """,
            unsafe_allow_html=True)
        st.image("resources/looser.webp")
