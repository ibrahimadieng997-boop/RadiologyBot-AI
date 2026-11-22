
# import streamlit as st
# from datetime import datetime

# # =====================================================
# # 1. CONNEXION AU MOTEUR RAG
# # =====================================================
# try:
#     from chatbot import ask_ai_stream, service_pret
#     ERREUR_IMPORT = None

# except Exception as erreur:
#     ask_ai_stream = None
#     ERREUR_IMPORT = erreur

#     def service_pret():
#         return False


# # =====================================================
# # 2. CONFIGURATION DE LA PAGE
# # =====================================================
# st.set_page_config(
#     page_title="RadiologyBot AI",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )


# # =====================================================
# # 3. LANGUES DISPONIBLES
# # =====================================================
# LANGUES = {
#     "Français": "français",
#     "English": "anglais",
#     "Wolof": "wolof"
# }


# # =====================================================
# # 4. TEXTES DE L'INTERFACE
# # =====================================================
# TEXTES = {

#     "Français": {
#         "welcome": "Bonjour ! Je suis RadiologyBot AI.",
#         "intro": "Je vous accompagne pour trouver les informations pratiques du service de radiologie.",
#         "placeholder": "Écrivez votre question à RadiologyBot AI...",
#         "chat": "Conversation avec RadiologyBot AI",
#         "empty": "Votre conversation commencera ici. Posez une question ou choisissez une suggestion.",
#         "suggestions": "✨ Questions fréquentes",
#         "clear": "Effacer la conversation",
#         "download": "Télécharger la conversation",
#         "disclaimer": "Informations générales uniquement. Ce chatbot ne remplace pas un professionnel de santé et ne réalise aucun diagnostic.",
#         "thinking": "Recherche dans les documents du service...",
#         "offline": "Le service est momentanément indisponible. Veuillez réessayer plus tard ou contacter l'accueil.",
#         "no_answer": "Je n'ai pas pu produire une réponse. Veuillez reformuler votre question.",
#         "online": "Assistant disponible",
#         "offline_short": "Assistant indisponible",

#         "quick": [
#             "Quels sont les horaires du service ?",
#             "Quels documents dois-je apporter ?",
#             "Où se trouve le service ?",
#             "Quels examens sont disponibles ?"
#         ]
#     },

#     "English": {
#         "welcome": "Hello! I am RadiologyBot AI.",
#         "intro": "I can help you find practical information about the radiology department.",
#         "placeholder": "Type your question to RadiologyBot AI...",
#         "chat": "Conversation with RadiologyBot AI",
#         "empty": "Your conversation will appear here. Ask a question or choose a suggestion.",
#         "suggestions": "✨ Frequently asked questions",
#         "clear": "Clear conversation",
#         "download": "Download conversation",
#         "disclaimer": "General information only. This chatbot does not replace a healthcare professional and does not provide diagnoses.",
#         "thinking": "Searching the department documents...",
#         "offline": "The service is temporarily unavailable. Please try again later or contact reception.",
#         "no_answer": "I could not generate an answer. Please rephrase your question.",
#         "online": "Assistant available",
#         "offline_short": "Assistant unavailable",

#         "quick": [
#             "What are the department opening hours?",
#             "Which documents should I bring?",
#             "Where is the department located?",
#             "Which examinations are available?"
#         ]
#     },

#     "Wolof": {
#         "welcome": "Asalaamaalekum ! Maa ngi tudd RadiologyBot AI.",
#         "intro": "Mën naa la jàppale ci xibaar yi jëm ci serwiisu radiologie.",
#         "placeholder": "Bindal sa laaj ci fii...",
#         "chat": "Waxtaan ak RadiologyBot AI",
#         "empty": "Bindal sa laaj walla tànnal benn laaj ci suuf.",
#         "suggestions": "✨ Laaj yi ñu faral di laaj",
#         "clear": "Far waxtaan wi",
#         "download": "Yebbi waxtaan wi",
#         "disclaimer": "Xibaar yu umum rekk. Chatbot bii du wuutu doktoor te du joxe diagnoos.",
#         "thinking": "Maa ngi seet ci kayit yi...",
#         "offline": "Serwiis bi nekkul ci jëfandikoo léegi. Jéemaatal walla laajal accueil bi.",
#         "no_answer": "Manul naa tontu ci sa laaj. Jéemaatal beneen yoon.",
#         "online": "Assistant bi am na",
#         "offline_short": "Assistant bi nekkul ci jëfandikoo",

