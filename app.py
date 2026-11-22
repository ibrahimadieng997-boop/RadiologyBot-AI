# import base64
# import itertools
# import html as html_lib
# import re
# import time
# import urllib.request
# from pathlib import Path

# import streamlit as st

# # Import sécurisé : si la base ou Ollama pose problème, l'application s'affiche quand même
# try:
#     from chatbot import ask_ai_stream, prechauffer, service_pret
#     erreur_import = None
# except Exception as erreur:
#     ask_ai_stream = None
#     erreur_import = erreur

#     def service_pret():
#         return False

#     def prechauffer():
#         pass


# def afficher_html(contenu, **options):
#     """Affiche du HTML sans lignes vides ni indentation
#     (sinon Markdown le prend pour un bloc de code)."""
#     lignes = [l.strip() for l in contenu.splitlines() if l.strip()]
#     st.markdown(" ".join(lignes), unsafe_allow_html=True)


# def ollama_actif() -> bool:
#     """Vérifie que le serveur Ollama répond."""
#     try:
#         with urllib.request.urlopen("http://localhost:11434", timeout=2) as r:
#             return r.status == 200
#     except Exception:
#         return False


# # =====================================================
# # 1. CONFIGURATION
# # =====================================================

# st.set_page_config(
#     page_title="RadiologyBot AI",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# ROBOT = Path("assets/radiologybot_avatar.png")
# robot_disponible = ROBOT.exists()
# en_ligne = ask_ai_stream is not None and service_pret()

# # True  : robot animé (yeux qui clignotent), dessiné dans le code
# # False : votre image assets/radiologybot_avatar.png
# ROBOT_ANIME = True

# # Robot animé en SVG : les yeux clignotent, l'antenne pulse, le robot flotte
# ROBOT_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
# <style>
# .float{animation:float 3s ease-in-out infinite}
# .eye{transform-box:fill-box;transform-origin:center;animation:blink 4.5s infinite}
# .antenna{animation:pulse 2s ease-in-out infinite}
# @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
# @keyframes blink{0%,38%,42%,84%,88%,100%{transform:scaleY(1)}40%,86%{transform:scaleY(0.06)}}
# @keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
# </style>
# <defs>
# <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
# <stop offset="0" stop-color="#1d4f82"/>
# <stop offset="1" stop-color="#0b2540"/>
# </linearGradient>
# </defs>
# <g class="float">
# <line x1="150" y1="40" x2="150" y2="68" stroke="#35d9ff" stroke-width="5" stroke-linecap="round"/>
# <circle class="antenna" cx="150" cy="30" r="11" fill="#35d9ff"/>
# <rect x="36" y="118" width="24" height="56" rx="11" fill="#142f54" stroke="#35d9ff" stroke-width="3"/>
# <rect x="240" y="118" width="24" height="56" rx="11" fill="#142f54" stroke="#35d9ff" stroke-width="3"/>
# <rect x="55" y="66" width="190" height="150" rx="42" fill="url(#g)" stroke="#35d9ff" stroke-width="4"/>
# <rect x="78" y="92" width="144" height="84" rx="26" fill="#061426" stroke="#28618a" stroke-width="2"/>
# <g class="eye">
# <ellipse cx="118" cy="132" rx="18" ry="21" fill="#35d9ff"/>
# <circle cx="112" cy="124" r="5" fill="#ffffff" opacity="0.85"/>
# </g>
# <g class="eye">
# <ellipse cx="182" cy="132" rx="18" ry="21" fill="#35d9ff"/>
# <circle cx="176" cy="124" r="5" fill="#ffffff" opacity="0.85"/>
# </g>
# <path d="M128 192 Q150 207 172 192" stroke="#35d9ff" stroke-width="5" fill="none" stroke-linecap="round"/>
# <rect x="136" y="214" width="28" height="16" fill="#142f54"/>
# <rect x="85" y="228" width="130" height="62" rx="26" fill="url(#g)" stroke="#35d9ff" stroke-width="4"/>
# <rect x="142" y="240" width="16" height="40" rx="4" fill="#25e0a0"/>
# <rect x="130" y="252" width="40" height="16" rx="4" fill="#25e0a0"/>
# </g>
# </svg>"""

# ROBOT_SVG_B64 = base64.b64encode(ROBOT_SVG.encode("utf-8")).decode("ascii")


# # =====================================================
# # 2. DESIGN DE L'APPLICATION
# # =====================================================

# st.markdown("""
# <style>

# .stApp {
#     background:
#         radial-gradient(circle at 10% 5%, #173d66 0%, transparent 35%),
#         linear-gradient(135deg, #061426, #0b203b, #102e50);
#     color: white;
# }

# footer, #MainMenu, [data-testid="stToolbar"] {
#     visibility: hidden;
# }

# header {
#     background: transparent;
# }

# .block-container {
#     max-width: 1100px;
#     padding-top: 25px;
#     padding-bottom: 60px;
# }

# /* TITRE */

# .brand {
#     text-align: center;
#     font-size: 40px;
#     font-weight: 850;
#     color: white;
#     letter-spacing: 1px;
# }

# .brand span {
#     color: #35d9ff;
# }

# .subtitle {
#     text-align: center;
#     color: #b4cce5;
#     font-size: 16px;
#     margin-bottom: 25px;
# }

# /* CARTE D'ACCUEIL */

# .hero {
#     background: linear-gradient(135deg, #102b50, #071a32);
#     border: 1px solid #28618a;
#     border-radius: 24px;
#     padding: 25px;
#     margin-bottom: 18px;
# }

