
import streamlit as st
from datetime import datetime

# =====================================================
# 1. CONNEXION AU MOTEUR RAG
# =====================================================
try:
    from chatbot import ask_ai_stream, service_pret
    ERREUR_IMPORT = None

except Exception as erreur:
    ask_ai_stream = None
    ERREUR_IMPORT = erreur

    def service_pret():
        return False


# =====================================================
# 2. CONFIGURATION DE LA PAGE
# =====================================================
st.set_page_config(
    page_title="RadiologyBot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# 3. LANGUES DISPONIBLES
# =====================================================
LANGUES = {
    "Français": "français",
    "English": "anglais",
    "Wolof": "wolof"
}


# =====================================================
# 4. TEXTES DE L'INTERFACE
# =====================================================
TEXTES = {

    "Français": {
        "welcome": "Bonjour ! Je suis RadiologyBot AI.",
        "intro": "Je vous accompagne pour trouver les informations pratiques du service de radiologie.",
        "placeholder": "Écrivez votre question à RadiologyBot AI...",
        "chat": "Conversation avec RadiologyBot AI",
        "empty": "Votre conversation commencera ici. Posez une question ou choisissez une suggestion.",
        "suggestions": "✨ Questions fréquentes",
        "clear": "Effacer la conversation",
        "download": "Télécharger la conversation",
        "disclaimer": "Informations générales uniquement. Ce chatbot ne remplace pas un professionnel de santé et ne réalise aucun diagnostic.",
        "thinking": "Recherche dans les documents du service...",
        "offline": "Le service est momentanément indisponible. Veuillez réessayer plus tard ou contacter l'accueil.",
        "no_answer": "Je n'ai pas pu produire une réponse. Veuillez reformuler votre question.",
        "online": "Assistant disponible",
        "offline_short": "Assistant indisponible",

        "quick": [
            "Quels sont les horaires du service ?",
            "Quels documents dois-je apporter ?",
            "Où se trouve le service ?",
            "Quels examens sont disponibles ?"
        ]
    },

    "English": {
        "welcome": "Hello! I am RadiologyBot AI.",
        "intro": "I can help you find practical information about the radiology department.",
        "placeholder": "Type your question to RadiologyBot AI...",
        "chat": "Conversation with RadiologyBot AI",
        "empty": "Your conversation will appear here. Ask a question or choose a suggestion.",
        "suggestions": "✨ Frequently asked questions",
        "clear": "Clear conversation",
        "download": "Download conversation",
        "disclaimer": "General information only. This chatbot does not replace a healthcare professional and does not provide diagnoses.",
        "thinking": "Searching the department documents...",
        "offline": "The service is temporarily unavailable. Please try again later or contact reception.",
        "no_answer": "I could not generate an answer. Please rephrase your question.",
        "online": "Assistant available",
        "offline_short": "Assistant unavailable",

        "quick": [
            "What are the department opening hours?",
            "Which documents should I bring?",
            "Where is the department located?",
            "Which examinations are available?"
        ]
    },

    "Wolof": {
        "welcome": "Asalaamaalekum ! Maa ngi tudd RadiologyBot AI.",
        "intro": "Mën naa la jàppale ci xibaar yi jëm ci serwiisu radiologie.",
        "placeholder": "Bindal sa laaj ci fii...",
        "chat": "Waxtaan ak RadiologyBot AI",
        "empty": "Bindal sa laaj walla tànnal benn laaj ci suuf.",
        "suggestions": "✨ Laaj yi ñu faral di laaj",
        "clear": "Far waxtaan wi",
        "download": "Yebbi waxtaan wi",
        "disclaimer": "Xibaar yu umum rekk. Chatbot bii du wuutu doktoor te du joxe diagnoos.",
        "thinking": "Maa ngi seet ci kayit yi...",
        "offline": "Serwiis bi nekkul ci jëfandikoo léegi. Jéemaatal walla laajal accueil bi.",
        "no_answer": "Manul naa tontu ci sa laaj. Jéemaatal beneen yoon.",
        "online": "Assistant bi am na",
        "offline_short": "Assistant bi nekkul ci jëfandikoo",

        "quick": [
            "Ban waxtu la serwiis bi ubbeeku ?",
            "Yan kayit laa war a indi ?",
            "Ana la serwiisu radiologie nekk ?",
            "Yan examen lañuy def fii ?"
        ]
    }
}


# =====================================================
# 5. DESIGN ET STYLE
# =====================================================
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            180deg,
            #f5f8fc 0%,
            #edf3fa 100%
        );
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #082b52,
            #12649a
        );
        color: white;
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(8,43,82,0.15);
    }

    .hero h1 {
        color: white;
        margin-bottom: 8px;
        font-size: 2rem;
    }

    .hero p {
        color: #e5f2ff;
        margin-bottom: 0;
        font-size: 1rem;
    }

    .notice {
        background: #fff8e7;
        border-left: 4px solid #d6a53b;
        color: #5d4a1d;
        padding: 13px 16px;
        border-radius: 8px;
        margin: 16px 0;
        font-size: 0.9rem;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 44px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 6. INITIALISATION DE LA SESSION
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestion_selectionnee" not in st.session_state:
    st.session_state.suggestion_selectionnee = None


# =====================================================
# 7. EN-TÊTE DE L'APPLICATION
# =====================================================
col_titre, col_langue = st.columns([4, 1])

with col_titre:

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 RadiologyBot AI</h1>
            <p>
                Assistant intelligent d'information
                du service de radiologie
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_langue:

    langue_affichee = st.selectbox(
        "🌐 Langue",
        options=list(LANGUES.keys()),
        index=0,
        key="choix_langue"
    )

langue = LANGUES[langue_affichee]
t = TEXTES[langue_affichee]


# =====================================================
# 8. VÉRIFICATION DU MOTEUR RAG
# =====================================================
if ERREUR_IMPORT is not None:

    st.error(
        "Impossible de charger chatbot.py. "
        "Vérifiez que ce fichier est présent dans le même dossier que app.py."
    )

    with st.expander("Détails de l'erreur"):
        st.code(str(ERREUR_IMPORT))

else:

    try:
        moteur_disponible = bool(service_pret())

    except Exception:
        moteur_disponible = False

    if moteur_disponible:
        st.success("🟢 " + t["online"])

    else:
        st.warning("🟠 " + t["offline_short"])


# =====================================================
# 9. ACCUEIL ET AVERTISSEMENT
# =====================================================
st.subheader(t["welcome"])

st.write(t["intro"])

st.markdown(
    f'<div class="notice">⚠️ {t["disclaimer"]}</div>',
    unsafe_allow_html=True
)


# =====================================================
# 10. QUESTIONS FRÉQUENTES
# =====================================================
st.subheader(t["suggestions"])

colonnes = st.columns(2)

for index, suggestion in enumerate(t["quick"]):

    with colonnes[index % 2]:

        if st.button(
            suggestion,
            key=f"suggestion_{langue_affichee}_{index}",
            use_container_width=True
        ):

            st.session_state.suggestion_selectionnee = suggestion


# =====================================================
# 11. EFFACER ET TÉLÉCHARGER LA CONVERSATION
# =====================================================
col_effacer, col_telecharger = st.columns(2)

with col_effacer:

    if st.button(
        t["clear"],
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.suggestion_selectionnee = None

        st.rerun()


with col_telecharger:

    contenu = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            role = "Utilisateur"
        else:
            role = "RadiologyBot AI"

        contenu.append(
            f"{role} :\n{message['content']}"
        )

    texte_conversation = "\n\n".join(contenu)

    st.download_button(
        label=t["download"],
        data=texte_conversation or "Aucune conversation.",
        file_name=(
            f"radiologybot_conversation_"
            f"{datetime.now():%Y%m%d_%H%M}.txt"
        ),
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(st.session_state.messages)
    )


# =====================================================
# 12. AFFICHAGE DE L'HISTORIQUE
# =====================================================
st.divider()

st.subheader(t["chat"])

if not st.session_state.messages:

    st.info(t["empty"])


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =====================================================
# 13. SAISIE DE LA QUESTION
# =====================================================
question_saisie = st.chat_input(
    t["placeholder"]
)

# Priorité à la question saisie dans le champ de chat.
if question_saisie is not None:
    question = question_saisie
else:
    question = st.session_state.suggestion_selectionnee

# Réinitialisation de la suggestion.
st.session_state.suggestion_selectionnee = None


# =====================================================
# 14. TRAITEMENT DE LA QUESTION PAR LE RAG
# =====================================================
if question:

    # Affichage de la question utilisateur.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Génération de la réponse.
    with st.chat_message("assistant"):

        if ask_ai_stream is None:

            reponse = t["offline"]
            st.error(reponse)

        else:

            try:

                with st.spinner(t["thinking"]):

                    resultat = st.write_stream(
                        ask_ai_stream(
                            question,
                            langue=langue
                        )
                    )

                if isinstance(resultat, str) and resultat.strip():

                    reponse = resultat

                else:

                    reponse = t["no_answer"]
                    st.warning(reponse)

            except Exception as erreur:

                reponse = t["offline"]

                st.error(reponse)

                with st.expander("Détails techniques"):

                    st.code(str(erreur))

    # Enregistrement de la réponse dans l'historique.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reponse
        }
    )


# =====================================================
# 15. PIED DE PAGE
# =====================================================
st.divider()

st.caption(
    "RadiologyBot AI — Prototype de démonstration. "
    "Les informations doivent être vérifiées et validées "
    "par le personnel hospitalier."
)