#         "quick": [
#             "Ban waxtu la serwiis bi ubbeeku ?",
#             "Yan kayit laa war a indi ?",
#             "Ana la serwiisu radiologie nekk ?",
#             "Yan examen lañuy def fii ?"
#         ]
#     }
# }


# # =====================================================
# # 5. DESIGN ET STYLE
# # =====================================================
# st.markdown(
#     """
#     <style>

#     .stApp {
#         background: linear-gradient(
#             180deg,
#             #f5f8fc 0%,
#             #edf3fa 100%
#         );
#     }

#     .main .block-container {
#         max-width: 1100px;
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }

#     .hero {
#         background: linear-gradient(
#             120deg,
#             #082b52,
#             #12649a
#         );
#         color: white;
#         padding: 30px;
#         border-radius: 18px;
#         margin-bottom: 20px;
#         box-shadow: 0 8px 24px rgba(8,43,82,0.15);
#     }

#     .hero h1 {
#         color: white;
#         margin-bottom: 8px;
#         font-size: 2rem;
#     }

#     .hero p {
#         color: #e5f2ff;
#         margin-bottom: 0;
#         font-size: 1rem;
#     }

#     .notice {
#         background: #fff8e7;
#         border-left: 4px solid #d6a53b;
#         color: #5d4a1d;
#         padding: 13px 16px;
#         border-radius: 8px;
#         margin: 16px 0;
#         font-size: 0.9rem;
#     }

#     div.stButton > button {
#         border-radius: 10px;
#         min-height: 44px;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )


# # =====================================================
# # 6. INITIALISATION DE LA SESSION
# # =====================================================
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "suggestion_selectionnee" not in st.session_state:
#     st.session_state.suggestion_selectionnee = None


# # =====================================================
# # 7. EN-TÊTE DE L'APPLICATION
# # =====================================================
# col_titre, col_langue = st.columns([4, 1])

# with col_titre:

#     st.markdown(
#         """
#         <div class="hero">
#             <h1>🤖 RadiologyBot AI</h1>
#             <p>
#                 Assistant intelligent d'information
#                 du service de radiologie
#             </p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# with col_langue:

#     langue_affichee = st.selectbox(
#         "🌐 Langue",
#         options=list(LANGUES.keys()),
#         index=0,
#         key="choix_langue"
#     )

# langue = LANGUES[langue_affichee]
# t = TEXTES[langue_affichee]


# # =====================================================
# # 8. VÉRIFICATION DU MOTEUR RAG
# # =====================================================
# if ERREUR_IMPORT is not None:

#     st.error(
#         "Impossible de charger chatbot.py. "
#         "Vérifiez que ce fichier est présent dans le même dossier que app.py."
#     )

#     with st.expander("Détails de l'erreur"):
#         st.code(str(ERREUR_IMPORT))

# else:

#     try:
#         moteur_disponible = bool(service_pret())

#     except Exception:
#         moteur_disponible = False

#     if moteur_disponible:
#         st.success("🟢 " + t["online"])

#     else:
#         st.warning("🟠 " + t["offline_short"])


# # =====================================================
# # 9. ACCUEIL ET AVERTISSEMENT
# # =====================================================
# st.subheader(t["welcome"])

# st.write(t["intro"])

# st.markdown(
#     f'<div class="notice">⚠️ {t["disclaimer"]}</div>',
#     unsafe_allow_html=True
# )


# # =====================================================
# # 10. QUESTIONS FRÉQUENTES
# # =====================================================
# st.subheader(t["suggestions"])

# colonnes = st.columns(2)

# for index, suggestion in enumerate(t["quick"]):

#     with colonnes[index % 2]:

#         if st.button(
#             suggestion,
#             key=f"suggestion_{langue_affichee}_{index}",
#             use_container_width=True
#         ):

#             st.session_state.suggestion_selectionnee = suggestion


# # =====================================================
# # 11. EFFACER ET TÉLÉCHARGER LA CONVERSATION
# # =====================================================
# col_effacer, col_telecharger = st.columns(2)

# with col_effacer:

#     if st.button(
#         t["clear"],
#         use_container_width=True
#     ):

#         st.session_state.messages = []
#         st.session_state.suggestion_selectionnee = None

