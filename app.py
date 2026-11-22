
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


# # #import re
# from datetime import datetime
# from pathlib import Path

# import streamlit as st

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
#     page_title="RadiologyAi",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )


# # =====================================================
# # 3. LANGUES (détection automatique, plus de liste)
# # =====================================================
# LANGUES = {"Français": "français", "English": "anglais", "Wolof": "wolof"}

# # Mots qui permettent de reconnaître chaque langue
# MOTS_WOLOF = {
#     "wolof", "nanga", "naka", "jàmm", "jamm", "jërëjëf", "jerejef", "jërejëf",
#     "dama", "bëgg", "begg", "laaj", "laajal", "serwiis", "kayit", "yan", "ban",
#     "waxtu", "lañuy", "lanuy", "fii", "ubbeeku", "ubbi", "tontu", "waaw",
#     "deedeet", "déedéet", "ñu", "dëkk", "toog", "jàppale", "jappale", "yoon",
#     "fekk", "nekk", "nekkul", "ndax", "léegi", "legi", "asalaamaalekum",
#     "salaam", "maalekum", "lii", "loolu", "lan", "walla", "mbaa", "rekk",
#     "mën", "dafa", "amul", "xam", "xamul", "ngi", "maa", "kaay", "dem",
#     "indi", "xibaar", "doktoor", "jëm", "fan", "foo", "lu", "dinaa", "dina",
# }
# MOTS_FR = {
#     "le", "la", "les", "des", "du", "de", "un", "une", "est", "sont", "je",
#     "vous", "nous", "quel", "quels", "quelle", "quelles", "où", "ou", "et",
#     "pour", "dans", "avec", "sur", "que", "qui", "quoi", "comment", "combien",
#     "puis", "peut", "bonjour", "salut", "merci", "horaires", "service",
#     "examens", "examen", "documents", "apporter", "rendez-vous", "faut",
#     "dois", "il", "elle", "au", "aux", "ce", "cette", "mon", "ma", "mes",
#     "radiologie", "est-ce", "ai", "suis", "veux", "voudrais", "besoin",
# }
# MOTS_EN = {
#     "the", "is", "are", "what", "where", "how", "do", "does", "can", "i",
#     "you", "my", "your", "which", "when", "who", "with", "for", "and", "of",
#     "to", "hello", "hi", "thanks", "thank", "please", "hours", "appointment",
#     "need", "want", "should", "bring", "open", "available", "department",
#     "examinations", "exam", "exams", "it", "there", "this", "that", "me",
# }

# # Commande explicite : l'utilisateur tape juste le nom de la langue
# COMMANDES_LANGUE = {
#     "wolof": "Wolof",
#     "français": "Français", "francais": "Français", "french": "Français",
#     "anglais": "English", "english": "English",
# }

# CONFIRMATIONS = {
#     "Français": "D'accord, je vous répondrai en **français**. Posez votre question.",
#     "English": "Sure, I will answer in **English**. Ask your question.",
#     "Wolof": "Waaw, dinaa la tontu ci **wolof**. Laajal sa laaj.",
# }


# def mots(texte):
#     return re.findall(r"[\w'’\-àâäçéèêëîïôöùûüÿñœ]+", texte.lower())


# def commande_langue(texte):
#     """Retourne la langue demandée si le message est juste un nom de langue."""
#     tokens = mots(texte)
#     if 0 < len(tokens) <= 3:
#         for tok in tokens:
#             if tok in COMMANDES_LANGUE:
#                 return COMMANDES_LANGUE[tok]
#     return None


# def detecter_langue(texte, langue_precedente="Français"):
#     """Détecte Français / English / Wolof à partir du texte tapé."""
#     tokens = mots(texte)
#     sw = sum(1 for m in tokens if m in MOTS_WOLOF)
#     sf = sum(1 for m in tokens if m in MOTS_FR)
#     se = sum(1 for m in tokens if m in MOTS_EN)
#     if re.search(r"[çèùêô]", texte.lower()):
#         sf += 1

#     if sw >= 1 and sw >= sf and sw >= se:
#         return "Wolof"
#     if se > sf:
#         return "English"
#     if sf > se:
#         return "Français"
#     return langue_precedente


# # =====================================================
# # 4. TEXTES DE L'INTERFACE
# # =====================================================
# TEXTES = {
#     "Français": {
#         "welcome": "Bonjour ! Je suis RadiologyAi.",
#         "intro": "Je vous accompagne pour trouver les informations pratiques du service de radiologie.",
#         "chat": "Conversation avec RadiologyAi",
#         "suggestions": "✨ Questions fréquentes",
#         "clear": "🗑️ Effacer la conversation",
#         "download": "⬇️ Télécharger la conversation",
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
#             "Quels examens sont disponibles ?",
#         ],
#     },
#     "English": {
#         "welcome": "Hello! I am RadiologyAi.",
#         "intro": "I can help you find practical information about the radiology department.",
#         "chat": "Conversation with RadiologyAi",
#         "suggestions": "✨ Frequently asked questions",
#         "clear": "🗑️ Clear conversation",
#         "download": "⬇️ Download conversation",
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
#             "Which examinations are available?",
#         ],
#     },
#     "Wolof": {
#         "welcome": "Asalaamaalekum ! Maa ngi tudd RadiologyAi.",
#         "intro": "Mën naa la jàppale ci xibaar yi jëm ci serwiisu radiologie.",
#         "chat": "Waxtaan ak RadiologyAi",
#         "suggestions": "✨ Laaj yi ñu faral di laaj",
#         "clear": "🗑️ Far waxtaan wi",
#         "download": "⬇️ Yebbi waxtaan wi",
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
#             "Yan examen lañuy def fii ?",
#         ],
#     },
# }

# PLACEHOLDER = "Écrivez en Français, English ou Wolof...  ✍️"

# MESSAGE_ACCUEIL = (
#     "👋 **Bonjour !** Je suis **RadiologyAi**. Écrivez-moi en **français**.\n\n"
#     "👋 **Hello!** I am **RadiologyAi**. Write to me in **English**.\n\n"
#     "👋 **Asalaamaalekum !** Maa ngi tudd **RadiologyAi**. Bindal ma ci **wolof**."
# )


# # =====================================================
# # 5. LE ROBOT (SVG animé : yeux qui clignotent, main qui salue)
# # =====================================================
# ROBOT_SVG = """
# <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 270" width="{size}" height="{size}">
#   <style>
#     .rb-eye {{ transform-box: fill-box; transform-origin: center; animation: rb-blink 4s infinite; }}
#     .rb-eye2 {{ animation-delay: 0.02s; }}
#     .rb-ant {{ animation: rb-pulse 1.6s ease-in-out infinite; }}
#     .rb-bot {{ {float_anim} }}
#     .rb-scan {{ animation: rb-scan 3s ease-in-out infinite; }}
#     .rb-wave {{ transform-origin: 176px 178px; animation: rb-wave 2.4s ease-in-out infinite; }}
#     .rb-shadow {{ transform-box: fill-box; transform-origin: center; animation: rb-shadow 3.5s ease-in-out infinite; }}
#     .rb-core {{ animation: rb-pulse 2s ease-in-out infinite; }}
#     @keyframes rb-blink {{ 0%,90%,100% {{ transform: scaleY(1); }} 94% {{ transform: scaleY(0.07); }} }}
#     @keyframes rb-pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
#     @keyframes rb-float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
#     @keyframes rb-scan {{ 0%,100% {{ opacity: 0.1; }} 50% {{ opacity: 0.55; }} }}
#     @keyframes rb-wave {{ 0%,100% {{ transform: rotate(-8deg); }} 50% {{ transform: rotate(22deg); }} }}
#     @keyframes rb-shadow {{ 0%,100% {{ transform: scale(1); opacity: 0.35; }} 50% {{ transform: scale(0.85); opacity: 0.2; }} }}
#   </style>
#   <defs>
#     <linearGradient id="rbHead" x1="0" y1="0" x2="0" y2="1">
#       <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c9f5de"/>
#     </linearGradient>
#     <linearGradient id="rbBody" x1="0" y1="0" x2="0" y2="1">
#       <stop offset="0" stop-color="#1fbf83"/><stop offset="1" stop-color="#075c3d"/>
#     </linearGradient>
#     <radialGradient id="rbEye" cx="0.5" cy="0.4" r="0.6">
#       <stop offset="0" stop-color="#f2fff8"/><stop offset="0.5" stop-color="#5dffb0"/><stop offset="1" stop-color="#0fae6b"/>
#     </radialGradient>
#   </defs>
#   <ellipse class="rb-shadow" cx="120" cy="256" rx="52" ry="8" fill="#000000"/>
#   <g class="rb-bot">
#     <line x1="120" y1="30" x2="120" y2="54" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
#     <circle class="rb-ant" cx="120" cy="22" r="10" fill="#5dffb0"/>
#     <rect x="36" y="86" width="14" height="46" rx="7" fill="#10b981"/>
#     <rect x="190" y="86" width="14" height="46" rx="7" fill="#10b981"/>
#     <rect x="50" y="54" width="140" height="108" rx="38" fill="url(#rbHead)" stroke="#10b981" stroke-width="4"/>
#     <rect x="66" y="74" width="108" height="68" rx="26" fill="#02261a"/>
#     <rect class="rb-scan" x="74" y="80" width="92" height="9" rx="4" fill="#5dffb0"/>
#     <ellipse class="rb-eye" cx="98" cy="106" rx="14" ry="17" fill="url(#rbEye)"/>
#     <ellipse class="rb-eye rb-eye2" cx="142" cy="106" rx="14" ry="17" fill="url(#rbEye)"/>
#     <path d="M104 128 Q120 140 136 128" fill="none" stroke="#5dffb0" stroke-width="5" stroke-linecap="round"/>
#     <rect x="80" y="168" width="80" height="70" rx="22" fill="url(#rbBody)"/>
#     <rect x="114" y="180" width="12" height="32" rx="3" fill="#ffffff"/>
#     <rect x="104" y="190" width="32" height="12" rx="3" fill="#ffffff"/>
#     <circle class="rb-core" cx="120" cy="224" r="5" fill="#5dffb0"/>
#     <rect x="58" y="176" width="14" height="46" rx="7" fill="#10b981"/>
#     <g class="rb-wave">
#       <rect x="168" y="172" width="14" height="48" rx="7" fill="#10b981"/>
#       <circle cx="175" cy="224" r="10" fill="#c9f5de" stroke="#10b981" stroke-width="3"/>
#     </g>
#   </g>
# </svg>
# """