# .online {
#     color: #25e0a0;
#     font-weight: bold;
# }

# .hero h1 {
#     font-size: 31px;
#     color: white;
# }

# .hero p {
#     color: #c5d9ef;
#     font-size: 18px;
# }

# /* CARTES */

# .service-card {
#     background: #142f54;
#     border: 1px solid rgba(53,217,255,.2);
#     border-radius: 17px;
#     padding: 18px;
#     min-height: 120px;
# }

# .service-card h3 {
#     color: white;
#     font-size: 18px;
# }

# .service-card p {
#     color: #c2d7ed;
#     font-size: 14px;
# }

# /* ROBOT */

# .robot-box {
#     background: linear-gradient(135deg, #102b50, #0a1c35);
#     border: 1px solid #35d9ff;
#     border-radius: 24px;
#     padding: 20px;
#     margin-top: 20px;
#     margin-bottom: 20px;
# }

# .robot-heading {
#     text-align: center;
#     color: #35d9ff;
#     font-size: 18px;
#     font-weight: bold;
#     margin-bottom: 15px;
# }

# .robot-title {
#     color: white;
#     font-size: 27px;
#     font-weight: 800;
# }

# .robot-description {
#     color: #d5e8fa;
#     font-size: 17px;
#     line-height: 1.6;
# }

# .robot-status {
#     display: inline-block;
#     background: #103f3b;
#     color: #27e5a2;
#     padding: 9px 15px;
#     border-radius: 25px;
#     font-weight: bold;
# }

# /* BOUTONS */

# .stButton > button {
#     background: #142f54;
#     color: white;
#     border: 1px solid #28618a;
#     border-radius: 13px;
#     min-height: 48px;
#     font-weight: 600;
# }

# .stButton > button:hover {
#     background: #15527b;
#     color: white;
#     border: 1px solid #35d9ff;
# }

# /* TEXTE DES RÉPONSES : blanc clair, bien visible */

# [data-testid="stChatMessage"],
# [data-testid="stChatMessage"] p,
# [data-testid="stChatMessage"] li,
# [data-testid="stChatMessage"] span,
# [data-testid="stChatMessage"] div,
# [data-testid="stChatMessage"] strong,
# [data-testid="stChatMessage"] em,
# [data-testid="stChatMessage"] h1,
# [data-testid="stChatMessage"] h2,
# [data-testid="stChatMessage"] h3,
# [data-testid="stChatMessage"] h4 {
#     color: #f4f8fc !important;
#     opacity: 1 !important;
# }

# [data-testid="stChatMessage"] li::marker {
#     color: #35d9ff;
# }

# /* ============ BARRE DE SAISIE PREMIUM ============ */

# /* Zone du bas : fond sombre dégradé (supprime la bande blanche) */
# [data-testid="stBottom"],
# [data-testid="stBottom"] > div,
# [data-testid="stBottomBlockContainer"] {
#     background: linear-gradient(180deg, rgba(6,20,38,0) 0%, #061426 38%) !important;
#     box-shadow: none !important;
# }

# [data-testid="stBottomBlockContainer"] {
#     max-width: 1100px;
#     padding-top: 22px;
#     padding-bottom: 26px;
# }

# .saisie-note {
#     text-align: center;
#     margin: 4px 0 22px 0;
#     font-size: 13px;
#     letter-spacing: .3px;
#     color: #8fb0d0;
# }

# .suggest-title {
#     color: #b4cce5;
#     font-size: 15px;
#     font-weight: 600;
#     margin: 6px 0 10px 2px;
# }

# /* Capsule de saisie */
# [data-testid="stChatInput"] {
#     margin-top: 8px;
# }
# [data-testid="stChatInput"] {
#     border: none !important;
#     background: transparent !important;
#     border-radius: 32px;
# }

# [data-testid="stChatInput"] > div {
#     background: linear-gradient(180deg, #ffffff, #eef5fb) !important;
#     border: 2px solid rgba(53,217,255,.65) !important;
#     border-radius: 32px !important;
#     min-height: 62px;
#     padding: 4px 10px 4px 18px;
#     box-shadow:
#         0 0 0 4px rgba(53,217,255,.10),
#         0 10px 35px rgba(0,0,0,.45),
#         0 0 28px rgba(53,217,255,.22);
#     transition: all .25s ease;
# }

# [data-testid="stChatInput"] > div:focus-within {
#     border-color: #25e0a0 !important;
#     box-shadow:
#         0 0 0 5px rgba(37,224,160,.18),
#         0 12px 40px rgba(0,0,0,.5),
#         0 0 36px rgba(37,224,160,.35);
# }

# /* Texte saisi : noir foncé bien visible */
# [data-testid="stChatInput"] textarea,
# [data-testid="stChatInput"] input {
#     color: #0a0a0a !important;
#     -webkit-text-fill-color: #0a0a0a !important;
#     caret-color: #0a6ea8 !important;
#     font-size: 17px !important;
#     font-weight: 500;
#     background: transparent !important;
# }

# [data-testid="stChatInput"] textarea::placeholder,
# [data-testid="stChatInput"] input::placeholder {
#     color: #243447 !important;
#     -webkit-text-fill-color: #243447 !important;
#     opacity: .85 !important;
#     font-weight: 400;
# }