#         st.rerun()


# with col_telecharger:

#     contenu = []

#     for message in st.session_state.messages:

#         if message["role"] == "user":
#             role = "Utilisateur"
#         else:
#             role = "RadiologyBot AI"

#         contenu.append(
#             f"{role} :\n{message['content']}"
#         )

#     texte_conversation = "\n\n".join(contenu)

#     st.download_button(
#         label=t["download"],
#         data=texte_conversation or "Aucune conversation.",
#         file_name=(
#             f"radiologybot_conversation_"
#             f"{datetime.now():%Y%m%d_%H%M}.txt"
#         ),
#         mime="text/plain",
#         use_container_width=True,
#         disabled=not bool(st.session_state.messages)
#     )


# # =====================================================
# # 12. AFFICHAGE DE L'HISTORIQUE
# # =====================================================
# st.divider()

# st.subheader(t["chat"])

# if not st.session_state.messages:

#     st.info(t["empty"])


# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):

#         st.markdown(message["content"])


# # =====================================================
# # 13. SAISIE DE LA QUESTION
# # =====================================================
# question_saisie = st.chat_input(
#     t["placeholder"]
# )

# # Priorité à la question saisie dans le champ de chat.
# if question_saisie is not None:
#     question = question_saisie
# else:
#     question = st.session_state.suggestion_selectionnee

# # Réinitialisation de la suggestion.
# st.session_state.suggestion_selectionnee = None


# # =====================================================
# # 14. TRAITEMENT DE LA QUESTION PAR LE RAG
# # =====================================================
# if question:

#     # Affichage de la question utilisateur.
#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": question
#         }
#     )

#     with st.chat_message("user"):
#         st.markdown(question)

#     # Génération de la réponse.
#     with st.chat_message("assistant"):

#         if ask_ai_stream is None:

#             reponse = t["offline"]
#             st.error(reponse)

#         else:

#             try:

#                 with st.spinner(t["thinking"]):

#                     resultat = st.write_stream(
#                         ask_ai_stream(
#                             question,
#                             langue=langue
#                         )
#                     )

#                 if isinstance(resultat, str) and resultat.strip():

#                     reponse = resultat

#                 else:

#                     reponse = t["no_answer"]
#                     st.warning(reponse)

#             except Exception as erreur:

#                 reponse = t["offline"]

#                 st.error(reponse)

#                 with st.expander("Détails techniques"):

#                     st.code(str(erreur))

#     # Enregistrement de la réponse dans l'historique.
#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": reponse
#         }
#     )


# # =====================================================
# # 15. PIED DE PAGE
# # =====================================================
# st.divider()

# st.caption(
#     "RadiologyBot AI — Prototype de démonstration. "
#     "Les informations doivent être vérifiées et validées "
#     "par le personnel hospitalier."
# )
# Fin coe
# nouveau
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

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
    page_title="RadiologyAi",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================
# 3. LANGUES (détection automatique, plus de liste)
# =====================================================
LANGUES = {"Français": "français", "English": "anglais", "Wolof": "wolof"}

# Mots qui permettent de reconnaître chaque langue
MOTS_WOLOF = {
    "wolof", "nanga", "naka", "jàmm", "jamm", "jërëjëf", "jerejef", "jërejëf",
    "dama", "bëgg", "begg", "laaj", "laajal", "serwiis", "kayit", "yan", "ban",
    "waxtu", "lañuy", "lanuy", "fii", "ubbeeku", "ubbi", "tontu", "waaw",
    "deedeet", "déedéet", "ñu", "dëkk", "toog", "jàppale", "jappale", "yoon",
    "fekk", "nekk", "nekkul", "ndax", "léegi", "legi", "asalaamaalekum",
    "salaam", "maalekum", "lii", "loolu", "lan", "walla", "mbaa", "rekk",
    "mën", "dafa", "amul", "xam", "xamul", "ngi", "maa", "kaay", "dem",
    "indi", "xibaar", "doktoor", "jëm", "fan", "foo", "lu", "dinaa", "dina",
}
MOTS_FR = {
    "le", "la", "les", "des", "du", "de", "un", "une", "est", "sont", "je",
    "vous", "nous", "quel", "quels", "quelle", "quelles", "où", "ou", "et",
    "pour", "dans", "avec", "sur", "que", "qui", "quoi", "comment", "combien",
    "puis", "peut", "bonjour", "salut", "merci", "horaires", "service",
    "examens", "examen", "documents", "apporter", "rendez-vous", "faut",
    "dois", "il", "elle", "au", "aux", "ce", "cette", "mon", "ma", "mes",
    "radiologie", "est-ce", "ai", "suis", "veux", "voudrais", "besoin",
}
MOTS_EN = {
    "the", "is", "are", "what", "where", "how", "do", "does", "can", "i",
    "you", "my", "your", "which", "when", "who", "with", "for", "and", "of",
    "to", "hello", "hi", "thanks", "thank", "please", "hours", "appointment",
    "need", "want", "should", "bring", "open", "available", "department",
    "examinations", "exam", "exams", "it", "there", "this", "that", "me",
}

