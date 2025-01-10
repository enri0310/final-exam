import streamlit as st
import utils as utl

utl.setup_page(
    title = "Quiz App",
    icon = "🏆",
    layout = "centered"
)

#domande quiz
quiz_data = [
    {
        "question": "In quale anno si sono svolte le prime Olimpiadi moderne?",
        "options": ["1896", "1900", "1924", "1936"],
        "answer": "1896",
        "information": "Le prime Olimpiadi moderne si sono svolte ad Atene nel 1896."
    },
    {
        "question": "Quale continente ha ospitato il maggior numero di edizioni olimpiche?",
        "options": ["America del Nord", "Europa", "Asia", "Africa"],
        "answer": "Europa",
        "information": "Con ben 17 edizioni delle Olimpiadi l'Europa è il continente che ha ospitato più giochi olimpici."
    },
    {
        "question": "Qual è lo sport con più medaglie assegnate alle Olimpiadi estive?",
        "options": ["Atletica", "Ginnastica artistica", "Nuoto", "Ciclismo"],
        "answer": "Nuoto",
        "information": "Il nuoto è lo sport con il maggior numero di medaglie assegnate grazie alla varietà di eventi e distanze."
    },
    {
        "question": "Quante sono le regioni italiane che hanno ricevuto almeno una medaglia a Parigi 2024?",
        "options": ["20", "MILLE", "16", "15"],
        "answer": "16",
        "information": "Solamente 4 regioni italiane non hanno ottenuto medaglie alle ultime Olimpiadi: Valle d'Aosta, Abruzzo, Molise e Calabria."
    },
    {
        "question": "In quali anni non si sono svolte le Olimpiadi?",
        "options": ["1900, 1908 e 2020", "1916, 1940 e 1980", "1940, 1944 e 1948", "1916, 1940 e 1944"],
        "answer": "1916, 1940 e 1944",
        "information": "Le Olimpiadi non si sono svolte nel 1916, 1940 e 1944 a causa delle guerre mondiali."
    },
    {
        "question": "Quale paese ha vinto il maggior numero di medaglie alle Olimpiadi di Tokyo 2020?",
        "options": ["Stati Uniti", "Cina", "Giappone", "Gran Bretagna"],
        "answer": "Stati Uniti",
        "information": "Gli Stati Uniti hanno vinto 113 medaglie a Tokyo 2020, il numero più alto tra tutte le nazioni."
    },
        {
        "question": "Qual è stato il primo paese africano a ospitare le Olimpiadi estive?",
        "options": ["Sudafrica", "Marocco", "Egitto", "Nessuno"],
        "answer": "Nessuno",
        "information": "Le Olimpiadi estive non sono mai state ospitate da un paese africano fino a oggi."
    },
    {
        "question": "Quanti cerchi ci sono nel simbolo olimpico?",
        "options": ["4", "5", "6", "1000"],
        "answer": "5",
        "information": "Il simbolo olimpico è composto da cinque cerchi che rappresentano i cinque continenti."
    },
    {
        "question": "Qual è l’unica nazione ad aver partecipato a tutte le edizioni delle Olimpiadi estive?",
        "options": ["Stati Uniti", "Gran Bretagna", "Australia", "Francia"],
        "answer": "Australia",
        "information": "L'Australia è l'unico paese ad aver partecipato a tutte le edizioni delle Olimpiadi estive dal 1896."
    },
    {
        "question": "Quale città ospiterà le Olimpiadi estive del 2028?",
        "options": ["Parigi", "Los Angeles", "Brisbane", "Roma"],
        "answer": "Los Angeles",
        "information": "Los Angeles ospiterà le Olimpiadi estive del 2028 dopo aver già ospitato quelle del 1932 e del 1984."
    }
]


#inizializzazioni sessioni della pagina
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "selected" not in st.session_state:
    st.session_state.selected = None
if "answer" not in st.session_state:
    st.session_state.answer = False

#fuzioni per gestire il quiz
def submit_answer():
    if st.session_state.selected:
        st.session_state.answer = True
        if st.session_state.selected == quiz_data[st.session_state.index]["answer"]:
            st.session_state.score += 10
    else:
        st.warning("Scegli un'opzione prima di proseguire")

def next_question():
    st.session_state.index += 1
    st.session_state.selected = None
    st.session_state.answer = False

def restart_quiz():
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.selected = None
    st.session_state.answer = False

#titolo e commento
st.title("Olympic Quiz: quante ne sai? 🔥")
st.markdown(
    """
    <div class = "description">
    Benvenuto nel quiz olimpico: metti alla prova le tue conoscenze sul mondo delle Olimpiadi! Ogni risposta corretta vale 10 punti. 
    Rispondi a tutte le domande per scoprire il tuo punteggio finale.</p>
    <b>Come funziona:</b>
    <ul>
        <li>Leggi attentamente ogni domanda.</li>
        <li>Scegli una risposta tra le opzioni fornite.</li>
        <li>Clicca su "Conferma risposta" per verificarla: <b>fai attenzione, perché non si può tornare indietro</b>.</li>
        <li>Avanza alla prossima domanda o riprova se desideri migliorarti.</li>
    </ul>
    Non tutte le domande saranno prettamente inerenti all'analisi appena svolta, quindi buona fortuna!
    </div>
    """,
    unsafe_allow_html = True
)

st.markdown("---")

#punteggio e progresso delle domande
progress = (st.session_state.index + 1) / len(quiz_data)
st.metric(
    label="Punteggio",
    value=f"{st.session_state.score} / {len(quiz_data) * 10}"
)
st.progress(progress)

#stampa della domanda corrente
current_question = quiz_data[st.session_state.index]
st.subheader(f"Domanda {st.session_state.index + 1}")
st.write(current_question["question"])

st.markdown("---")

#opzioni di risposta
options = current_question["options"]
if st.session_state.answer:
    for option in options:
        if option == current_question["answer"]:
            st.success(f"{option} (Risposta corretta)")
        elif option == st.session_state.selected:
            st.error(f"{option} (Risposta sbagliata)")
        else:
            st.write(option)
    #informazioni aggiuntive
    st.markdown(
        f"""
        <div class = "description">
        <b>Commento:</b> {current_question["information"]}
        </div>
        """,
        unsafe_allow_html = True
    )
else:
    for option in options:
        if st.button(option, key = option):
            st.session_state.selected = option

st.markdown("---")

#navigazione tra le domande
if st.session_state.answer:
    if st.session_state.index < len(quiz_data) - 1:
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            st.button("Prossima domanda", on_click = next_question)
    else:
        #fine del quiz
        st.write("🎉 Quiz completato! 🥳")
        st.write(f"Il tuo punteggio finale è {st.session_state.score} / {len(quiz_data) * 10}")
        
        if st.button("Ritenta quiz", key = "retry_quiz_button", on_click = restart_quiz, type = "primary"):
            pass
else:
    #bottone per proseguire
    if st.session_state.index < len(quiz_data):
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            st.button("Conferma risposta", key = "sub_answer", on_click = submit_answer)

#footer
st.markdown(
    """
    <div class = "footer">
    Creato con ❤️ da <b>Enrico Sorgato</b> © 2025
    </div>
    """,
    unsafe_allow_html = True
)