# def robot_html(size=120, flotte=True):
#     anim = "animation: rb-float 3.5s ease-in-out infinite;" if flotte else ""
#     svg = ROBOT_SVG.format(size=size, float_anim=anim)
#     return " ".join(svg.split())  # sur une seule ligne pour Markdown


# def avatar_robot():
#     """Crée le fichier image du robot pour les bulles de conversation."""
#     try:
#         chemin = Path(__file__).parent / "robot_avatar.svg"
#         chemin.write_text(robot_html(160, flotte=False), encoding="utf-8")
#         return str(chemin)
#     except Exception:
#         return "🤖"


# AVATAR_BOT = avatar_robot()


# # =====================================================
# # 6. DESIGN VERT FONCÉ
# # =====================================================
# st.markdown(
#     """
#     <style>
#     #MainMenu, footer { visibility: hidden; }

#     .stApp {
#         background:
#             radial-gradient(circle at 12% 8%, rgba(16,185,129,0.30) 0%, transparent 38%),
#             radial-gradient(circle at 92% 18%, rgba(110,231,183,0.16) 0%, transparent 34%),
#             linear-gradient(rgba(110,231,183,0.045) 1px, transparent 1px),
#             linear-gradient(90deg, rgba(110,231,183,0.045) 1px, transparent 1px),
#             linear-gradient(180deg, #021510 0%, #05281c 55%, #08402b 100%);
#         background-size: auto, auto, 42px 42px, 42px 42px, auto;
#         background-attachment: fixed;
#     }

#     .main .block-container {
#         max-width: 1100px;
#         padding-top: 1.5rem;
#         padding-bottom: 6rem;
#     }

#     .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
#     .stApp span, .stApp li { color: #e8fff3; }

#     /* ---------- Héros ---------- */
#     .hero {
#         position: relative; overflow: hidden;
#         display: flex; align-items: center; gap: 40px;
#         background: linear-gradient(135deg, rgba(8,90,60,0.75), rgba(3,35,25,0.80));
#         border: 1px solid rgba(110,231,183,0.45);
#         border-radius: 30px;
#         padding: 34px 44px;
#         margin-bottom: 22px;
#         box-shadow: 0 22px 60px rgba(0,0,0,0.55),
#                     0 0 50px rgba(16,185,129,0.25),
#                     inset 0 0 60px rgba(52,211,153,0.10);
#     }
#     .hero::before {
#         content: ""; position: absolute; width: 420px; height: 420px; right: -120px; top: -160px;
#         background: radial-gradient(circle, rgba(93,255,176,0.30), transparent 65%);
#         animation: glow 6s ease-in-out infinite;
#     }
#     @keyframes glow { 0%,100% {opacity:0.5; transform:scale(1);} 50% {opacity:1; transform:scale(1.15);} }
#     .hero-robot {
#         position: relative; flex: 0 0 auto; line-height: 0;
#         filter: drop-shadow(0 0 28px rgba(93,255,176,0.55));
#     }
#     .hero-text { position: relative; }
#     .hero h1 {
#         margin: 0 0 8px 0; font-size: 3.4rem; font-weight: 800; letter-spacing: 0.5px; line-height: 1.05;
#         background: linear-gradient(90deg, #ffffff, #86efc0 60%, #34d399);
#         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     }
#     .hero p { margin: 0 0 16px 0; color: #b9f3d6; font-size: 1.2rem; }
#     .badges span {
#         display: inline-block; margin: 0 8px 6px 0; padding: 6px 16px;
#         border-radius: 999px; font-size: 0.9rem; font-weight: 600;
#         background: rgba(110,231,183,0.12); border: 1px solid rgba(110,231,183,0.50);
#         color: #e8fff3;
#     }
#     .status {
#         display: inline-block; margin-top: 10px; padding: 6px 16px; border-radius: 999px;
#         font-size: 0.9rem; font-weight: 600;
#         background: rgba(0,0,0,0.35); border: 1px solid rgba(110,231,183,0.35);
#     }
#     .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:8px;
#            animation: dotpulse 1.5s infinite; }
#     .dot.on  { background:#5dffb0; box-shadow:0 0 12px #5dffb0; }
#     .dot.off { background:#ffb020; box-shadow:0 0 12px #ffb020; }
#     @keyframes dotpulse { 0%,100% {opacity:1;} 50% {opacity:0.35;} }

#     @media (max-width: 760px) {
#         .hero { flex-direction: column; text-align: center; padding: 26px 20px; gap: 14px; }
#         .hero h1 { font-size: 2.4rem; }
#     }

#     /* ---------- Avertissement ---------- */
#     .notice {
#         background: rgba(255,247,222,0.96); border-left: 5px solid #d9a21f;
#         color: #4d3b0f !important; padding: 13px 18px; border-radius: 12px;
#         margin: 14px 0 20px 0; font-size: 0.92rem;
#     }

#     /* ---------- Boutons ---------- */
#     div.stButton > button, div.stDownloadButton > button {
#         border-radius: 14px; min-height: 50px; font-weight: 600;
#         color: #ffffff; background: linear-gradient(135deg, #0c7a53, #14b378);
#         border: 1px solid rgba(110,231,183,0.55);
#         box-shadow: 0 6px 18px rgba(0,0,0,0.35);
#         transition: all 0.2s ease;
#     }
#     div.stButton > button:hover, div.stDownloadButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 10px 28px rgba(52,211,153,0.50);
#         border-color: #ffffff; color: #ffffff;
#     }
#     div.stDownloadButton > button:disabled { opacity: 0.4; }

#     /* ---------- Conversation ---------- */
#     [data-testid="stChatMessage"] {
#         background: rgba(8,70,48,0.55);
#         border: 1px solid rgba(110,231,183,0.30);
#         border-radius: 20px; padding: 16px 20px; margin-bottom: 14px;
#         box-shadow: 0 6px 20px rgba(0,0,0,0.25);
#     }
#     [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
#         background: rgba(20,179,120,0.28);
#         border-color: rgba(134,239,192,0.55);
#     }
#     [data-testid="stChatMessage"] p,
#     [data-testid="stChatMessage"] li { color: #f0fff7; font-size: 1.04rem; line-height: 1.6; }
#     [data-testid="stChatMessage"] img { border-radius: 50%; background: #d9fbe9; padding: 2px; }

#     /* ---------- Champ de saisie ---------- */
#     [data-testid="stChatInput"] {
#         background: #eafff4;
#         border-radius: 18px; border: 2px solid #34d399;
#         box-shadow: 0 0 26px rgba(52,211,153,0.50);
#     }
#     [data-testid="stChatInput"] textarea { color: #053a27 !important; }
#     [data-testid="stChatInput"] textarea::placeholder { color: #3f7a63 !important; }
#     [data-testid="stBottom"] > div { background: transparent; }

#     hr { border-color: rgba(110,231,183,0.25) !important; }
#     .stAlert { border-radius: 14px; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # =====================================================
# # 7. SESSION
# # =====================================================
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "suggestion_selectionnee" not in st.session_state:
#     st.session_state.suggestion_selectionnee = None
# if "langue_courante" not in st.session_state:
#     st.session_state.langue_courante = "Français"

# langue_affichee = st.session_state.langue_courante
# t = TEXTES[langue_affichee]


# # =====================================================
# # 8. EN-TÊTE AVEC ROBOT ANIMÉ
# # =====================================================
# if ERREUR_IMPORT is not None:
#     moteur_disponible = False
# else:
#     try:
#         moteur_disponible = bool(service_pret())
#     except Exception:
#         moteur_disponible = False

# etat_classe = "on" if moteur_disponible else "off"
# etat_texte = t["online"] if moteur_disponible else t["offline_short"]

# st.markdown(
#     f"""<div class="hero">
#     <div class="hero-robot">{robot_html(250)}</div>
#     <div class="hero-text">
#         <h1>RadiologyAi</h1>
#         <p>Assistant intelligent du service de radiologie</p>
#         <div class="badges"><span>🇫🇷 Français</span><span>🇬🇧 English</span><span>🇸🇳 Wolof</span></div>
#         <div class="status"><span class="dot {etat_classe}"></span>{etat_texte}</div>
#     </div>
# </div>""",
#     unsafe_allow_html=True,
# )

# if ERREUR_IMPORT is not None:
#     st.error(
#         "Impossible de charger chatbot.py. "
#         "Vérifiez que ce fichier est présent dans le même dossier que app.py."
#     )
#     with st.expander("Détails de l'erreur"):
#         st.code(str(ERREUR_IMPORT))


# # =====================================================
# # 9. ACCUEIL ET AVERTISSEMENT
# # =====================================================
# st.subheader(t["welcome"])
# st.write(t["intro"])
# st.markdown(f'<div class="notice">⚠️ {t["disclaimer"]}</div>', unsafe_allow_html=True)


# # =====================================================
# # 10. QUESTIONS FRÉQUENTES (dans la langue détectée)
# # =====================================================
# st.subheader(t["suggestions"])
# colonnes = st.columns(2)
# for index, suggestion in enumerate(t["quick"]):
#     with colonnes[index % 2]:
#         if st.button(
#             suggestion,
#             key=f"suggestion_{langue_affichee}_{index}",
#             use_container_width=True,
#         ):
#             st.session_state.suggestion_selectionnee = suggestion


# # =====================================================
# # 11. EFFACER ET TÉLÉCHARGER
# # =====================================================
# col_effacer, col_telecharger = st.columns(2)

# with col_effacer:
#     if st.button(t["clear"], use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.suggestion_selectionnee = None
#         st.rerun()