# /* Bouton d'envoi : pastille dégradée */
# [data-testid="stChatInputSubmitButton"],
# [data-testid="stChatInput"] button {
#     background: linear-gradient(135deg, #35d9ff, #25e0a0) !important;
#     border: none !important;
#     border-radius: 50% !important;
#     width: 44px;
#     height: 44px;
#     box-shadow: 0 4px 14px rgba(53,217,255,.5);
#     transition: transform .2s ease, box-shadow .2s ease;
# }

# [data-testid="stChatInputSubmitButton"]:hover,
# [data-testid="stChatInput"] button:hover {
#     transform: scale(1.1) rotate(-6deg);
#     box-shadow: 0 6px 20px rgba(37,224,160,.65);
# }

# [data-testid="stChatInputSubmitButton"] svg,
# [data-testid="stChatInput"] button svg {
#     color: #06233a !important;
#     fill: #06233a !important;
# }

# /* ============ FENÊTRE DE CONVERSATION ============ */

# .chat-header {
#     background: linear-gradient(135deg, #12335c, #0a1f3a);
#     border: 1px solid rgba(53,217,255,.35);
#     border-radius: 18px;
#     padding: 14px 22px;
#     margin: 30px 0 16px 0;
#     color: #ffffff;
#     font-size: 18px;
#     font-weight: 700;
#     box-shadow: 0 6px 20px rgba(0,0,0,.25);
# }

# .chat-status {
#     color: #25e0a0;
#     font-size: 14px;
#     font-weight: 600;
#     margin-left: 14px;
# }

# .chat-empty {
#     text-align: center;
#     padding: 34px 20px;
#     border: 1px dashed rgba(53,217,255,.4);
#     border-radius: 18px;
#     color: #a9c4df;
#     font-size: 16px;
#     margin-bottom: 16px;
# }

# /* Fenêtre de discussion */
# .st-key-fenetre_chat {
#     background: linear-gradient(180deg, #0a1b30, #07121f);
#     border: 1px solid rgba(53,217,255,.25);
#     border-radius: 22px;
#     padding: 20px 22px 8px 22px;
#     margin-bottom: 26px;
#     box-shadow: inset 0 0 40px rgba(0,0,0,.35), 0 10px 30px rgba(0,0,0,.35);
# }

# /* Avatars masqués : on garde des bulles propres comme sur WhatsApp */
# [data-testid="stChatMessageAvatarUser"],
# [data-testid="stChatMessageAvatarAssistant"],
# [data-testid^="chatAvatarIcon"] {
#     display: none !important;
# }

# /* Bulle du robot : à gauche */
# [data-testid="stChatMessage"] {
#     background: linear-gradient(135deg, #1b3f6b, #13304f) !important;
#     border: 1px solid rgba(53,217,255,.25);
#     border-radius: 20px 20px 20px 5px;
#     padding: 12px 20px 8px 20px;
#     margin: 0 auto 16px 0;
#     width: 82%;
#     max-width: 82%;
#     box-shadow: 0 4px 14px rgba(0,0,0,.30);
# }

# /* Bulle du patient : à droite, verte */
# [data-testid="stChatMessage"]:has(.msg-user) {
#     background: linear-gradient(135deg, #0f7a6a, #0b5d52) !important;
#     border: 1px solid rgba(255,255,255,.15);
#     border-radius: 20px 20px 5px 20px;
#     margin: 0 0 16px auto;
#     width: fit-content;
#     min-width: 180px;
#     max-width: 75%;
# }

# [data-testid="stChatMessage"] p {
#     font-size: 16.5px;
#     line-height: 1.7;
# }

# [data-testid="stChatMessage"] .msg-nom {
#     color: #35d9ff !important;
#     font-size: 13px;
#     font-weight: 700;
#     margin-bottom: 4px;
# }

# [data-testid="stChatMessage"] .msg-heure {
#     display: block;
#     text-align: right;
#     font-size: 11.5px;
#     margin-top: 4px;
#     color: #9fc3e6 !important;
# }

# [data-testid="stChatMessage"]:has(.msg-user) .msg-heure {
#     color: #bff3e8 !important;
# }

# [data-testid="stChatMessage"] h1,
# [data-testid="stChatMessage"] h2,
# [data-testid="stChatMessage"] h3 {
#     color: #35d9ff !important;
# }

# [data-testid="stSpinner"] * {
#     color: #b4cce5 !important;
# }

# /* PIED DE PAGE */

# .footer {
#     text-align: center;
#     color: #a9c4df;
#     font-size: 13px;
#     padding: 25px;
# }

# </style>
# """, unsafe_allow_html=True)


# # =====================================================
# # 3. EN-TÊTE
# # =====================================================

# afficher_html("""
# <div class="brand">
#     🤖 RADIOLOGY<span>BOT AI</span>
# </div>

# <div class="subtitle">
#     Assistant intelligent du service de radiologie
#     <br>
#     Votre santé, notre priorité.
# </div>
# """, unsafe_allow_html=True)


# # =====================================================
# # 4. CARTE PRINCIPALE
# # =====================================================

# statut = "● En ligne" if en_ligne else "● Hors ligne"

# afficher_html(f"""
# <div class="hero">

#     <div class="online">{statut}</div>

#     <h1>Votre santé, notre priorité.</h1>

#     <p>
#         Comment puis-je vous accompagner aujourd'hui ?
#     </p>

# </div>
# """, unsafe_allow_html=True)


# # =====================================================
# # 5. INFORMATIONS DU SERVICE
# # =====================================================

# col1, col2 = st.columns(2)