# Commande explicite : l'utilisateur tape juste le nom de la langue
COMMANDES_LANGUE = {
    "wolof": "Wolof",
    "français": "Français", "francais": "Français", "french": "Français",
    "anglais": "English", "english": "English",
}

CONFIRMATIONS = {
    "Français": "D'accord, je vous répondrai en **français**. Posez votre question.",
    "English": "Sure, I will answer in **English**. Ask your question.",
    "Wolof": "Waaw, dinaa la tontu ci **wolof**. Laajal sa laaj.",
}


def mots(texte):
    return re.findall(r"[\w'’\-àâäçéèêëîïôöùûüÿñœ]+", texte.lower())


def commande_langue(texte):
    """Retourne la langue demandée si le message est juste un nom de langue."""
    tokens = mots(texte)
    if 0 < len(tokens) <= 3:
        for tok in tokens:
            if tok in COMMANDES_LANGUE:
                return COMMANDES_LANGUE[tok]
    return None


def detecter_langue(texte, langue_precedente="Français"):
    """Détecte Français / English / Wolof à partir du texte tapé."""
    tokens = mots(texte)
    sw = sum(1 for m in tokens if m in MOTS_WOLOF)
    sf = sum(1 for m in tokens if m in MOTS_FR)
    se = sum(1 for m in tokens if m in MOTS_EN)
    if re.search(r"[çèùêô]", texte.lower()):
        sf += 1

    if sw >= 1 and sw >= sf and sw >= se:
        return "Wolof"
    if se > sf:
        return "English"
    if sf > se:
        return "Français"
    return langue_precedente


# =====================================================
# 4. TEXTES DE L'INTERFACE
# =====================================================
TEXTES = {
    "Français": {
        "welcome": "Bonjour ! Je suis RadiologyAi.",
        "intro": "Je vous accompagne pour trouver les informations pratiques du service de radiologie.",
        "chat": "Conversation avec RadiologyAi",
        "suggestions": "✨ Questions fréquentes",
        "clear": "🗑️ Effacer la conversation",
        "download": "⬇️ Télécharger la conversation",
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
            "Quels examens sont disponibles ?",
        ],
    },
    "English": {
        "welcome": "Hello! I am RadiologyAi.",
        "intro": "I can help you find practical information about the radiology department.",
        "chat": "Conversation with RadiologyAi",
        "suggestions": "✨ Frequently asked questions",
        "clear": "🗑️ Clear conversation",
        "download": "⬇️ Download conversation",
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
            "Which examinations are available?",
        ],
    },
    "Wolof": {
        "welcome": "Asalaamaalekum ! Maa ngi tudd RadiologyAi.",
        "intro": "Mën naa la jàppale ci xibaar yi jëm ci serwiisu radiologie.",
        "chat": "Waxtaan ak RadiologyAi",
        "suggestions": "✨ Laaj yi ñu faral di laaj",
        "clear": "🗑️ Far waxtaan wi",
        "download": "⬇️ Yebbi waxtaan wi",
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
            "Yan examen lañuy def fii ?",
        ],
    },
}

PLACEHOLDER = "Écrivez en Français, English ou Wolof...  ✍️"

MESSAGE_ACCUEIL = (
    "👋 **Bonjour !** Je suis **RadiologyAi**. Écrivez-moi en **français**.\n\n"
    "👋 **Hello!** I am **RadiologyAi**. Write to me in **English**.\n\n"
    "👋 **Asalaamaalekum !** Maa ngi tudd **RadiologyAi**. Bindal ma ci **wolof**."
)