# with col_telecharger:
#     contenu = []
#     for message in st.session_state.messages:
#         role = "Utilisateur" if message["role"] == "user" else "RadiologyAi"
#         contenu.append(f"{role} :\n{message['content']}")
#     st.download_button(
#         label=t["download"],
#         data="\n\n".join(contenu) or "Aucune conversation.",
#         file_name=f"radiologyai_conversation_{datetime.now():%Y%m%d_%H%M}.txt",
#         mime="text/plain",
#         use_container_width=True,
#         disabled=not bool(st.session_state.messages),
#     )


# # =====================================================
# # 12. HISTORIQUE (robot = avatar des réponses)
# # =====================================================
# st.divider()
# st.subheader(t["chat"])

# if not st.session_state.messages:
#     with st.chat_message("assistant", avatar=AVATAR_BOT):
#         st.markdown(MESSAGE_ACCUEIL)

# for message in st.session_state.messages:
#     avatar = AVATAR_BOT if message["role"] == "assistant" else "🧑"
#     with st.chat_message(message["role"], avatar=avatar):
#         st.markdown(message["content"])


# # =====================================================
# # 13. SAISIE
# # =====================================================
# question_saisie = st.chat_input(PLACEHOLDER)

# question = question_saisie if question_saisie is not None else st.session_state.suggestion_selectionnee
# st.session_state.suggestion_selectionnee = None


# # =====================================================
# # 14. TRAITEMENT : détection de langue + RAG
# # =====================================================
# if question:
#     st.session_state.messages.append({"role": "user", "content": question})
#     with st.chat_message("user", avatar="🧑"):
#         st.markdown(question)

#     # Commande directe : l'utilisateur tape "wolof", "français" ou "english"
#     langue_demandee = commande_langue(question)

#     if langue_demandee:
#         st.session_state.langue_courante = langue_demandee
#         reponse = CONFIRMATIONS[langue_demandee]
#         with st.chat_message("assistant", avatar=AVATAR_BOT):
#             st.markdown(reponse)
#     else:
#         # Détection automatique de la langue de la question
#         langue_detectee = detecter_langue(question, st.session_state.langue_courante)
#         st.session_state.langue_courante = langue_detectee
#         td = TEXTES[langue_detectee]
#         langue_rag = LANGUES[langue_detectee]

#         with st.chat_message("assistant", avatar=AVATAR_BOT):
#             if ask_ai_stream is None:
#                 reponse = td["offline"]
#                 st.error(reponse)
#             else:
#                 try:
#                     with st.spinner(td["thinking"]):
#                         resultat = st.write_stream(
#                             ask_ai_stream(question, langue=langue_rag)
#                         )
#                     if isinstance(resultat, str) and resultat.strip():
#                         reponse = resultat
#                     else:
#                         reponse = td["no_answer"]
#                         st.warning(reponse)
#                 except Exception as erreur:
#                     reponse = td["offline"]
#                     st.error(reponse)
#                     with st.expander("Détails techniques"):
#                         st.code(str(erreur))

#     st.session_state.messages.append({"role": "assistant", "content": reponse})

#     # Rafraîchit l'interface (suggestions, textes) dans la langue détectée
#     st.rerun()


# # =====================================================
# # 15. PIED DE PAGE
# # =====================================================
# st.divider()
# st.caption(
#     "RadiologyAi — Prototype de démonstration. "
#     "Les informations doivent être vérifiées et validées par le personnel hospitalier."
# ) =====================================================
# # # 15. PIED DE PAGE
# # # =====================================================
# # st.divider()

# # st.caption(
# #     "RadiologyBot AI — Prototype de démonstration. "
# #     "Les informations doivent être vérifiées et validées "
# #     "par le personnel hospitalier."
# # )
# Fin coe
# nouveau

# import re
# from datetime import datetime
# from pathlib import Path

# import streamlit as st

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
#     page_title="RadiologyAi — Assistant Service de Radiologie",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )


# # =====================================================
# # 3. LANGUES (détection directe Français / Wolof / English)
# # =====================================================
# LANGUES = {
#     "Français": "français",
#     "English": "anglais",
#     "Wolof": "wolof",
# }

# MOTS_WOLOF = {
#     "wolof", "nanga", "naka", "def", "jàmm", "jamm", "jërëjëf", "jerejef",
#     "jërejëf", "dama", "bëgg", "begg", "laaj", "laajal", "serwiis", "kayit",
#     "yan", "ban", "waxtu", "lañuy", "lanuy", "fii", "ubbeeku", "ubbi", "tontu",
#     "waaw", "deedeet", "déedéet", "ñu", "dëkk", "toog", "jàppale", "jappale",
#     "yoon", "fekk", "nekk", "nekkul", "ndax", "léegi", "legi", "asalaamaalekum",
#     "salaam", "maalekum", "lii", "loolu", "lan", "walla", "mbaa", "rekk",
#     "mën", "men", "dafa", "amul", "xam", "xamul", "ngi", "maa", "kaay", "dem",
#     "indi", "xibaar", "doktoor", "jëm", "fan", "foo", "lu", "dinaa", "dina",
#     "ekografi", "radio", "scanner", "irm", "randez", "wute", "sante",
# }

# MOTS_FR = {
#     "le", "la", "les", "des", "du", "de", "un", "une", "est", "sont", "je",
#     "vous", "nous", "quel", "quels", "quelle", "quelles", "où", "ou", "et",
#     "pour", "dans", "avec", "sur", "que", "qui", "quoi", "comment", "combien",
#     "puis", "peut", "bonjour", "salut", "merci", "horaires", "service",
#     "examens", "examen", "documents", "apporter", "rendez-vous", "faut",
#     "dois", "il", "elle", "au", "aux", "ce", "cette", "mon", "ma", "mes",
#     "radiologie", "est-ce", "ai", "suis", "veux", "voudrais", "besoin",
#     "échographie", "scanner", "irm", "préparation", "résultats",
# }

# MOTS_EN = {
#     "the", "is", "are", "what", "where", "how", "do", "does", "can", "i",
#     "you", "my", "your", "which", "when", "who", "with", "for", "and", "of",
#     "to", "hello", "hi", "thanks", "thank", "please", "hours", "appointment",
#     "need", "want", "should", "bring", "open", "available", "department",
#     "examinations", "exam", "exams", "it", "there", "this", "that", "me",
#     "ultrasound", "ct", "mri", "xray", "x-ray", "results", "preparation",
# }

# COMMANDES_LANGUE = {
#     "wolof": "Wolof",
#     "français": "Français",
#     "francais": "Français",
#     "french": "Français",
#     "anglais": "English",
#     "english": "English",
# }

# CONFIRMATIONS = {
#     "Français": "Parfait, je vous répondrai directement en **français**. Posez votre question sur le service de radiologie.",
#     "English": "Understood, I will answer directly in **English**. Ask your question about the radiology department.",
#     "Wolof": "Waaw, dinaa la tontu ci **wolof** ci saa si. Laajal sa laaj ci serwiisu radiologie.",
# }


# def mots(texte: str) -> list[str]:
#     return re.findall(r"[\w'’\-àâäçéèêëîïôöùûüÿñœ]+", texte.lower())


# def commande_langue(texte: str) -> str | None:
#     tokens = mots(texte)
#     if 0 < len(tokens) <= 3:
#         for tok in tokens:
#             if tok in COMMANDES_LANGUE:
#                 return COMMANDES_LANGUE[tok]
#     return None


# def detecter_langue(texte: str, langue_precedente: str = "Français") -> str:
#     tokens = mots(texte)
#     sw = sum(1 for m in tokens if m in MOTS_WOLOF)
#     sf = sum(1 for m in tokens if m in MOTS_FR)
#     se = sum(1 for m in tokens if m in MOTS_EN)

#     if re.search(r"[çèùêôàéîï]", texte.lower()):
#         sf += 1

#     scores = {"Wolof": sw, "Français": sf, "English": se}
#     meilleure = max(scores, key=scores.get)
#     if scores[meilleure] > 0:
#         return meilleure
#     return langue_precedente


# # =====================================================
# # 4. TEXTES DE L'INTERFACE
# # =====================================================
# TEXTES = {
#     "Français": {
#         "welcome": "Bienvenue au service de radiologie — RadiologyAi",
#         "intro": "Orientation rapide, préparation aux examens, horaires et documents à prévoir.",
#         "chat": "Échange en direct avec RadiologyAi",
#         "suggestions": "✨ Questions fréquentes des patients",
#         "clear": "🗑️ Nouvelle discussion",
#         "download": "⬇️ Exporter l'échange",
#         "disclaimer": "Information d'orientation uniquement. RadiologyAi ne remplace pas un médecin radiologue et n'établit aucun diagnostic médical.",
#         "thinking": "Consultation de la base documentaire de radiologie...",
#         "offline": "Le moteur d'assistance est momentanément indisponible. Veuillez réessayer ou vous adresser à l'accueil de la radiologie.",
#         "no_answer": "Aucune réponse n'a pu être générée. Merci de reformuler votre question.",
#         "online": "Moteur RAG opérationnel",
#         "offline_short": "Moteur RAG hors ligne",
#         "lang_badge": "Langue active : Français",
#         "quick": [
#             "Quels sont les horaires d'ouverture de la radiologie ?",
#             "Quels documents dois-je apporter pour mon examen ?",
#             "Comment se préparer à une échographie ou un scanner ?",
#             "Où se situe le service de radiologie ?",
#         ],
#     },
#     "English": {
#         "welcome": "Welcome to Radiology — RadiologyAi",
#         "intro": "Instant guidance on opening hours, exam preparation, required documents, and location.",
#         "chat": "Live conversation with RadiologyAi",
#         "suggestions": "✨ Frequent patient questions",
#         "clear": "🗑️ New chat",
#         "download": "⬇️ Export transcript",
#         "disclaimer": "General guidance only. RadiologyAi does not replace a radiologist or healthcare professional and does not provide medical diagnoses.",
#         "thinking": "Searching radiology department knowledge base...",
#         "offline": "The assistant service is temporarily unavailable. Please try again later or contact the radiology front desk.",
#         "no_answer": "I could not generate a response. Please rephrase your question.",
#         "online": "RAG engine online",
#         "offline_short": "RAG engine offline",
#         "lang_badge": "Active language: English",
#         "quick": [
#             "What are the radiology department opening hours?",
#             "Which documents should I bring for my exam?",
#             "How do I prepare for an ultrasound or CT scan?",
#             "Where is the radiology department located?",
#         ],
#     },
#     "Wolof": {
#         "welcome": "Dalal ak jàmm ci serwiisu radiologie — RadiologyAi",
#         "intro": "Jàppale bu gaaw ci waxtuy ubbiku, waajtaayoo examen, kayit yi ak barab bi.",
#         "chat": "Waxtaan ak RadiologyAi",
#         "suggestions": "✨ Laaj yi ñu gëna faral di laaj",
#         "clear": "🗑️ Waxtaan bu bees",
#         "download": "⬇️ Yebbi waxtaan wi",
#         "disclaimer": "Xibaar ngir gindi rekk. RadiologyAi du wuutu doktoor te du def diagnoos.",
#         "thinking": "Maa ngi seet ci xibaar yi jëm ci radiologie...",
#         "offline": "Serwiis bi amul léegi. Jéemaatal ci kanam tuuti walla nga dem ci accueil radiologie.",
#         "no_answer": "Manul naa tontu. Jéemaatal di laaj ci beneen anam.",
#         "online": "Moteur RAG dafa ubbiku",
#         "offline_short": "Moteur RAG dafa tëju",
#         "lang_badge": "Làkk wi : Wolof",
#         "quick": [
#             "Ban waxtu la serwiisu radiologie di ubbeeku ?",
#             "Yan kayit laa war a indi ngir sama examen ?",
#             "Naka laay waajtaayoo ngir ekografi walla scanner ?",
#             "Ana la serwiisu radiologie nekk ?",
#         ],
#     },
# }