# with col1:
#     afficher_html("""
#     <div class="service-card">
#         <h3>🏥 Informations médicales</h3>
#         <p>
#             Accédez aux informations pratiques
#             du service de radiologie.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     afficher_html("""
#     <div class="service-card">
#         <h3>🧭 Orientation patient</h3>
#         <p>
#             Découvrez les examens disponibles,
#             les horaires et la localisation.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)


# # =====================================================
# # 6. PRÉSENTATION DU ROBOT
# # =====================================================

# afficher_html("""
# <div class="robot-box">
#     <div class="robot-heading">
#         🤖 VOTRE ASSISTANT MÉDICAL
#     </div>
# </div>
# """, unsafe_allow_html=True)

# robot_col, text_col = st.columns(
#     [1.2, 2],
#     vertical_alignment="center"
# )

# with robot_col:

#     if ROBOT_ANIME:
#         st.markdown(
#             f'<img src="data:image/svg+xml;base64,{ROBOT_SVG_B64}" '
#             'alt="RadiologyBot AI" '
#             'style="width:100%;max-width:320px;display:block;margin:auto;">',
#             unsafe_allow_html=True
#         )
#     elif robot_disponible:
#         st.image(
#             str(ROBOT),
#             width="stretch"
#         )
#     else:
#         st.warning(
#             "Image introuvable : vérifiez le dossier assets."
#         )

# with text_col:

#     statut_robot = (
#         "● Assistant disponible" if en_ligne
#         else "● Assistant indisponible"
#     )

#     afficher_html(f"""
#     <div>

#         <div class="robot-title">
#             Bonjour ! Je suis RadiologyBot AI.
#         </div>

#         <p class="robot-description">
#             Votre assistant intelligent est disponible
#             pour vous accompagner et répondre à vos
#             questions sur le service de radiologie.
#         </p>

#         <div class="robot-status">
#             {statut_robot}
#         </div>

#     </div>
#     """, unsafe_allow_html=True)


# # =====================================================
# # 7. INITIALISATION DE LA CONVERSATION
# # =====================================================

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "pending_question" not in st.session_state:
#     st.session_state.pending_question = None


# def definir_question(question):
#     """Appelée au clic sur un bouton : mémorise la question à traiter."""
#     st.session_state.pending_question = question


# st.divider()

# st.markdown("## 💬 Discutez avec votre assistant")

# st.caption(
#     "Posez votre question directement au robot."
# )


# # =====================================================
# # 8. ZONE DE SAISIE (juste sous le robot)
# # =====================================================

# with st.container():
#     question_saisie = st.chat_input(
#         "Écrivez votre question à RadiologyBot AI..."
#     )

# afficher_html("""
# <div class="saisie-note">
#     🔒 Informations générales du service — ne remplace pas un avis médical
# </div>
# """)

# if question_saisie:
#     st.session_state.pending_question = question_saisie


# # =====================================================
# # 10. CONVERSATION STYLE WHATSAPP (réponse sous la question)
# # =====================================================

# def ecrire_progressivement(texte):
#     """Effet machine à écrire pour la réponse du robot."""
#     for morceau in re.split(r"(\s+)", texte):
#         yield morceau
#         time.sleep(0.012)


# def heure_actuelle():
#     return time.strftime("%H:%M")


# def afficher_message(role, contenu, heure=""):
#     """Affiche un message : patient à droite, robot à gauche."""
#     if role == "user":
#         with st.chat_message("user", avatar="👤"):
#             texte = html_lib.escape(contenu).replace("\n", "  \n")
#             st.markdown(
#                 '<span class="msg-user"></span>' + texte
#                 + f'<span class="msg-heure">{heure} ✓✓</span>',
#                 unsafe_allow_html=True
#             )
#     else:
#         avatar = str(ROBOT) if robot_disponible else "🤖"
#         with st.chat_message("assistant", avatar=avatar):
#             afficher_html('<div class="msg-nom">🤖 RadiologyBot AI</div>')
#             st.markdown(contenu)
#             afficher_html(f'<div class="msg-heure">{heure}</div>')


# def defiler_vers_le_dernier_message():
#     """Fait défiler la page jusqu'à la dernière réponse."""
#     script = """<script>
#     const d = window.parent.document;
#     const m = d.querySelectorAll('[data-testid="stChatMessage"]');
#     if (m.length) {
#         m[m.length - 1].scrollIntoView({behavior: 'smooth', block: 'center'});
#     }
#     </script>"""
#     try:
#         st.iframe(script, height=1)            # Streamlit récent
#     except Exception:
#         try:
#             import streamlit.components.v1 as components
#             components.html(script, height=0)  # anciennes versions
#         except Exception:
#             pass


# entete_col, bouton_col = st.columns([4, 1], vertical_alignment="center")

# with entete_col:
#     statut_chat = "● En ligne" if en_ligne else "● Hors ligne"
#     afficher_html(f"""
#     <div class="chat-header">
#         💬 Conversation avec RadiologyBot AI
#         <span class="chat-status">{statut_chat}</span>
#     </div>
#     """)

# with bouton_col:
#     if st.button("🗑️ Effacer", key="effacer_conversation", width="stretch"):
#         st.session_state.messages = []
#         st.session_state.pending_question = None
#         st.rerun()

# question_en_cours = st.session_state.pending_question
# st.session_state.pending_question = None

# nouvelle_reponse = None

# with st.container(key="fenetre_chat"):

#     if not st.session_state.messages and not question_en_cours:
#         afficher_html("""
#         <div class="chat-empty">
#             👋 Aucune question pour le moment.<br>
#             Écrivez votre question ci-dessus ou choisissez une question
#             fréquente plus bas : la réponse s'affichera ici, sous votre question.
#         </div>
#         """)