# =====================================================
# 5. LE ROBOT (SVG animé : yeux qui clignotent)
# =====================================================
ROBOT_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{size}" height="{size}">
  <style>
    .rb-eye {{ transform-box: fill-box; transform-origin: center; animation: rb-blink 4s infinite; }}
    .rb-eye2 {{ animation-delay: 0.02s; }}
    .rb-ant {{ animation: rb-pulse 1.6s ease-in-out infinite; }}
    .rb-bot {{ {float_anim} }}
    .rb-scan {{ animation: rb-scan 3s ease-in-out infinite; }}
    @keyframes rb-blink {{ 0%,90%,100% {{ transform: scaleY(1); }} 94% {{ transform: scaleY(0.07); }} }}
    @keyframes rb-pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
    @keyframes rb-float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
    @keyframes rb-scan {{ 0%,100% {{ opacity: 0.15; }} 50% {{ opacity: 0.6; }} }}
  </style>
  <defs>
    <linearGradient id="rbHead" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bcdcff"/>
    </linearGradient>
    <linearGradient id="rbBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2b8cff"/><stop offset="1" stop-color="#0b4fb3"/>
    </linearGradient>
    <radialGradient id="rbEye" cx="0.5" cy="0.4" r="0.6">
      <stop offset="0" stop-color="#e8fdff"/><stop offset="0.5" stop-color="#4fe3ff"/><stop offset="1" stop-color="#0a9bd8"/>
    </radialGradient>
  </defs>
  <g class="rb-bot">
    <line x1="100" y1="24" x2="100" y2="44" stroke="#5aa9ff" stroke-width="5" stroke-linecap="round"/>
    <circle class="rb-ant" cx="100" cy="17" r="8" fill="#4fe3ff"/>
    <rect x="29" y="72" width="12" height="38" rx="6" fill="#2b8cff"/>
    <rect x="159" y="72" width="12" height="38" rx="6" fill="#2b8cff"/>
    <rect x="40" y="44" width="120" height="92" rx="30" fill="url(#rbHead)" stroke="#2b8cff" stroke-width="3"/>
    <rect x="54" y="62" width="92" height="56" rx="22" fill="#05234a"/>
    <rect class="rb-scan" x="60" y="66" width="80" height="8" rx="4" fill="#4fe3ff"/>
    <ellipse class="rb-eye" cx="80" cy="88" rx="12" ry="14" fill="url(#rbEye)"/>
    <ellipse class="rb-eye rb-eye2" cx="120" cy="88" rx="12" ry="14" fill="url(#rbEye)"/>
    <path d="M86 108 Q100 118 114 108" fill="none" stroke="#4fe3ff" stroke-width="4" stroke-linecap="round"/>
    <rect x="64" y="142" width="72" height="46" rx="16" fill="url(#rbBody)"/>
    <rect x="94" y="152" width="12" height="28" rx="3" fill="#ffffff"/>
    <rect x="86" y="160" width="28" height="12" rx="3" fill="#ffffff"/>
  </g>