# PLACEHOLDER = "Posez votre question en Français, Wolof ou English...  ✍️"

# MESSAGE_ACCUEIL = (
#     "👋 **Bonjour !** Je suis **RadiologyAi**. Écrivez directement en **français**.\n\n"
#     "👋 **Asalaamaalekum !** Maa ngi tudd **RadiologyAi**. Bindal ci **wolof** ci saa si.\n\n"
#     "👋 **Hello!** I am **RadiologyAi**. Write directly in **English**."
# )


# # =====================================================
# # 5. GRAND ROBOT BLEU DE NUIT FONCÉ (YEUX QUI CLIGNOTENT)
# # =====================================================
# ROBOT_SVG = """
# <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 295" width="{size}" height="{size}" role="img" aria-label="Grand robot bleu de nuit foncé RadiologyAi">
#   <style>
#     .rb-eye {{ transform-box: fill-box; transform-origin: center; animation: rb-blink 3.6s infinite; }}
#     .rb-eye2 {{ animation-delay: 0.03s; }}
#     .rb-pupil {{ animation: rb-glint 3.6s infinite; }}
#     .rb-ant {{ animation: rb-pulse 1.8s ease-in-out infinite; }}
#     .rb-bot {{ {float_anim} }}
#     .rb-scan {{ animation: rb-scan 3.2s ease-in-out infinite; }}
#     .rb-wave {{ transform-origin: 188px 186px; animation: rb-wave 2.5s ease-in-out infinite; }}
#     .rb-shadow {{ transform-box: fill-box; transform-origin: center; animation: rb-shadow 3.5s ease-in-out infinite; }}
#     .rb-core {{ animation: rb-pulse 2s ease-in-out infinite; }}
#     @keyframes rb-blink {{ 0%,88%,100% {{ transform: scaleY(1); }} 92%,95% {{ transform: scaleY(0.06); }} }}
#     @keyframes rb-glint {{ 0%,88%,100% {{ opacity: 1; }} 92%,95% {{ opacity: 0; }} }}
#     @keyframes rb-pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}
#     @keyframes rb-float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
#     @keyframes rb-scan {{ 0%,100% {{ opacity: 0.12; }} 50% {{ opacity: 0.65; }} }}
#     @keyframes rb-wave {{ 0%,100% {{ transform: rotate(-6deg); }} 50% {{ transform: rotate(20deg); }} }}
#     @keyframes rb-shadow {{ 0%,100% {{ transform: scale(1); opacity: 0.42; }} 50% {{ transform: scale(0.86); opacity: 0.24; }} }}
#   </style>
#   <defs>
#     <linearGradient id="rbNightHead" x1="0" y1="0" x2="0" y2="1">
#       <stop offset="0" stop-color="#132952"/><stop offset="0.55" stop-color="#091630"/><stop offset="1" stop-color="#040b1a"/>
#     </linearGradient>
#     <linearGradient id="rbNightBody" x1="0" y1="0" x2="0" y2="1">
#       <stop offset="0" stop-color="#0f2347"/><stop offset="1" stop-color="#030917"/>
#     </linearGradient>
#     <radialGradient id="rbEyeGlow" cx="0.45" cy="0.38" r="0.62">
#       <stop offset="0" stop-color="#ffffff"/><stop offset="0.42" stop-color="#7dd3fc"/><stop offset="1" stop-color="#0284c7"/>
#     </radialGradient>
#   </defs>
#   <ellipse class="rb-shadow" cx="130" cy="280" rx="58" ry="9" fill="#000000"/>
#   <g class="rb-bot">
#     <line x1="130" y1="26" x2="130" y2="54" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
#     <circle class="rb-ant" cx="130" cy="19" r="10" fill="#7dd3fc"/>
#     <rect x="38" y="88" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
#     <rect x="207" y="88" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
#     <rect x="54" y="54" width="152" height="114" rx="40" fill="url(#rbNightHead)" stroke="#38bdf8" stroke-width="3.5"/>
#     <rect x="72" y="74" width="116" height="72" rx="26" fill="#020712" stroke="#1e3a8a" stroke-width="2"/>
#     <rect class="rb-scan" x="80" y="80" width="100" height="8" rx="4" fill="#38bdf8"/>
#     <g class="rb-eye">
#       <ellipse cx="105" cy="108" rx="15" ry="18" fill="url(#rbEyeGlow)"/>
#       <circle class="rb-pupil" cx="100" cy="102" r="4.5" fill="#ffffff"/>
#     </g>
#     <g class="rb-eye rb-eye2">
#       <ellipse cx="155" cy="108" rx="15" ry="18" fill="url(#rbEyeGlow)"/>
#       <circle class="rb-pupil" cx="150" cy="102" r="4.5" fill="#ffffff"/>
#     </g>
#     <path d="M111 132 Q130 144 149 132" fill="none" stroke="#7dd3fc" stroke-width="4.5" stroke-linecap="round"/>
#     <rect x="84" y="174" width="92" height="76" rx="24" fill="url(#rbNightBody)" stroke="#38bdf8" stroke-width="3"/>
#     <rect x="124" y="188" width="12" height="34" rx="3" fill="#ffffff"/>
#     <rect x="113" y="199" width="34" height="12" rx="3" fill="#ffffff"/>
#     <circle class="rb-core" cx="130" cy="234" r="5.5" fill="#38bdf8"/>
#     <rect x="60" y="182" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
#     <g class="rb-wave">
#       <rect x="181" y="178" width="15" height="52" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
#       <circle cx="188.5" cy="234" r="10.5" fill="#091630" stroke="#7dd3fc" stroke-width="3"/>
#     </g>
#   </g>
# </svg>
# """


# def robot_html(size: int = 160, flotte: bool = True) -> str:
#     anim = "animation: rb-float 3.5s ease-in-out infinite;" if flotte else ""
#     svg = ROBOT_SVG.format(size=size, float_anim=anim)
#     return " ".join(svg.split())


# def avatar_robot() -> str:
#     try:
#         chemin = Path(__file__).parent / "robot_night_avatar.svg"
#         chemin.write_text(robot_html(160, flotte=False), encoding="utf-8")
#         return str(chemin)
#     except Exception:
#         return "🤖"


# AVATAR_BOT = avatar_robot()


# # =====================================================
# # 6. DESIGN BLEU DE NUIT FONCÉ + VERT FONCÉ + BLANC
# # =====================================================
# st.markdown(
#     """
#     <style>
#     #MainMenu, footer { visibility: hidden; }

#     .stApp {
#         background:
#             radial-gradient(circle at 14% 10%, rgba(56,189,248,0.16) 0%, transparent 40%),
#             radial-gradient(circle at 88% 16%, rgba(6,95,70,0.28) 0%, transparent 38%),
#             linear-gradient(rgba(148,163,184,0.035) 1px, transparent 1px),
#             linear-gradient(90deg, rgba(148,163,184,0.035) 1px, transparent 1px),
#             linear-gradient(180deg, #020611 0%, #050f24 55%, #071936 100%);
#         background-size: auto, auto, 44px 44px, 44px 44px, auto;
#         background-attachment: fixed;
#     }

#     .main .block-container {
#         max-width: 1140px;
#         padding-top: 1.4rem;
#         padding-bottom: 6rem;
#     }

#     .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
#     .stApp span, .stApp li, .stApp div {
#         color: #ffffff;
#     }

#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #030917 0%, #052e22 100%);
#         border-right: 1px solid rgba(110,231,183,0.28);
#     }