#     # Historique : question, puis réponse en dessous
#     for message in st.session_state.messages:
#         afficher_message(
#             message["role"],
#             message["content"],
#             message.get("heure", "")
#         )

#     # Nouvelle question : affichée tout de suite, puis réponse en direct
#     if question_en_cours:

#         heure_question = heure_actuelle()
#         afficher_message("user", question_en_cours, heure_question)

#         avatar = str(ROBOT) if robot_disponible else "🤖"

#         with st.chat_message("assistant", avatar=avatar):

#             afficher_html('<div class="msg-nom">🤖 RadiologyBot AI</div>')

#             erreur_technique = None

#             try:
#                 if ask_ai_stream is None:
#                     raise RuntimeError(
#                         f"Moteur RAG indisponible : {erreur_import}"
#                     )

#                 flux = ask_ai_stream(question_en_cours)

#                 # Le spinner dure jusqu'au premier mot, puis la réponse s'écrit en direct
#                 with st.spinner("RadiologyBot écrit..."):
#                     premier = next(flux, None)

#                 if premier is None:
#                     reponse = (
#                         "Je n'ai pas pu produire une réponse. "
#                         "Veuillez reformuler votre question."
#                     )
#                     st.markdown(reponse)
#                 else:
#                     reponse = st.write_stream(
#                         itertools.chain([premier], flux)
#                     )

#                 if not isinstance(reponse, str) or not reponse.strip():
#                     reponse = (
#                         "Je n'ai pas pu produire une réponse. "
#                         "Veuillez reformuler votre question."
#                     )

#             except Exception as erreur:
#                 erreur_technique = f"{type(erreur).__name__}: {erreur}"
#                 texte_erreur = str(erreur).upper()
#                 if any(m in texte_erreur for m in ("429", "RESOURCE_EXHAUSTED", "QUOTA")):
#                     reponse = (
#                         "⏳ Le service reçoit beaucoup de demandes en ce moment. "
#                         "Veuillez patienter environ une minute, puis reposer "
#                         "votre question."
#                     )
#                 else:
#                     reponse = (
#                         "Le service est momentanément indisponible. "
#                         "Veuillez réessayer plus tard ou contacter "
#                         "l'accueil de l'hôpital."
#                     )
#                 st.markdown(reponse)

#             heure_reponse = heure_actuelle()
#             afficher_html(f'<div class="msg-heure">{heure_reponse}</div>')

#             if erreur_technique:
#                 with st.expander("Détails techniques (pour le développeur)"):
#                     st.code(erreur_technique)

#         st.session_state.messages.append(
#             {"role": "user", "content": question_en_cours,
#              "heure": heure_question}
#         )
#         st.session_state.messages.append(
#             {"role": "assistant", "content": reponse,
#              "heure": heure_reponse}
#         )

#         nouvelle_reponse = True

# if nouvelle_reponse:
#     defiler_vers_le_dernier_message()


# # =====================================================
# # 11. QUESTIONS SUGGÉRÉES (en bas, sous la conversation)
# # =====================================================

# st.markdown(
#     '<div class="suggest-title">✨ Ou choisissez une question fréquente</div>',
#     unsafe_allow_html=True
# )

# questions = [
#     "Quels sont les horaires du service ?",
#     "Quels documents dois-je apporter ?",
#     "Où se trouve le service ?",
#     "Quels examens sont disponibles ?"
# ]

# col1, col2 = st.columns(2)

# for i, question in enumerate(questions):

#     with col1 if i % 2 == 0 else col2:

#         st.button(
#             question,
#             key=f"question_{i}",
#             width="stretch",
#             on_click=definir_question,
#             args=(question,)
#         )


# # =====================================================
# # 12. PIED DE PAGE
# # =====================================================

# st.divider()

# afficher_html("""
# <div class="footer">

#     <h3 style="color:#35d9ff;">
#         🤖 RadiologyBot AI
#     </h3>

#     Assistant intelligent d'information hospitalière
#     basé sur le RAG.

#         <br><br>

#     ⚠️ Ce chatbot ne remplace pas un médecin
#     et ne réalise aucun diagnostic médical.

#     <br><br>

#     <span style="color:#35d9ff;font-weight:700;">👨‍💻 Développé par</span><br>
#     <b style="color:#ffffff;">Ibrahima Dieng</b><br>
#     Élève ingénieur au Dakar Institute of Technology

#     <br><br>

#     <span style="color:#35d9ff;font-weight:700;">🎓 Encadré par</span><br>
#     <b style="color:#ffffff;">Mouhamed Naby Dia</b><br>
#     Ingénieur à Sanatel

#     <br><br>

#     Prototype de démonstration - Version 1.0

# </div>
# """, unsafe_allow_html=True)


# # =====================================================
# # 13. MENU LATÉRAL
# # =====================================================

# with st.sidebar:

#     st.title("🤖 RadiologyBot AI")

#     st.write(
#         "Assistant intelligent du service de radiologie."
#     )

#     st.divider()

#     if st.button(
#         "🗑️ Nouvelle conversation",
#         width="stretch"
#     ):

#         st.session_state.messages = []
#         st.session_state.pending_question = None
#         st.rerun()

#     st.info(
#         "Les réponses sont basées sur les informations "
#         "disponibles dans la base documentaire."
#     )


# # =====================================================
# # 14. PRÉCHAUFFAGE (après l'affichage de la page)
# # =====================================================

# if en_ligne:
#     try:
#         prechauffer()
#     except Exception:
#         pass
# fIN

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
# Fin