</svg>
"""


def robot_html(size=120, flotte=True):
    anim = "animation: rb-float 3.5s ease-in-out infinite;" if flotte else ""
    svg = ROBOT_SVG.format(size=size, float_anim=anim)
    return " ".join(svg.split())  # sur une seule ligne pour Markdown


def avatar_robot():
    """Crée le fichier image du robot pour les bulles de conversation."""
    try:
        chemin = Path(__file__).parent / "robot_avatar.svg"
        chemin.write_text(robot_html(160, flotte=False), encoding="utf-8")
        return str(chemin)
    except Exception:
        return "🤖"


AVATAR_BOT = avatar_robot()


# =====================================================
# 6. DESIGN BLEU
# =====================================================
st.markdown(
    """
    <style>
    #MainMenu, footer { visibility: hidden; }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(56,160,255,0.35) 0%, transparent 40%),
            radial-gradient(circle at 90% 20%, rgba(0,212,255,0.25) 0%, transparent 35%),
            linear-gradient(180deg, #04122b 0%, #07254d 55%, #0a3a73 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        max-width: 1050px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    /* Textes sur fond sombre */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
    .stApp span, .stApp li { color: #eaf4ff; }

    /* ---------- Héros ---------- */
    .hero {
        display: flex; align-items: center; gap: 28px;
        background: linear-gradient(135deg, rgba(20,110,230,0.55), rgba(0,200,255,0.18));
        border: 1px solid rgba(120,200,255,0.35);
        backdrop-filter: blur(10px);
        border-radius: 26px;
        padding: 26px 34px;
        margin-bottom: 18px;
        box-shadow: 0 18px 50px rgba(0,60,160,0.45), inset 0 0 40px rgba(80,180,255,0.10);
    }
    .hero-robot { flex: 0 0 auto; filter: drop-shadow(0 0 22px rgba(79,227,255,0.65)); }
    .hero h1 {
        margin: 0 0 6px 0; font-size: 2.6rem; font-weight: 800; letter-spacing: 0.5px;
        background: linear-gradient(90deg, #ffffff, #8fe6ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p { margin: 0 0 12px 0; color: #cfe8ff; font-size: 1.05rem; }
    .badges span {
        display: inline-block; margin-right: 8px; padding: 5px 14px;
        border-radius: 999px; font-size: 0.85rem; font-weight: 600;
        background: rgba(255,255,255,0.12); border: 1px solid rgba(160,220,255,0.45);
        color: #eaf8ff;
    }
    .status {
        display: inline-block; margin-top: 12px; padding: 5px 14px; border-radius: 999px;
        font-size: 0.85rem; font-weight: 600;
        background: rgba(0,0,0,0.25); border: 1px solid rgba(160,220,255,0.35);
    }
    .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px;
           animation: dotpulse 1.5s infinite; }
    .dot.on  { background:#2be28a; box-shadow:0 0 10px #2be28a; }
    .dot.off { background:#ffb020; box-shadow:0 0 10px #ffb020; }
    @keyframes dotpulse { 0%,100% {opacity:1;} 50% {opacity:0.35;} }

    /* ---------- Avertissement ---------- */
    .notice {
        background: rgba(255,248,231,0.95); border-left: 5px solid #e0a82e;
        color: #5d4a1d !important; padding: 13px 18px; border-radius: 12px;
        margin: 14px 0 20px 0; font-size: 0.92rem;
    }

    /* ---------- Boutons ---------- */
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 14px; min-height: 48px; font-weight: 600;
        color: #ffffff; background: linear-gradient(135deg, #1976f2, #0fb4ff);
        border: 1px solid rgba(160,220,255,0.5);
        box-shadow: 0 6px 18px rgba(0,100,220,0.35);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(0,180,255,0.55);
        border-color: #ffffff; color: #ffffff;
    }
    div.stDownloadButton > button:disabled { opacity: 0.45; }

    /* ---------- Conversation ---------- */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(140,200,255,0.25);
        border-radius: 18px; padding: 14px 18px; margin-bottom: 12px;
        backdrop-filter: blur(6px);
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li { color: #f2f8ff; font-size: 1.02rem; }
    [data-testid="stChatMessage"] img { border-radius: 50%; background: #eaf4ff; }

    /* Champ de saisie */
    [data-testid="stChatInput"] {
        border-radius: 18px; border: 2px solid #3fb8ff;
        box-shadow: 0 0 24px rgba(63,184,255,0.45);
    }
    [data-testid="stBottom"] > div { background: transparent; }

    hr { border-color: rgba(140,200,255,0.25) !important; }
    .stAlert { border-radius: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# 7. SESSION
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggestion_selectionnee" not in st.session_state:
    st.session_state.suggestion_selectionnee = None
if "langue_courante" not in st.session_state:
    st.session_state.langue_courante = "Français"

langue_affichee = st.session_state.langue_courante
t = TEXTES[langue_affichee]


# =====================================================
# 8. EN-TÊTE AVEC ROBOT ANIMÉ
# =====================================================
if ERREUR_IMPORT is not None:
    moteur_disponible = False
else:
    try:
        moteur_disponible = bool(service_pret())
    except Exception:
        moteur_disponible = False

etat_classe = "on" if moteur_disponible else "off"
etat_texte = t["online"] if moteur_disponible else t["offline_short"]

st.markdown(
    f"""<div class="hero">
    <div class="hero-robot">{robot_html(150)}</div>
    <div>
        <h1>RadiologyAi</h1>
        <p>Assistant intelligent du service de radiologie</p>
        <div class="badges"><span>🇫🇷 Français</span><span>🇬🇧 English</span><span>🇸🇳 Wolof</span></div>
        <div class="status"><span class="dot {etat_classe}"></span>{etat_texte}</div>
    </div>
</div>""",
    unsafe_allow_html=True,
)

if ERREUR_IMPORT is not None:
    st.error(
        "Impossible de charger chatbot.py. "
        "Vérifiez que ce fichier est présent dans le même dossier que app.py."
    )
    with st.expander("Détails de l'erreur"):
        st.code(str(ERREUR_IMPORT))


# =====================================================
# 9. ACCUEIL ET AVERTISSEMENT
# =====================================================
st.subheader(t["welcome"])
st.write(t["intro"])
st.markdown(f'<div class="notice">⚠️ {t["disclaimer"]}</div>', unsafe_allow_html=True)


# =====================================================
# 10. QUESTIONS FRÉQUENTES (dans la langue détectée)
# =====================================================
st.subheader(t["suggestions"])
colonnes = st.columns(2)
for index, suggestion in enumerate(t["quick"]):
    with colonnes[index % 2]:
        if st.button(
            suggestion,
            key=f"suggestion_{langue_affichee}_{index}",
            use_container_width=True,
        ):
            st.session_state.suggestion_selectionnee = suggestion


# =====================================================
# 11. EFFACER ET TÉLÉCHARGER
# =====================================================
col_effacer, col_telecharger = st.columns(2)

with col_effacer:
    if st.button(t["clear"], use_container_width=True):
        st.session_state.messages = []
        st.session_state.suggestion_selectionnee = None
        st.rerun()

with col_telecharger:
    contenu = []
    for message in st.session_state.messages:
        role = "Utilisateur" if message["role"] == "user" else "RadiologyAi"
        contenu.append(f"{role} :\n{message['content']}")
    st.download_button(
        label=t["download"],
        data="\n\n".join(contenu) or "Aucune conversation.",
        file_name=f"radiologyai_conversation_{datetime.now():%Y%m%d_%H%M}.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(st.session_state.messages),
    )


# =====================================================
# 12. HISTORIQUE (robot = avatar des réponses)
# =====================================================
st.divider()
st.subheader(t["chat"])

if not st.session_state.messages:
    with st.chat_message("assistant", avatar=AVATAR_BOT):
        st.markdown(MESSAGE_ACCUEIL)

for message in st.session_state.messages:
    avatar = AVATAR_BOT if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# =====================================================
# 13. SAISIE
# =====================================================
question_saisie = st.chat_input(PLACEHOLDER)

question = question_saisie if question_saisie is not None else st.session_state.suggestion_selectionnee
st.session_state.suggestion_selectionnee = None


# =====================================================
# 14. TRAITEMENT : détection de langue + RAG
# =====================================================
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    # Commande directe : l'utilisateur tape "wolof", "français" ou "english"
    langue_demandee = commande_langue(question)

    if langue_demandee:
        st.session_state.langue_courante = langue_demandee
        reponse = CONFIRMATIONS[langue_demandee]
        with st.chat_message("assistant", avatar=AVATAR_BOT):
            st.markdown(reponse)
    else:
        # Détection automatique de la langue de la question
        langue_detectee = detecter_langue(question, st.session_state.langue_courante)
        st.session_state.langue_courante = langue_detectee
        td = TEXTES[langue_detectee]
        langue_rag = LANGUES[langue_detectee]

        with st.chat_message("assistant", avatar=AVATAR_BOT):
            if ask_ai_stream is None:
                reponse = td["offline"]
                st.error(reponse)
            else:
                try:
                    with st.spinner(td["thinking"]):
                        resultat = st.write_stream(
                            ask_ai_stream(question, langue=langue_rag)
                        )
                    if isinstance(resultat, str) and resultat.strip():
                        reponse = resultat
                    else:
                        reponse = td["no_answer"]
                        st.warning(reponse)
                except Exception as erreur:
                    reponse = td["offline"]
                    st.error(reponse)
                    with st.expander("Détails techniques"):
                        st.code(str(erreur))

    st.session_state.messages.append({"role": "assistant", "content": reponse})

    # Rafraîchit l'interface (suggestions, textes) dans la langue détectée
    st.rerun()


# =====================================================
# 15. PIED DE PAGE
# =====================================================
st.divider()
st.caption(
    "RadiologyAi — Prototype de démonstration. "
    "Les informations doivent être vérifiées et validées par le personnel hospitalier."
)