#     /* ---------- Héros Bleu de Nuit Foncé & Vert Foncé ---------- */
#     .hero {
#         position: relative;
#         overflow: hidden;
#         display: flex;
#         align-items: center;
#         gap: 42px;
#         background: linear-gradient(135deg, rgba(3,11,28,0.95) 0%, rgba(6,54,40,0.88) 100%);
#         border: 1px solid rgba(125,211,252,0.38);
#         border-radius: 28px;
#         padding: 32px 42px;
#         margin-bottom: 22px;
#         box-shadow: 0 24px 64px rgba(0,0,0,0.68),
#                     0 0 44px rgba(14,165,233,0.16),
#                     inset 0 0 48px rgba(6,95,70,0.22);
#     }
#     .hero::before {
#         content: "";
#         position: absolute;
#         width: 440px;
#         height: 440px;
#         right: -130px;
#         top: -170px;
#         background: radial-gradient(circle, rgba(56,189,248,0.22), transparent 68%);
#         animation: glow 6s ease-in-out infinite;
#     }
#     @keyframes glow {
#         0%,100% { opacity: 0.45; transform: scale(1); }
#         50% { opacity: 0.95; transform: scale(1.12); }
#     }
#     .hero-robot {
#         position: relative;
#         flex: 0 0 auto;
#         line-height: 0;
#         background: radial-gradient(circle, rgba(2,132,199,0.20) 0%, rgba(3,10,24,0.85) 72%);
#         border: 1px solid rgba(125,211,252,0.30);
#         border-radius: 26px;
#         padding: 12px;
#         filter: drop-shadow(0 0 26px rgba(56,189,248,0.38));
#     }
#     .hero-text { position: relative; }
#     .hero-kicker {
#         display: inline-block;
#         font-size: 0.82rem;
#         font-weight: 700;
#         letter-spacing: 1.1px;
#         text-transform: uppercase;
#         color: #a7f3d0 !important;
#         background: rgba(5,56,40,0.85);
#         border: 1px solid rgba(110,231,183,0.40);
#         padding: 5px 14px;
#         border-radius: 999px;
#         margin-bottom: 12px;
#     }
#     .hero h1 {
#         margin: 0 0 8px 0;
#         font-size: 3.3rem;
#         font-weight: 800;
#         letter-spacing: 0.4px;
#         line-height: 1.06;
#         color: #ffffff !important;
#     }
#     .hero p {
#         margin: 0 0 16px 0;
#         color: #e2e8f0 !important;
#         font-size: 1.15rem;
#     }
#     .badges span {
#         display: inline-block;
#         margin: 0 8px 6px 0;
#         padding: 6px 16px;
#         border-radius: 999px;
#         font-size: 0.9rem;
#         font-weight: 600;
#         background: #053828;
#         border: 1px solid rgba(110,231,183,0.45);
#         color: #ffffff !important;
#     }
#     .status {
#         display: inline-block;
#         margin-top: 10px;
#         padding: 6px 16px;
#         border-radius: 999px;
#         font-size: 0.9rem;
#         font-weight: 600;
#         background: #020817;
#         border: 1px solid rgba(125,211,252,0.35);
#         color: #ffffff !important;
#     }
#     .dot {
#         display: inline-block;
#         width: 10px;
#         height: 10px;
#         border-radius: 50%;
#         margin-right: 8px;
#         animation: dotpulse 1.5s infinite;
#     }
#     .dot.on { background: #34d399; box-shadow: 0 0 12px #34d399; }
#     .dot.off { background: #f59e0b; box-shadow: 0 0 12px #f59e0b; }
#     @keyframes dotpulse {
#         0%,100% { opacity: 1; }
#         50% { opacity: 0.35; }
#     }

#     @media (max-width: 820px) {
#         .hero { flex-direction: column; text-align: center; padding: 26px 20px; gap: 18px; }
#         .hero h1 { font-size: 2.4rem; }
#     }

#     /* ---------- Bandeau Avertissement Vert Foncé ---------- */
#     .notice {
#         background: #042f22;
#         border: 1px solid rgba(110,231,183,0.40);
#         border-left: 5px solid #10b981;
#         color: #ffffff !important;
#         padding: 13px 18px;
#         border-radius: 12px;
#         margin: 14px 0 22px 0;
#         font-size: 0.95rem;
#     }

#     /* ---------- Boutons Vert Foncé / Bleu Nuit ---------- */
#     div.stButton > button, div.stDownloadButton > button {
#         border-radius: 14px;
#         min-height: 50px;
#         font-weight: 600;
#         color: #ffffff !important;
#         background: linear-gradient(135deg, #042f22 0%, #064e3b 100%);
#         border: 1px solid rgba(110,231,183,0.48);
#         box-shadow: 0 6px 18px rgba(0,0,0,0.42);
#         transition: all 0.2s ease;
#     }
#     div.stButton > button:hover, div.stDownloadButton > button:hover {
#         transform: translateY(-2px);
#         background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
#         box-shadow: 0 10px 26px rgba(16,185,129,0.28);
#         border-color: #ffffff;
#         color: #ffffff !important;
#     }
#     div.stDownloadButton > button:disabled { opacity: 0.42; }

#     /* ---------- Bulles de Conversation ---------- */
#     [data-testid="stChatMessage"] {
#         background: rgba(4, 15, 36, 0.90);
#         border: 1px solid rgba(125,211,252,0.26);
#         border-radius: 20px;
#         padding: 16px 20px;
#         margin-bottom: 14px;
#         box-shadow: 0 8px 24px rgba(0,0,0,0.35);
#     }
#     [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
#         background: rgba(5, 56, 40, 0.85);
#         border-color: rgba(110,231,183,0.48);
#     }
#     [data-testid="stChatMessage"] p,
#     [data-testid="stChatMessage"] li,
#     [data-testid="stChatMessage"] strong {
#         color: #ffffff !important;
#         font-size: 1.04rem;
#         line-height: 1.62;
#     }
#     [data-testid="stChatMessage"] img {
#         border-radius: 50%;
#         background: #030b1c;
#         border: 1px solid rgba(125,211,252,0.55);
#         padding: 2px;
#     }

#     /* ---------- Zone de Saisie : écriture noir foncé bien visible ---------- */
#     [data-testid="stChatInput"],
#     [data-testid="stChatInput"] > div,
#     [data-testid="stChatInput"] > div > div {
#         background: #f8fafc !important;
#         border-radius: 18px !important;
#         border: 2px solid #10b981 !important;
#         box-shadow: 0 0 28px rgba(6, 95, 70, 0.42) !important;
#     }
#     [data-testid="stChatInput"] textarea,
#     [data-testid="stChatInput"] textarea:focus,
#     [data-testid="stChatInput"] input {
#         color: #050811 !important;
#         -webkit-text-fill-color: #050811 !important;
#         caret-color: #050811 !important;
#         background: transparent !important;
#         font-weight: 600 !important;
#     }
#     [data-testid="stChatInput"] textarea::placeholder,
#     [data-testid="stChatInput"] input::placeholder {
#         color: #334155 !important;
#         -webkit-text-fill-color: #334155 !important;
#         opacity: 1 !important;
#     }
#     [data-testid="stChatInput"] button {
#         color: #050811 !important;
#         background: transparent !important;
#     }
#     [data-testid="stBottom"] > div {
#         background: transparent !important;
#     }

#     hr { border-color: rgba(148,163,184,0.22) !important; }
#     .stAlert { border-radius: 14px; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # =====================================================
# # 7. SESSION
# # =====================================================
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "suggestion_selectionnee" not in st.session_state:
#     st.session_state.suggestion_selectionnee = None
# if "langue_courante" not in st.session_state:
#     st.session_state.langue_courante = "Français"

# langue_affichee = st.session_state.langue_courante
# t = TEXTES[langue_affichee]

# if ERREUR_IMPORT is not None:
#     moteur_disponible = False
# else:
#     try:
#         moteur_disponible = bool(service_pret())
#     except Exception:
#         moteur_disponible = False

# etat_classe = "on" if moteur_disponible else "off"
# etat_texte = t["online"] if moteur_disponible else t["offline_short"]


# # =====================================================
# # 8. BARRE LATÉRALE (VUE DIRECTION / SUPERVISION)
# # =====================================================
# with st.sidebar:
#     st.markdown("### 🏥 Pôle Radiologie")
#     st.markdown(f"**{t['lang_badge']}**")
#     st.markdown(f"**Statut :** {etat_texte}")
#     st.markdown(f"**Messages échangés :** {len(st.session_state.messages)}")
#     st.divider()
#     st.caption(
#         "Détection automatique activée pour le Français, le Wolof et l'English. "
#         "Chaque question est transmise directement au moteur RAG dans la langue détectée."
#     )


# # =====================================================
# # 9. EN-TÊTE AVEC GRAND ROBOT BLEU DE NUIT FONCÉ
# # =====================================================
# st.markdown(
#     f"""<div class="hero">
#     <div class="hero-robot">{robot_html(270)}</div>
#     <div class="hero-text">
#         <div class="hero-kicker">SERVICE D'IMAGERIE MÉDICALE • ASSISTANT RAG</div>
#         <h1>RadiologyAi</h1>
#         <p>Assistant conversationnel multilingue du service de radiologie</p>
#         <div class="badges"><span>🇫🇷 Français</span><span>🇸🇳 Wolof</span><span>🇬🇧 English</span></div>
#         <div class="status"><span class="dot {etat_classe}"></span>{etat_texte}</div>
#     </div>
# </div>""",
#     unsafe_allow_html=True,
# )

# if ERREUR_IMPORT is not None:
#     st.error(
#         "Impossible de charger chatbot.py. "
#         "Vérifiez que ce fichier est présent dans le même dossier que l'application."
#     )
#     with st.expander("Détails techniques de l'import"):
#         st.code(str(ERREUR_IMPORT))


# # =====================================================
# # 10. ACCUEIL ET AVERTISSEMENT
# # =====================================================
# st.subheader(t["welcome"])
# st.write(t["intro"])
# st.markdown(f'<div class="notice">ℹ️ {t["disclaimer"]}</div>', unsafe_allow_html=True)


# # =====================================================
# # 11. QUESTIONS FRÉQUENTES
# # =====================================================
# st.subheader(t["suggestions"])
# colonnes = st.columns(2)
# for index, suggestion in enumerate(t["quick"]):
#     with colonnes[index % 2]:
#         if st.button(
#             suggestion,
#             key=f"suggestion_{langue_affichee}_{index}",
#             use_container_width=True,
#         ):
#             st.session_state.suggestion_selectionnee = suggestion


# # =====================================================
# # 12. ACTIONS (EFFACER / EXPORTER)
# # =====================================================
# col_effacer, col_telecharger = st.columns(2)