import streamlit as st
from datetime import datetime
from pathlib import Path
import re
import html

# =========================================================
# 1. CONNEXION AU MOTEUR RAG
# =========================================================

try:
    from chatbot import ask_ai_stream, service_pret
    ERREUR_IMPORT = None

except Exception as erreur:

    ask_ai_stream = None
    ERREUR_IMPORT = erreur

    def service_pret():
        return False


# =========================================================
# 2. CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RadiologyAI | Assistant hospitalier",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent

ROBOT_PATH = (
    BASE_DIR
    / "assets"
    / "radiologyai_robot.png"
)

AVATAR_ROBOT = (
    str(ROBOT_PATH)
    if ROBOT_PATH.exists()
    else "🤖"
)


# =========================================================
# 3. DÉTECTION AUTOMATIQUE DE LA LANGUE
# =========================================================

MOTS_WOLOF = {
    "naka", "nga", "jamm", "fan", "ana",
    "lan", "yan", "jëf", "jëfandikoo",
    "waxtu", "xam", "laaj", "ndax",
    "sama", "bëgg", "ñu", "ci", "ak",
    "waaw", "déedéet", "fépp", "mbokk",
    "nit", "dem", "man", "maa", "ngi",
    "rekk", "jërejëf", "talif", "suba",
    "tus", "yaram", "feebar", "ndimbal",
    "suñu", "sa", "bu", "bii", "bi",
    "xale", "ndey", "baay", "jàmm",
    "ñangi", "sant", "ndaxte"
}

MOTS_ANGLAIS = {
    "the", "what", "where", "when",
    "which", "how", "please", "hello",
    "hi", "opening", "hours", "department",
    "hospital", "appointment", "bring",
    "documents", "located", "scan",
    "examination", "radiology", "thank",
    "you", "can", "could", "is", "are",
    "do", "does", "my", "need", "tell",
    "about", "available", "service",
    "medical", "report", "room", "find"
}


def detecter_langue(question):

    texte = question.lower().strip()

    mots = set(
        re.findall(
            r"[a-zA-ZÀ-ÿŋñëó]+",
            texte
        )
    )

    score_wolof = len(
        mots.intersection(MOTS_WOLOF)
    )

    score_anglais = len(
        mots.intersection(MOTS_ANGLAIS)
    )

    if score_wolof >= 1 and score_wolof >= score_anglais:
        return "wolof"

    if score_anglais >= 2:
        return "anglais"

    return "français"


# =========================================================
# 4. TEXTES DE L'APPLICATION
# =========================================================

TEXTES = {

    "welcome": "Bonjour ! Je suis RadiologyAI.",

    "intro": (
        "Votre assistant intelligent pour obtenir "
        "des informations pratiques sur le service "
        "de radiologie."
    ),

    "placeholder": (
        "Écrivez votre question en français, "
        "en anglais ou en wolof..."
    ),

    "chat": "Votre conversation",

    "empty": (
        "Votre conversation commencera ici. "
        "Posez simplement votre question."
    ),

    "suggestions": "Questions fréquentes",

    "clear": "Effacer la conversation",

    "download": "Télécharger la conversation",

    "disclaimer": (
        "Informations générales uniquement. "
        "RadiologyAI ne remplace pas un professionnel "
        "de santé et ne réalise aucun diagnostic."
    ),

    "thinking": (
        "RadiologyAI consulte les informations du service..."
    ),

    "offline": (
        "Le service est momentanément indisponible. "
        "Veuillez réessayer plus tard ou contacter l'accueil."
    ),

    "no_answer": (
        "Je n'ai pas pu produire une réponse. "
        "Veuillez reformuler votre question."
    ),

    "online": "RadiologyAI est connecté",

    "offline_short": "Connexion indisponible",

    "quick": [

        "Quels sont les horaires du service ?",

        "Quels documents dois-je apporter ?",

        "Où se trouve le service de radiologie ?",

        "Quels examens sont disponibles ?"

    ]
}


# =========================================================
# 5. DESIGN PROFESSIONNEL BLEU
# =========================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {

        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(34,151,255,.12),
                transparent 28%
            ),

            radial-gradient(
                circle at 90% 18%,
                rgba(0,215,255,.10),
                transparent 24%
            ),

            linear-gradient(
                135deg,
                #f5f9ff 0%,
                #edf4ff 48%,
                #f8fbff 100%
            );

        color: #102b4e;
    }

    .main .block-container {

        max-width: 1180px;

        padding-top: 1.6rem;

        padding-bottom: 3rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* HERO */

    .hero {

        position: relative;

        overflow: hidden;

        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 22px;

        padding: 32px;

        border-radius: 25px;

        color: white;

        background:
            linear-gradient(
                120deg,
                #061b42 0%,
                #073d78 52%,
                #087fbd 100%
            );

        box-shadow:
            0 18px 48px rgba(4,39,89,.22);

        border: 1px solid rgba(255,255,255,.18);

        margin-bottom: 22px;
    }

    .hero:before {

        content: "";

        position: absolute;

        width: 360px;

        height: 360px;

        border-radius: 50%;

        right: -100px;

        top: -210px;

        background: rgba(70,205,255,.18);

        filter: blur(3px);
    }

    .hero-copy {
        position: relative;
        z-index: 2;
    }

    .hero-kicker {

        color: #83e5ff;

        font-size: .78rem;

        letter-spacing: .18em;

        font-weight: 800;

        text-transform: uppercase;

        margin-bottom: 9px;
    }

    .hero h1 {

        color: white !important;

        font-size: clamp(2rem, 4vw, 3.05rem);

        line-height: 1.05;

        font-weight: 800;

        margin: 0 0 12px 0;
    }

    .hero p {

        color: #e2f3ff !important;

        font-size: 1rem;

        line-height: 1.65;

        margin: 0;

        max-width: 650px;
    }

    /* ROBOT ANIMÉ */

    .bot-stage {

        position: relative;

        z-index: 2;

        flex: 0 0 178px;

        height: 150px;

        display: flex;

        align-items: center;

        justify-content: center;
    }

    .bot-head {

        position: relative;

        width: 142px;

        height: 112px;

        border-radius: 48px 48px 42px 42px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #cfeaff
            );

        border: 4px solid #6bdcff;

        box-shadow:
            0 0 0 7px rgba(79,208,255,.12),
            0 12px 30px rgba(0,0,0,.25),
            inset 0 -8px 14px rgba(24,113,195,.18);

        animation: robot-float 3s ease-in-out infinite;
    }

    @keyframes robot-float {

        0%, 100% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-7px);
        }
    }

    .bot-head:before {

        content: "";

        position: absolute;

        width: 46px;

        height: 12px;

        top: -13px;

        left: 44px;

        border-radius: 10px 10px 3px 3px;

        background: #55dfff;

        box-shadow: 0 0 15px #42d8ff;
    }

    .bot-ear {

        position: absolute;

        top: 39px;

        width: 13px;

        height: 35px;

        border-radius: 8px;

        background: #42cfff;

        box-shadow: 0 0 12px rgba(62,216,255,.8);
    }

    .bot-ear.left {
        left: -13px;
    }

    .bot-ear.right {
        right: -13px;
    }

    .bot-eye {

        position: absolute;

        top: 39px;

        width: 25px;

        height: 31px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle at 35% 30%,
                #bdfaff 0 10%,
                #28bfff 25%,
                #064aa4 75%
            );

        box-shadow: 0 0 13px #24caff;

        overflow: hidden;
    }

    .bot-eye.left {
        left: 32px;
    }

    .bot-eye.right {
        right: 32px;
    }

    .bot-eye:after {

        content: "";

        position: absolute;

        inset: -2px 0 100% 0;

        background: #dff7ff;

        border-radius: 50%;

        animation: blink 4.8s infinite;
    }

    @keyframes blink {

        0%, 44%, 50%, 100% {
            inset: -2px 0 100% 0;
        }

        46%, 48% {
            inset: -2px 0 0 0;
        }
    }

    .bot-mouth {

        position: absolute;

        width: 30px;

        height: 11px;

        left: 52px;

        bottom: 17px;

        border-bottom: 4px solid #1386cb;

        border-radius: 0 0 30px 30px;
    }

    .bot-glow {

        position: absolute;

        width: 105px;

        height: 15px;

        bottom: 2px;

        border-radius: 50%;

        background: rgba(34,203,255,.35);

        filter: blur(12px);
    }

    /* STATUT */

    .status-line {

        display: flex;

        align-items: center;

        gap: 9px;

        padding: 11px 15px;

        margin: 12px 0 18px;

        border: 1px solid #d5e7fb;

        border-radius: 13px;

        background: rgba(255,255,255,.78);

        color: #16436d;

        font-size: .88rem;

        font-weight: 600;
    }

    .status-dot {

        width: 9px;

        height: 9px;

        border-radius: 50%;

        background: #19bf83;

        box-shadow: 0 0 0 4px rgba(25,191,131,.13);
    }

    .section-title {

        color: #0a2b52;

        font-size: 1.15rem;

        font-weight: 800;

        margin: 18px 0 8px;
    }

    /* AVERTISSEMENT */

    .notice {

        background:
            linear-gradient(
                90deg,
                #fff9e9,
                #fffdf7
            );

        border: 1px solid #f2dfad;

        border-left: 5px solid #e0ae3d;

        color: #654d19;

        padding: 14px 17px;

        border-radius: 13px;

        margin: 16px 0 20px;

        font-size: .88rem;
    }

    /* BOUTONS */

    div.stButton > button {

        border-radius: 13px;

        min-height: 48px;

        border: 1px solid #d3e5f8;

        background: rgba(255,255,255,.9);

        color: #0a3c70;

        font-weight: 650;

        transition: all .2s ease;

        box-shadow:
            0 4px 13px rgba(20,74,130,.05);
    }

    div.stButton > button:hover {

        border-color: #159de0;

        color: #0066a8;

        background: #f1faff;

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px rgba(12,115,184,.12);
    }

    /* CHAMP DE CHAT */

    div[data-testid="stChatInput"] {

        border: 1px solid #9dc9ed;

        border-radius: 18px;

        box-shadow:
            0 8px 26px rgba(14,83,145,.09);

        background: white;
    }

    /* MESSAGES */

    div[data-testid="stChatMessage"] {

        border: 1px solid #e0ebf7;

        border-radius: 17px;

        padding: 12px 16px;

        background: rgba(255,255,255,.82);

        margin-bottom: 12px;

        box-shadow:
            0 5px 17px rgba(13,59,105,.035);
    }

    .footer {

        text-align: center;

        color: #66809c;

        font-size: .78rem;

        padding: 15px 0 4px;
    }

    @media (max-width: 700px) {

        .hero {
            padding: 24px 20px;
        }

        .bot-stage {
            flex-basis: 105px;
            transform: scale(.78);
            margin-right: -15px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 6. INITIALISATION DE LA SESSION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestion_selectionnee" not in st.session_state:
    st.session_state.suggestion_selectionnee = None


# =========================================================
# 7. EN-TÊTE RADIOLOGYAI
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-copy">

            <div class="hero-kicker">
                Votre assistant hospitalier intelligent
            </div>

            <h1>RadiologyAI</h1>

            <p>
                Un accueil digital pour vous guider
                et vous informer sur le service de radiologie.
                Posez votre question naturellement en français,
                en anglais ou en wolof.
            </p>

        </div>

        <div class="bot-stage">

            <div class="bot-glow"></div>

            <div class="bot-head">

                <div class="bot-ear left"></div>

                <div class="bot-ear right"></div>

                <div class="bot-eye left"></div>

                <div class="bot-eye right"></div>

                <div class="bot-mouth"></div>

            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 8. VÉRIFICATION DU MOTEUR RAG
# =========================================================

if ERREUR_IMPORT is not None:

    st.error(
        "Impossible de charger chatbot.py. "
        "Vérifiez que ce fichier est présent "
        "dans le même dossier que app.py."
    )

    with st.expander("Détails techniques"):
        st.code(str(ERREUR_IMPORT))

    moteur_disponible = False

else:

    try:
        moteur_disponible = bool(service_pret())

    except Exception:
        moteur_disponible = False


if moteur_disponible:

    st.markdown(
        """
        <div class="status-line">
            <span class="status-dot"></span>
            RadiologyAI est prêt à vous répondre
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "Connexion au moteur indisponible pour le moment. "
        "Vérifiez la configuration de chatbot.py."
    )


# =========================================================
# 9. ACCUEIL ET AVERTISSEMENT
# =========================================================

st.markdown(
    '<div class="section-title">Bienvenue sur RadiologyAI</div>',
    unsafe_allow_html=True
)

st.write(TEXTES["intro"])

st.markdown(
    f"""
    <div class="notice">
        ⚕️ {html.escape(TEXTES["disclaimer"])}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 10. QUESTIONS FRÉQUENTES
# =========================================================

st.markdown(
    '<div class="section-title">✨ Questions fréquentes</div>',
    unsafe_allow_html=True
)

colonnes = st.columns(2)

for index, suggestion in enumerate(TEXTES["quick"]):

    with colonnes[index % 2]:

        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True
        ):

            st.session_state.suggestion_selectionnee = suggestion


# =========================================================
# 11. EFFACER ET TÉLÉCHARGER LA CONVERSATION
# =========================================================

col_effacer, col_telecharger = st.columns(2)

with col_effacer:

    if st.button(
        TEXTES["clear"],
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.suggestion_selectionnee = None

        st.rerun()


with col_telecharger:

    contenu = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            role = "Patient"
        else:
            role = "RadiologyAI"

        contenu.append(
            f"{role} :\n{message['content']}"
        )

    texte_conversation = "\n\n".join(contenu)

    st.download_button(
        label=TEXTES["download"],
        data=texte_conversation or "Aucune conversation.",
        file_name=(
            f"radiologyai_conversation_"
            f"{datetime.now():%Y%m%d_%H%M}.txt"
        ),
        mime="text/plain",
        use_container_width=True,
        disabled=not bool(st.session_state.messages)
    )


# =========================================================
# 12. AFFICHAGE DE L'HISTORIQUE
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">💬 Votre conversation avec RadiologyAI</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.info(TEXTES["empty"])


for message in st.session_state.messages:

    if message["role"] == "assistant":

        with st.chat_message(
            "assistant",
            avatar=AVATAR_ROBOT
        ):

            st.markdown(message["content"])

    else:

        with st.chat_message(
            "user",
            avatar="🧑"
        ):

            st.markdown(message["content"])


# =========================================================
# 13. SAISIE DE LA QUESTION
# =========================================================

question_saisie = st.chat_input(
    TEXTES["placeholder"]
)

if question_saisie is not None:

    question = question_saisie.strip()

else:

    question = st.session_state.suggestion_selectionnee


st.session_state.suggestion_selectionnee = None


# =========================================================
# 14. TRAITEMENT DE LA QUESTION PAR LE RAG
# =========================================================

if question:

    # Détection automatique de la langue
    langue_detectee = detecter_langue(question)

    # Enregistrement de la question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user",
        avatar="🧑"
    ):

        st.markdown(question)

    # Génération de la réponse
    with st.chat_message(
        "assistant",
        avatar=AVATAR_ROBOT
    ):

        if ask_ai_stream is None:

            reponse = TEXTES["offline"]

            st.error(reponse)

        else:

            try:

                with st.spinner(TEXTES["thinking"]):

                    resultat = st.write_stream(
                        ask_ai_stream(
                            question,
                            langue=langue_detectee
                        )
                    )

                if isinstance(resultat, str) and resultat.strip():

                    reponse = resultat

                else:

                    reponse = TEXTES["no_answer"]

                    st.warning(reponse)

            except Exception as erreur:

                reponse = TEXTES["offline"]

                st.error(reponse)

                with st.expander("Détails techniques"):

                    st.code(str(erreur))

    # Enregistrement de la réponse
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reponse
        }
    )


# =========================================================
# 15. PIED DE PAGE
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        <strong>RadiologyAI</strong>
        · Assistant intelligent d'information hospitalière

        <br>

        Prototype de démonstration.
        Les informations doivent être vérifiées et validées
        par le personnel hospitalier.

    </div>
    """,
    unsafe_allow_html=True
)