# with col_effacer:
#     if st.button(t["clear"], use_container_width=True):
#         st.session_state.messages = []
#         st.session_state.suggestion_selectionnee = None
#         st.rerun()

# with col_telecharger:
#     contenu = []
#     for message in st.session_state.messages:
#         role = "Patient" if message["role"] == "user" else "RadiologyAi"
#         contenu.append(f"[{role}]\n{message['content']}")
#     st.download_button(
#         label=t["download"],
#         data="\n\n".join(contenu) or "Aucun échange enregistré.",
#         file_name=f"radiologyai_conversation_{datetime.now():%Y%m%d_%H%M}.txt",
#         mime="text/plain",
#         use_container_width=True,
#         disabled=not bool(st.session_state.messages),
#     )


# # =====================================================
# # 13. HISTORIQUE DE CONVERSATION
# # =====================================================
# st.divider()
# st.subheader(t["chat"])

# if not st.session_state.messages:
#     with st.chat_message("assistant", avatar=AVATAR_BOT):
#         st.markdown(MESSAGE_ACCUEIL)

# for message in st.session_state.messages:
#     avatar = AVATAR_BOT if message["role"] == "assistant" else "🧑"
#     with st.chat_message(message["role"], avatar=avatar):
#         st.markdown(message["content"])


# # =====================================================
# # 14. SAISIE ET RÉPONSE DIRECTE DANS LA LANGUE DU PATIENT
# # =====================================================
# question_saisie = st.chat_input(PLACEHOLDER)
# question = question_saisie if question_saisie is not None else st.session_state.suggestion_selectionnee
# st.session_state.suggestion_selectionnee = None

# if question:
#     st.session_state.messages.append({"role": "user", "content": question})
#     with st.chat_message("user", avatar="🧑"):
#         st.markdown(question)

#     langue_demandee = commande_langue(question)

#     if langue_demandee:
#         st.session_state.langue_courante = langue_demandee
#         reponse = CONFIRMATIONS[langue_demandee]
#         with st.chat_message("assistant", avatar=AVATAR_BOT):
#             st.markdown(reponse)
#     else:
#         langue_detectee = detecter_langue(question, st.session_state.langue_courante)
#         st.session_state.langue_courante = langue_detectee
#         td = TEXTES[langue_detectee]
#         langue_rag = LANGUES[langue_detectee]

#         with st.chat_message("assistant", avatar=AVATAR_BOT):
#             if ask_ai_stream is None:
#                 reponse = td["offline"]
#                 st.error(reponse)
#             else:
#                 try:
#                     with st.spinner(td["thinking"]):
#                         resultat = st.write_stream(
#                             ask_ai_stream(question, langue=langue_rag)
#                         )
#                     if isinstance(resultat, str) and resultat.strip():
#                         reponse = resultat
#                     else:
#                         reponse = td["no_answer"]
#                         st.warning(reponse)
#                 except Exception as erreur:
#                     reponse = td["offline"]
#                     st.error(reponse)
#                     with st.expander("Détails techniques"):
#                         st.code(str(erreur))

#     st.session_state.messages.append({"role": "assistant", "content": reponse})
#     st.rerun()


# # =====================================================
# # 15. PIED DE PAGE
# # =====================================================
# st.divider()
# st.caption(
#     "RadiologyAi — Assistant d'orientation pour le service de radiologie. "
#     "Les informations affichées doivent être validées par l'équipe médicale et d'accueil."
# )
# Fin 
# Nouveau
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

# =====================================================
# 1. CONNEXION AU MOTEUR RAG (chatbot.py)
# =====================================================
try:
    from chatbot import ask_ai_stream, prechauffer, service_pret
    ERREUR_IMPORT = None
except Exception as erreur:
    ask_ai_stream = None
    prechauffer = None
    ERREUR_IMPORT = erreur

    def service_pret():
        return False


# =====================================================
# 2. CONFIGURATION DE LA PAGE
# =====================================================
st.set_page_config(
    page_title="RadiologyAi — Assistant Service de Radiologie",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================
# 3. LANGUES (Wolof normal, Français, English)
# =====================================================
LANGUES = {
    "Wolof": "wolof",
    "Français": "français",
    "English": "anglais",
}

# Mots et particules très fréquents en wolof parlé (avec ou sans accents)
MOTS_WOLOF_FORTS = {
    "wolof", "nanga", "def", "naka", "jàmm", "jamm", "jërëjëf", "jerejef",
    "jërejëf", "dama", "bëgg", "begg", "laaj", "laajal", "serwiis", "kayit",
    "yan", "ban", "waxtu", "lañuy", "lanuy", "fii", "ubbeeku", "ubbi", "tontu",
    "waaw", "deedeet", "déedéet", "ñu", "dëkk", "toog", "jàppale", "jappale",
    "yoon", "fekk", "nekk", "nekkul", "ndax", "léegi", "legi", "asalaamaalekum",
    "salaam", "maalekum", "lii", "loolu", "lan", "walla", "mbaa", "rekk",
    "mën", "men", "dafa", "amul", "xam", "xamul", "ngi", "maa", "kaay", "dem",
    "indi", "xibaar", "doktoor", "jëm", "fan", "foo", "lu", "dinaa", "dina",
    "ekografi", "lopitaal", "ana", "ngir", "sama", "suñu", "sunu", "am na",
    "nan", "nuyoo", "nuyo", "sant", "sante",
}

MOTS_WOLOF_FAIBLES = {
    "bi", "yi", "ci", "ak", "sa", "am", "la", "na", "di", "du", "bu", "su",
}

MOTS_FR = {
    "le", "la", "les", "des", "du", "de", "un", "une", "est", "sont", "je",
    "vous", "nous", "quel", "quels", "quelle", "quelles", "où", "ou", "et",
    "pour", "dans", "avec", "sur", "que", "qui", "quoi", "comment", "combien",
    "puis", "peut", "bonjour", "salut", "bonsoir", "merci", "horaires", "service",
    "examens", "examen", "documents", "apporter", "rendez-vous", "faut",
    "dois", "il", "elle", "au", "aux", "ce", "cette", "mon", "ma", "mes",
    "radiologie", "est-ce", "ai", "suis", "veux", "voudrais", "besoin",
    "échographie", "echographie", "scanner", "irm", "préparation", "preparation",
    "résultats", "resultats", "hôpital", "hopital", "faire", "tarif", "tarifs",
    "ouvert", "ouverture", "fermeture", "svp", "s'il", "plaît",
}

MOTS_EN = {
    "the", "is", "are", "what", "where", "how", "do", "does", "can", "i",
    "you", "my", "your", "which", "when", "who", "with", "for", "and", "of",
    "to", "hello", "hi", "thanks", "thank", "please", "hours", "appointment",
    "need", "want", "should", "bring", "open", "available", "department",
    "examinations", "exam", "exams", "it", "there", "this", "that", "me",
    "ultrasound", "ct", "mri", "xray", "x-ray", "results", "preparation",
    "cost", "price", "hospital", "radiology",
}

COMMANDES_LANGUE = {
    "wolof": "Wolof",
    "français": "Français",
    "francais": "Français",
    "french": "Français",
    "anglais": "English",
    "english": "English",
}

CONFIRMATIONS = {
    "Wolof": "Waaw, dinaa la tontu ci **wolof** ci saa si. Laajal sa laaj ci serwiisu radiologie.",
    "Français": "Parfait, je vous répondrai directement en **français**. Posez votre question sur le service de radiologie.",
    "English": "Understood, I will answer directly in **English**. Ask your question about the radiology department.",
}


def mots(texte: str) -> list[str]:
    return re.findall(r"[\w'’\-àâäçéèêëîïôöùûüÿñœ]+", texte.lower())


def commande_langue(texte: str) -> str | None:
    tokens = mots(texte)
    if 0 < len(tokens) <= 3:
        for tok in tokens:
            if tok in COMMANDES_LANGUE:
                return COMMANDES_LANGUE[tok]
    return None


def detecter_langue(texte: str, langue_precedente: str = "Français") -> str:
    """
    Détecte le Wolof normal (même avec mots français/anglais courants),
    le Français ou l'English.
    """
    texte_min = texte.lower().strip()
    tokens = mots(texte_min)

    if not tokens:
        return langue_precedente

    # Indices très clairs de wolof parlé
    if re.search(
        r"[ñëà]|jàmm|jërëjëf|asalaamaalekum|ubbeeku|laajal|serwiis|"
        r"\b(dama|bëgg|begg|nanga|naka|waxtu|kayit|ekografi|lopitaal|"
        r"waaw|deedeet|déedéet|mën|men|lañuy|lanuy|dinaa|ana)\b",
        texte_min,
    ):
        return "Wolof"

    sw = sum(2.5 for m in tokens if m in MOTS_WOLOF_FORTS) + sum(
        0.6 for m in tokens if m in MOTS_WOLOF_FAIBLES
    )
    sf = sum(1.0 for m in tokens if m in MOTS_FR)
    se = sum(1.0 for m in tokens if m in MOTS_EN)

    if re.search(r"[çèùêôéîï]", texte_min):
        sf += 1.5

    if re.search(r"\b(i'm|i am|can i|do you|what is|where is|how do)\b", texte_min):
        se += 2.0

    # Le wolof parlé intègre souvent des noms français (scanner, radio, rendez-vous...)
    if sw >= 1.5 and sw >= sf * 0.75 and sw >= se:
        return "Wolof"

    scores = {"Wolof": sw, "Français": sf, "English": se}
    meilleure = max(scores, key=scores.get)

    if scores[meilleure] > 0:
        return meilleure

    return langue_precedente


# =====================================================
# 4. TEXTES DE L'INTERFACE
# =====================================================
TEXTES = {
    "Français": {
        "welcome": "Bienvenue au service de radiologie — RadiologyAi",
        "intro": "Orientation rapide, préparation aux examens, horaires et documents à prévoir.",
        "chat": "Échange en direct avec RadiologyAi",
        "suggestions": "✨ Questions fréquentes des patients",
        "clear": "🗑️ Nouvelle discussion",
        "download": "⬇️ Exporter l'échange",
        "disclaimer": "Information d'orientation uniquement. RadiologyAi ne remplace pas un médecin radiologue et n'établit aucun diagnostic médical.",
        "thinking": "Consultation des documents du service de radiologie...",
        "offline": "Le moteur d'assistance est momentanément indisponible. Veuillez réessayer ou vous adresser à l'accueil de la radiologie.",
        "no_answer": "Aucune réponse n'a pu être générée. Merci de reformuler votre question.",
        "online": "Moteur RAG opérationnel",
        "offline_short": "Moteur RAG hors ligne",
        "lang_badge": "Langue détectée : Français",
        "quick": [
            "Quels sont les horaires d'ouverture de la radiologie ?",
            "Quels documents dois-je apporter pour mon examen ?",
            "Comment se préparer à une échographie ou un scanner ?",
            "Où se situe le service de radiologie ?",
        ],
    },
    "Wolof": {
        "welcome": "Dalal ak jàmm ci serwiisu radiologie — RadiologyAi",
        "intro": "Jàppale bu gaaw ci waxtuy ubbiku, waajtaayoo examen, kayit yi ak barab bi.",
        "chat": "Waxtaan ak RadiologyAi",
        "suggestions": "✨ Laaj yi ñu gëna faral di laaj",
        "clear": "🗑️ Waxtaan bu bees",
        "download": "⬇️ Yebbi waxtaan wi",
        "disclaimer": "Xibaar ngir gindi rekk. RadiologyAi du wuutu doktoor te du def diagnoos.",
        "thinking": "Maa ngi seet ci kayiti serwiisu radiologie bi...",
        "offline": "Serwiis bi amul léegi. Jéemaatal ci kanam tuuti walla nga dem ci accueil radiologie.",
        "no_answer": "Manul naa tontu. Jéemaatal di laaj ci beneen anam.",
        "online": "Moteur RAG dafa ubbiku",
        "offline_short": "Moteur RAG dafa tëju",
        "lang_badge": "Làkk wi : Wolof",
        "quick": [
            "Ban waxtu la serwiisu radiologie di ubbeeku ?",
            "Yan kayit laa war a indi ngir sama examen ?",
            "Naka laay waajtaayoo ngir ekografi walla scanner ?",
            "Ana la serwiisu radiologie nekk ?",
        ],
    },
    "English": {
        "welcome": "Welcome to Radiology — RadiologyAi",
        "intro": "Instant guidance on opening hours, exam preparation, required documents, and location.",
        "chat": "Live conversation with RadiologyAi",
        "suggestions": "✨ Frequent patient questions",
        "clear": "🗑️ New chat",
        "download": "⬇️ Export transcript",
        "disclaimer": "General guidance only. RadiologyAi does not replace a radiologist or healthcare professional and does not provide medical diagnoses.",
        "thinking": "Searching radiology department knowledge base...",
        "offline": "The assistant service is temporarily unavailable. Please try again later or contact the radiology front desk.",
        "no_answer": "I could not generate a response. Please rephrase your question.",
        "online": "RAG engine online",
        "offline_short": "RAG engine offline",
        "lang_badge": "Detected language: English",
        "quick": [
            "What are the radiology department opening hours?",
            "Which documents should I bring for my exam?",
            "How do I prepare for an ultrasound or CT scan?",
            "Where is the radiology department located?",
        ],
    },
}

PLACEHOLDER = "Bindal ci Wolof, écrivez en Français ou write in English...  ✍️"

MESSAGE_ACCUEIL = (
    "👋 **Asalaamaalekum !** Maa ngi tudd **RadiologyAi**. Bindal ci **wolof** ci saa si.\n\n"
    "👋 **Bonjour !** Je suis **RadiologyAi**. Écrivez directement en **français**.\n\n"
    "👋 **Hello!** I am **RadiologyAi**. Write directly in **English**."
)


# =====================================================
# 5. GRAND ROBOT BLEU DE NUIT FONCÉ (YEUX QUI CLIGNOTENT)
# =====================================================
ROBOT_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 295" width="{size}" height="{size}" role="img" aria-label="Grand robot bleu de nuit foncé RadiologyAi">
  <style>
    .rb-eye {{ transform-box: fill-box; transform-origin: center; animation: rb-blink 3.6s infinite; }}
    .rb-eye2 {{ animation-delay: 0.03s; }}
    .rb-pupil {{ animation: rb-glint 3.6s infinite; }}
    .rb-ant {{ animation: rb-pulse 1.8s ease-in-out infinite; }}
    .rb-bot {{ {float_anim} }}
    .rb-scan {{ animation: rb-scan 3.2s ease-in-out infinite; }}
    .rb-wave {{ transform-origin: 188px 186px; animation: rb-wave 2.5s ease-in-out infinite; }}
    .rb-shadow {{ transform-box: fill-box; transform-origin: center; animation: rb-shadow 3.5s ease-in-out infinite; }}
    .rb-core {{ animation: rb-pulse 2s ease-in-out infinite; }}
    @keyframes rb-blink {{ 0%,88%,100% {{ transform: scaleY(1); }} 92%,95% {{ transform: scaleY(0.06); }} }}
    @keyframes rb-glint {{ 0%,88%,100% {{ opacity: 1; }} 92%,95% {{ opacity: 0; }} }}
    @keyframes rb-pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.35; }} }}
    @keyframes rb-float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-7px); }} }}
    @keyframes rb-scan {{ 0%,100% {{ opacity: 0.12; }} 50% {{ opacity: 0.65; }} }}
    @keyframes rb-wave {{ 0%,100% {{ transform: rotate(-6deg); }} 50% {{ transform: rotate(20deg); }} }}
    @keyframes rb-shadow {{ 0%,100% {{ transform: scale(1); opacity: 0.42; }} 50% {{ transform: scale(0.86); opacity: 0.24; }} }}
  </style>
  <defs>
    <linearGradient id="rbNightHead" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#132952"/><stop offset="0.55" stop-color="#091630"/><stop offset="1" stop-color="#040b1a"/>
    </linearGradient>
    <linearGradient id="rbNightBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0f2347"/><stop offset="1" stop-color="#030917"/>
    </linearGradient>
    <radialGradient id="rbEyeGlow" cx="0.45" cy="0.38" r="0.62">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.42" stop-color="#7dd3fc"/><stop offset="1" stop-color="#0284c7"/>
    </radialGradient>
  </defs>
  <ellipse class="rb-shadow" cx="130" cy="280" rx="58" ry="9" fill="#000000"/>
  <g class="rb-bot">
    <line x1="130" y1="26" x2="130" y2="54" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
    <circle class="rb-ant" cx="130" cy="19" r="10" fill="#7dd3fc"/>
    <rect x="38" y="88" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
    <rect x="207" y="88" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
    <rect x="54" y="54" width="152" height="114" rx="40" fill="url(#rbNightHead)" stroke="#38bdf8" stroke-width="3.5"/>
    <rect x="72" y="74" width="116" height="72" rx="26" fill="#020712" stroke="#1e3a8a" stroke-width="2"/>
    <rect class="rb-scan" x="80" y="80" width="100" height="8" rx="4" fill="#38bdf8"/>
    <g class="rb-eye">
      <ellipse cx="105" cy="108" rx="15" ry="18" fill="url(#rbEyeGlow)"/>
      <circle class="rb-pupil" cx="100" cy="102" r="4.5" fill="#ffffff"/>
    </g>
    <g class="rb-eye rb-eye2">
      <ellipse cx="155" cy="108" rx="15" ry="18" fill="url(#rbEyeGlow)"/>
      <circle class="rb-pupil" cx="150" cy="102" r="4.5" fill="#ffffff"/>
    </g>
    <path d="M111 132 Q130 144 149 132" fill="none" stroke="#7dd3fc" stroke-width="4.5" stroke-linecap="round"/>
    <rect x="84" y="174" width="92" height="76" rx="24" fill="url(#rbNightBody)" stroke="#38bdf8" stroke-width="3"/>
    <rect x="124" y="188" width="12" height="34" rx="3" fill="#ffffff"/>
    <rect x="113" y="199" width="34" height="12" rx="3" fill="#ffffff"/>
    <circle class="rb-core" cx="130" cy="234" r="5.5" fill="#38bdf8"/>
    <rect x="60" y="182" width="15" height="50" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
    <g class="rb-wave">
      <rect x="181" y="178" width="15" height="52" rx="7.5" fill="#0c1e3e" stroke="#38bdf8" stroke-width="2"/>
      <circle cx="188.5" cy="234" r="10.5" fill="#091630" stroke="#7dd3fc" stroke-width="3"/>
    </g>
  </g>
</svg>
"""


def robot_html(size: int = 160, flotte: bool = True) -> str:
    anim = "animation: rb-float 3.5s ease-in-out infinite;" if flotte else ""
    svg = ROBOT_SVG.format(size=size, float_anim=anim)
    return " ".join(svg.split())


def avatar_robot() -> str:
    try:
        chemin = Path(__file__).parent / "robot_night_avatar.svg"
        chemin.write_text(robot_html(160, flotte=False), encoding="utf-8")
        return str(chemin)
    except Exception:
        return "🤖"


AVATAR_BOT = avatar_robot()


# =====================================================
# 6. DESIGN BLEU DE NUIT FONCÉ + VERT FONCÉ + BLANC
# =====================================================
st.markdown(
    """
    <style>
    #MainMenu, footer { visibility: hidden; }

    .stApp {
        background:
            radial-gradient(circle at 14% 10%, rgba(56,189,248,0.16) 0%, transparent 40%),
            radial-gradient(circle at 88% 16%, rgba(6,95,70,0.28) 0%, transparent 38%),
            linear-gradient(rgba(148,163,184,0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.035) 1px, transparent 1px),
            linear-gradient(180deg, #020611 0%, #050f24 55%, #071936 100%);
        background-size: auto, auto, 44px 44px, 44px 44px, auto;
        background-attachment: fixed;
    }

    .main .block-container {
        max-width: 1140px;
        padding-top: 1.4rem;
        padding-bottom: 6rem;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
    .stApp span, .stApp li, .stApp div {
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #030917 0%, #052e22 100%);
        border-right: 1px solid rgba(110,231,183,0.28);
    }

    /* ---------- Héros Bleu de Nuit Foncé & Vert Foncé ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        gap: 42px;
        background: linear-gradient(135deg, rgba(3,11,28,0.95) 0%, rgba(6,54,40,0.88) 100%);
        border: 1px solid rgba(125,211,252,0.38);
        border-radius: 28px;
        padding: 32px 42px;
        margin-bottom: 22px;
        box-shadow: 0 24px 64px rgba(0,0,0,0.68),
                    0 0 44px rgba(14,165,233,0.16),
                    inset 0 0 48px rgba(6,95,70,0.22);
    }
    .hero::before {
        content: "";
        position: absolute;
        width: 440px;
        height: 440px;
        right: -130px;
        top: -170px;
        background: radial-gradient(circle, rgba(56,189,248,0.22), transparent 68%);
        animation: glow 6s ease-in-out infinite;
    }
    @keyframes glow {
        0%,100% { opacity: 0.45; transform: scale(1); }
        50% { opacity: 0.95; transform: scale(1.12); }
    }
    .hero-robot {
        position: relative;
        flex: 0 0 auto;
        line-height: 0;
        background: radial-gradient(circle, rgba(2,132,199,0.20) 0%, rgba(3,10,24,0.85) 72%);
        border: 1px solid rgba(125,211,252,0.30);
        border-radius: 26px;
        padding: 12px;
        filter: drop-shadow(0 0 26px rgba(56,189,248,0.38));
    }
    .hero-text { position: relative; }
    .hero-kicker {
        display: inline-block;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        color: #a7f3d0 !important;
        background: rgba(5,56,40,0.85);
        border: 1px solid rgba(110,231,183,0.40);
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 12px;
    }
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 3.3rem;
        font-weight: 800;
        letter-spacing: 0.4px;
        line-height: 1.06;
        color: #ffffff !important;
    }
    .hero p {
        margin: 0 0 16px 0;
        color: #e2e8f0 !important;
        font-size: 1.15rem;
    }
    .badges span {
        display: inline-block;
        margin: 0 8px 6px 0;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        background: #053828;
        border: 1px solid rgba(110,231,183,0.45);
        color: #ffffff !important;
    }
    .status {
        display: inline-block;
        margin-top: 10px;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        background: #020817;
        border: 1px solid rgba(125,211,252,0.35);
        color: #ffffff !important;
    }
    .dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: dotpulse 1.5s infinite;
    }
    .dot.on { background: #34d399; box-shadow: 0 0 12px #34d399; }
    .dot.off { background: #f59e0b; box-shadow: 0 0 12px #f59e0b; }
    @keyframes dotpulse {
        0%,100% { opacity: 1; }
        50% { opacity: 0.35; }
    }

    @media (max-width: 820px) {
        .hero { flex-direction: column; text-align: center; padding: 26px 20px; gap: 18px; }
        .hero h1 { font-size: 2.4rem; }
    }

    /* ---------- Bandeau Avertissement Vert Foncé ---------- */
    .notice {
        background: #042f22;
        border: 1px solid rgba(110,231,183,0.40);
        border-left: 5px solid #10b981;
        color: #ffffff !important;
        padding: 13px 18px;
        border-radius: 12px;
        margin: 14px 0 22px 0;
        font-size: 0.95rem;
    }

    /* ---------- Boutons Vert Foncé / Bleu Nuit ---------- */
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 14px;
        min-height: 50px;
        font-weight: 600;
        color: #ffffff !important;
        background: linear-gradient(135deg, #042f22 0%, #064e3b 100%);
        border: 1px solid rgba(110,231,183,0.48);
        box-shadow: 0 6px 18px rgba(0,0,0,0.42);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        box-shadow: 0 10px 26px rgba(16,185,129,0.28);
        border-color: #ffffff;
        color: #ffffff !important;
    }
    div.stDownloadButton > button:disabled { opacity: 0.42; }

    /* ---------- Bulles de Conversation ---------- */
    [data-testid="stChatMessage"] {
        background: rgba(4, 15, 36, 0.90);
        border: 1px solid rgba(125,211,252,0.26);
        border-radius: 20px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: rgba(5, 56, 40, 0.85);
        border-color: rgba(110,231,183,0.48);
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong {
        color: #ffffff !important;
        font-size: 1.04rem;
        line-height: 1.62;
    }
    [data-testid="stChatMessage"] img {
        border-radius: 50%;
        background: #030b1c;
        border: 1px solid rgba(125,211,252,0.55);
        padding: 2px;
    }

    /* ---------- Zone de Saisie : écriture noir foncé bien visible ---------- */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div {
        background: #f8fafc !important;
        border-radius: 18px !important;
        border: 2px solid #10b981 !important;
        box-shadow: 0 0 28px rgba(6, 95, 70, 0.42) !important;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] input {
        color: #050811 !important;
        -webkit-text-fill-color: #050811 !important;
        caret-color: #050811 !important;
        background: transparent !important;
        font-weight: 600 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {
        color: #334155 !important;
        -webkit-text-fill-color: #334155 !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] button {
        color: #050811 !important;
        background: transparent !important;
    }
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }

    hr { border-color: rgba(148,163,184,0.22) !important; }
    .stAlert { border-radius: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# 7. SESSION & PRÉCHAUFFAGE
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggestion_selectionnee" not in st.session_state:
    st.session_state.suggestion_selectionnee = None
if "langue_courante" not in st.session_state:
    st.session_state.langue_courante = "Français"
if "mode_langue" not in st.session_state:
    st.session_state.mode_langue = "Auto"

if ERREUR_IMPORT is None:
    try:
        moteur_disponible = bool(service_pret())
        if moteur_disponible and callable(prechauffer):
            prechauffer()
    except Exception:
        moteur_disponible = False
else:
    moteur_disponible = False

langue_affichee = st.session_state.langue_courante
t = TEXTES[langue_affichee]
etat_classe = "on" if moteur_disponible else "off"
etat_texte = t["online"] if moteur_disponible else t["offline_short"]


# =====================================================
# 8. BARRE LATÉRALE
# =====================================================
with st.sidebar:
    st.markdown("### 🏥 Pôle Radiologie")
    choix_langue = st.selectbox(
        "Langue de réponse",
        options=["Auto", "Wolof", "Français", "English"],
        index=["Auto", "Wolof", "Français", "English"].index(st.session_state.mode_langue),
    )
    st.session_state.mode_langue = choix_langue
    if choix_langue != "Auto":
        st.session_state.langue_courante = choix_langue
        langue_affichee = choix_langue
        t = TEXTES[langue_affichee]

    st.markdown(f"**{t['lang_badge']}**")
    st.markdown(f"**Statut :** {etat_texte}")
    st.markdown(f"**Messages échangés :** {len(st.session_state.messages)}")


# =====================================================
# 9. EN-TÊTE AVEC GRAND ROBOT BLEU DE NUIT FONCÉ
# =====================================================
st.markdown(
    f"""<div class="hero">
    <div class="hero-robot">{robot_html(270)}</div>
    <div class="hero-text">
        <div class="hero-kicker">SERVICE DE RADIOLOGIE • HÔPITAL RÉGIONAL DE THIÈS</div>
        <h1>RadiologyAi</h1>
        <p>Assistant conversationnel multilingue du service de radiologie</p>
        <div class="badges"><span>🇸🇳 Wolof</span><span>🇫🇷 Français</span><span>🇬🇧 English</span></div>
        <div class="status"><span class="dot {etat_classe}"></span>{etat_texte}</div>
    </div>
</div>""",
    unsafe_allow_html=True,
)

if ERREUR_IMPORT is not None:
    st.error(
        "Impossible de charger chatbot.py. "
        "Vérifiez que ce fichier est présent dans le même dossier que l'application."
    )
    with st.expander("Détails techniques de l'import"):
        st.code(str(ERREUR_IMPORT))


# =====================================================
# 10. ACCUEIL ET AVERTISSEMENT
# =====================================================
st.subheader(t["welcome"])
st.write(t["intro"])
st.markdown(f'<div class="notice">ℹ️ {t["disclaimer"]}</div>', unsafe_allow_html=True)


# =====================================================
# 11. QUESTIONS FRÉQUENTES
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
# 12. ACTIONS (EFFACER / EXPORTER)
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
        role = "Patient" if message["role"] == "user" else "RadiologyAi"
        contenu.append(f"[{role}]\n{message['content']}")
    st.download_button(
        label=t["download"],
        data="\n\n".join(contenu) or "Aucun échange enregistré.",
        file_name=f"radiologyai_conversation_{datetime.now():%Y%m%d_%H%M}.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(st.session_state.messages),
    )


# =====================================================
# 13. HISTORIQUE DE CONVERSATION
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
# 14. SAISIE ET RÉPONSE DIRECTE DANS LA LANGUE DU PATIENT
# =====================================================
question_saisie = st.chat_input(PLACEHOLDER)
question = question_saisie if question_saisie is not None else st.session_state.suggestion_selectionnee
st.session_state.suggestion_selectionnee = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    langue_demandee = commande_langue(question)

    if langue_demandee:
        st.session_state.langue_courante = langue_demandee
        st.session_state.mode_langue = langue_demandee
        reponse = CONFIRMATIONS[langue_demandee]
        with st.chat_message("assistant", avatar=AVATAR_BOT):
            st.markdown(reponse)
    else:
        if st.session_state.mode_langue == "Auto":
            langue_detectee = detecter_langue(question, st.session_state.langue_courante)
        else:
            langue_detectee = st.session_state.mode_langue

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
    st.rerun()


# =====================================================
# 15. PIED DE PAGE
# =====================================================
st.divider()
st.caption(
    "RadiologyAi — Assistant d'orientation pour le service de radiologie de l'hôpital régional de Thiès. "
    "Les informations affichées doivent être validées par l'équipe médicale et d'accueil."
)
