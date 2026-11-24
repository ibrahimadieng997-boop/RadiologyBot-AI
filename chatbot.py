# """Moteur RAG de RadiologyBot AI (version cloud : Google Gemini).

# Aucun serveur local : tout passe par l'API Gemini. La base de
# connaissances est construite en mémoire à partir de radiologie.txt.
# """

# import os
# import re
# import time
# from pathlib import Path

# import streamlit as st
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_google_genai import (
#     ChatGoogleGenerativeAI,
#     GoogleGenerativeAIEmbeddings,
# )
# from langchain_text_splitters import (
#     MarkdownHeaderTextSplitter,
#     RecursiveCharacterTextSplitter,
# )

# FICHE = Path(__file__).parent / "radiologie.txt"


# def _secret(nom: str, defaut: str = "") -> str:
#     """Lit un secret Streamlit, sinon une variable d'environnement."""
#     try:
#         valeur = st.secrets.get(nom)
#     except Exception:
#         valeur = None
#     return str(valeur or os.environ.get(nom, defaut))


# def service_pret() -> bool:
#     """True si la clé API et la fiche du service sont disponibles."""
#     return bool(_secret("GOOGLE_API_KEY")) and FICHE.exists()


# def _gemini_recent(nom: str) -> bool:
#     """True pour les modèles Gemini 3 et plus (pas pour Gemini 2, Gemma...)."""
#     m = re.match(r"(?:models/)?gemini-(\d+)", nom or "")
#     return bool(m) and int(m.group(1)) >= 3


# @st.cache_resource(show_spinner=False)
# def _moteur():
#     """Construit (une seule fois) la recherche et le modèle."""
#     cle = _secret("GOOGLE_API_KEY")
#     if not cle:
#         raise RuntimeError(
#             "Clé GOOGLE_API_KEY absente : ajoutez-la dans les Secrets de l'application."
#         )

#     embeddings = GoogleGenerativeAIEmbeddings(
#         model=_secret("MODELE_EMBEDDINGS", "gemini-embedding-001"),
#         google_api_key=cle,
#     )

#     # Un passage par section "## ...", puis découpe des sections trop longues
#     texte = FICHE.read_text(encoding="utf-8")
#     sections = MarkdownHeaderTextSplitter(
#         headers_to_split_on=[("##", "section")],
#         strip_headers=False,
#     ).split_text(texte)
#     passages = RecursiveCharacterTextSplitter(
#         chunk_size=900, chunk_overlap=100
#     ).split_documents(sections)

#     base = InMemoryVectorStore.from_documents(passages, embeddings)
#     retriever = base.as_retriever(search_kwargs={"k": 4})

#     modele = _secret("MODELE_LLM", "gemini-3.8-flash")

#     # Gemini 3 et plus récent : température par défaut (recommandé).
#     # Autres modèles (Gemma, Gemini 2...) : température basse.
#     options = {}
#     if not _gemini_recent(modele):
#         options["temperature"] = 0.1

#     llm_standard = ChatGoogleGenerativeAI(
#         model=modele,
#         google_api_key=cle,
#         max_retries=1,      # chaque nouvelle tentative consomme du quota
#         **options,
#     )

#     # Réponses plus rapides : on limite la "réflexion" du modèle (Gemini 3+).
#     # Pour désactiver, ajoutez REFLEXION = "" dans les Secrets.
#     effort = _secret("REFLEXION", "low")
#     if effort and _gemini_recent(modele):
#         try:
#             llm_rapide = ChatGoogleGenerativeAI(
#                 model=modele,
#                 google_api_key=cle,
#                 max_retries=1,
#                 reasoning_effort=effort,
#             )
#         except Exception:
#             llm_rapide = llm_standard
#     else:
#         llm_rapide = llm_standard

#     modeles = [llm_rapide]
#     if llm_standard is not llm_rapide:
#         modeles.append(llm_standard)       # secours si le réglage rapide est refusé

#     # Modèle de secours facultatif (autre nom de modèle), utilisé si le 1er est surchargé
#     secours = _secret("MODELE_SECOURS")
#     if secours and secours != modele:
#         options_secours = {}
#         if not _gemini_recent(secours):
#             options_secours["temperature"] = 0.1
#         modeles.append(
#             ChatGoogleGenerativeAI(
#                 model=secours,
#                 google_api_key=cle,
#                 max_retries=1,
#                 **options_secours,
#             )
#         )

#     return retriever, modeles


# def prechauffer():
#     """Prépare le moteur au démarrage (le 1er visiteur n'attend pas)."""
#     _moteur()


# @st.cache_resource(show_spinner=False)
# def _cache_reponses():
#     """Mémoire des réponses déjà données (questions fréquentes instantanées)."""
#     return {}


# def _texte(reponse) -> str:
#     """Extrait le texte de la réponse, quelle que soit la version de LangChain."""
#     texte = getattr(reponse, "text", None)
#     if not isinstance(texte, str) and callable(texte):
#         texte = texte()          # anciennes versions : text() est une méthode
#     if isinstance(texte, str) and texte.strip():
#         return str(texte)
#     contenu = reponse.content
#     if isinstance(contenu, list):
#         return "".join(
#             bloc.get("text", "") if isinstance(bloc, dict) else str(bloc)
#             for bloc in contenu
#         )
#     return str(contenu)


# def ask_ai(question: str) -> str:

#     retriever, modeles = _moteur()
#     llm = modeles[0]

#     documents = retriever.invoke(question)

#     if not documents:
#         return (
#             "Je ne trouve pas cette information dans "
#             "les documents du service de radiologie. "
#             "Veuillez contacter l'accueil de l'hôpital."
#         )

#     contexte = "\n\n".join(d.page_content for d in documents)

#     prompt = f"""
# Tu es RadiologyBot AI, un assistant d'information
# du service de radiologie de l'hôpital régional de Thiès.

# Ta mission est de répondre aux questions des patients.

# RÈGLES IMPORTANTES :
# - Utilise uniquement les informations du contexte.
# - N'invente jamais d'horaires, de tarifs ou de prestations.
# - Si la réponse n'est pas dans le contexte, dis-le clairement.
# - Ne donne pas de diagnostic médical.
# - Oriente le patient vers le personnel hospitalier
#   pour toute question médicale personnelle.
# - Réponds en français simple et compréhensible.

# CONTEXTE :
# {contexte}

# QUESTION DU PATIENT :
# {question}

# RÉPONSE :
# """

#     return _texte(llm.invoke(prompt))


# def _construire_prompt(contexte: str, question: str) -> str:
#     return f"""
# Tu es RadiologyBot AI, un assistant d'information
# du service de radiologie de l'hôpital régional de Thiès.

# Ta mission est de répondre aux questions des patients.

# RÈGLES IMPORTANTES :
# - Utilise uniquement les informations du contexte.
# - N'invente jamais d'horaires, de tarifs ou de prestations.
# - Si la réponse n'est pas dans le contexte, dis-le clairement.
# - Ne donne pas de diagnostic médical.
# - Oriente le patient vers le personnel hospitalier
#   pour toute question médicale personnelle.
# - Réponds en français simple et compréhensible.

# CONTEXTE :
# {contexte}

# QUESTION DU PATIENT :
# {question}

# RÉPONSE :
# """


# def _est_quota(erreur) -> bool:
#     texte = str(erreur).upper()
#     return any(m in texte for m in ("429", "RESOURCE_EXHAUSTED", "QUOTA"))


# def _est_surcharge(erreur) -> bool:
#     texte = str(erreur).upper()
#     return any(m in texte for m in ("503", "UNAVAILABLE", "OVERLOADED", "HIGH DEMAND"))


# def ask_ai_stream(question: str):
#     """Version rapide : renvoie la réponse morceau par morceau (streaming)."""
#     cle = " ".join(question.lower().split())
#     memoire = _cache_reponses()

#     # Question déjà posée : réponse immédiate
#     if cle in memoire:
#         for morceau in re.split(r"(\s+)", memoire[cle]):
#             yield morceau
#             time.sleep(0.004)
#         return

#     retriever, modeles = _moteur()

#     documents = retriever.invoke(question)

#     if not documents:
#         yield (
#             "Je ne trouve pas cette information dans "
#             "les documents du service de radiologie. "
#             "Veuillez contacter l'accueil de l'hôpital."
#         )
#         return

#     contexte = "\n\n".join(d.page_content for d in documents)
#     prompt = _construire_prompt(contexte, question)

#     texte = ""
#     derniere = None
#     reussi = False
#     modeles_ecartes = set()

#     for modele in modeles:
#         nom = getattr(modele, "model", None)
#         if nom in modeles_ecartes:
#             continue                      # même modèle déjà en échec : inutile

#         for tentative in (1, 2):
#             try:
#                 for morceau in modele.stream(prompt):
#                     extrait = _texte(morceau)
#                     if extrait:
#                         texte += extrait
#                         yield extrait
#                 reussi = True
#                 break
#             except Exception as erreur:
#                 if texte:
#                     raise                 # déjà commencé à écrire
#                 derniere = erreur
#                 if _est_quota(erreur):
#                     modeles_ecartes.add(nom)   # passer à un autre modèle s'il existe
#                     break
#                 if _est_surcharge(erreur):
#                     # Surcharge temporaire de Google : une seule nouvelle tentative
#                     if tentative == 1:
#                         time.sleep(3)
#                         continue
#                     modeles_ecartes.add(nom)
#                 break
#         if reussi:
#             break

#     if not reussi and derniere is not None:
#         raise derniere

#     if texte.strip():
#         memoire[cle] = texte
# Fin 

# """
# Moteur RAG de RadiologyBot AI
# Architecture cloud : Google Gemini + LangChain + Streamlit.

# Base de connaissances : radiologie.txt
# Langues : français, anglais et wolof.
# """

# import os
# import re
# import time
# from pathlib import Path

# import streamlit as st

# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_google_genai import (
#     ChatGoogleGenerativeAI,
#     GoogleGenerativeAIEmbeddings,
# )
# from langchain_text_splitters import (
#     MarkdownHeaderTextSplitter,
#     RecursiveCharacterTextSplitter,
# )


# # ==========================================================
# # 1. CONFIGURATION
# # ==========================================================

# FICHE = Path(__file__).parent / "radiologie.txt"

# LANGUES = {
#     "fr": "français",
#     "français": "français",
#     "french": "français",
#     "en": "anglais",
#     "anglais": "anglais",
#     "english": "anglais",
#     "wo": "wolof",
#     "wolof": "wolof",
# }


# # ==========================================================
# # 2. GESTION DES SECRETS
# # ==========================================================

# def _secret(nom: str, defaut: str = "") -> str:
#     """Lit un secret Streamlit ou une variable d'environnement."""

#     try:
#         valeur = st.secrets.get(nom)
#     except Exception:
#         valeur = None

#     return str(valeur or os.environ.get(nom, defaut))


# def service_pret() -> bool:
#     """Vérifie la présence de la clé API et du document."""

#     return (
#         bool(_secret("GOOGLE_API_KEY"))
#         and FICHE.exists()
#         and FICHE.stat().st_size > 0
#     )


# def normaliser_langue(langue: str = "français") -> str:
#     """Convertit les différentes écritures vers une langue reconnue."""

#     valeur = str(langue or "français").strip().lower()

#     return LANGUES.get(valeur, "français")


# # ==========================================================
# # 3. CONSTRUCTION DU MOTEUR RAG
# # ==========================================================

# @st.cache_resource(show_spinner=False)
# def _moteur():
#     """Construit les embeddings, la base vectorielle et Gemini."""

#     cle = _secret("GOOGLE_API_KEY")

#     if not cle:
#         raise RuntimeError(
#             "La clé GOOGLE_API_KEY est absente. "
#             "Configure-la dans les Secrets Streamlit."
#         )

#     if not FICHE.exists():
#         raise FileNotFoundError(
#             f"Le fichier {FICHE.name} est introuvable."
#         )

#     texte = FICHE.read_text(encoding="utf-8").strip()

#     if not texte:
#         raise ValueError(
#             "Le fichier radiologie.txt est vide."
#         )

#     # Embeddings Google
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model=_secret(
#             "MODELE_EMBEDDINGS",
#             "gemini-embedding-001"
#         ),
#         google_api_key=cle,
#     )

#     # Découpage par sections Markdown
#     sections = MarkdownHeaderTextSplitter(
#         headers_to_split_on=[
#             ("##", "section")
#         ],
#         strip_headers=False,
#     ).split_text(texte)

#     # Découpage des sections en petits passages
#     passages = RecursiveCharacterTextSplitter(
#         chunk_size=900,
#         chunk_overlap=100,
#     ).split_documents(sections)

#     if not passages:
#         raise ValueError(
#             "Aucun passage exploitable dans radiologie.txt."
#         )

#     # Création de la base vectorielle
#     base = InMemoryVectorStore.from_documents(
#         passages,
#         embeddings,
#     )

#     retriever = base.as_retriever(
#         search_kwargs={"k": 4}
#     )

#     # Modèle principal
#     modele_principal = _secret(
#         "MODELE_LLM",
#         "gemini-2.5-flash"
#     )

#     llm_principal = ChatGoogleGenerativeAI(
#         model=modele_principal,
#         google_api_key=cle,
#         temperature=0.1,
#         max_retries=1,
#     )

#     modeles = [llm_principal]

#     # Modèle de secours facultatif
#     modele_secours = _secret("MODELE_SECOURS")

#     if modele_secours and modele_secours != modele_principal:

#         llm_secours = ChatGoogleGenerativeAI(
#             model=modele_secours,
#             google_api_key=cle,
#             temperature=0.1,
#             max_retries=1,
#         )

#         modeles.append(llm_secours)

#     return retriever, modeles


# # ==========================================================
# # 4. PRÉCHAUFFAGE
# # ==========================================================

# def prechauffer():
#     """Prépare le moteur au démarrage."""

#     _moteur()


# # ==========================================================
# # 5. CACHE DES RÉPONSES
# # ==========================================================

# @st.cache_resource(show_spinner=False)
# def _cache_reponses():
#     """Conserve les réponses fréquentes."""

#     return {}


# # ==========================================================
# # 6. EXTRACTION DU TEXTE
# # ==========================================================

# def _texte(reponse) -> str:
#     """Extrait le texte d'une réponse LangChain."""

#     contenu = getattr(reponse, "content", None)

#     if contenu is None:
#         valeur = getattr(reponse, "text", "")
#         if callable(valeur):
#             valeur = valeur()
#         return str(valeur or "")

#     if isinstance(contenu, str):
#         return contenu

#     if isinstance(contenu, list):
#         morceaux = []

#         for bloc in contenu:
#             if isinstance(bloc, dict):
#                 morceaux.append(str(bloc.get("text", "")))
#             else:
#                 morceaux.append(str(bloc))

#         return "".join(morceaux)

#     return str(contenu)


# # ==========================================================
# # 7. MESSAGES DE SECOURS
# # ==========================================================

# def _message_indisponible(langue: str) -> str:
#     """Retourne un message lorsque l'information est absente."""

#     messages = {
#         "français": (
#             "Je ne trouve pas cette information dans les "
#             "documents du service de radiologie. "
#             "Veuillez contacter l'accueil de l'hôpital."
#         ),
#         "anglais": (
#             "I cannot find this information in the radiology "
#             "department documents. Please contact the hospital reception."
#         ),
#         "wolof": (
#             "Xibaar bii gisuma ko ci kayiti departema radiologie bi. "
#             "Jëfandikool accueil bu lopitaal bi ngir am leeral."
#         ),
#     }

#     return messages[langue]


# # ==========================================================
# # 8. CONSTRUCTION DU PROMPT MULTILINGUE
# # ==========================================================

# def _construire_prompt(
#     contexte: str,
#     question: str,
#     langue: str = "français",
# ) -> str:

#     langue = normaliser_langue(langue)

#     return f"""
# Tu es RadiologyBot AI, un assistant d'information
# du service de radiologie de l'hôpital régional de Thiès.

# MISSION :
# Répondre clairement aux questions des patients
# concernant le fonctionnement du service.

# LANGUE OBLIGATOIRE :
# La réponse doit être entièrement rédigée en {langue}.

# RÈGLES IMPORTANTES :

# 1. Utilise uniquement les informations présentes dans le contexte.
# 2. N'invente jamais d'horaires, de tarifs ou de prestations.
# 3. Si une information est absente, indique-le clairement.
# 4. Ne donne jamais de diagnostic médical.
# 5. Ne prescris aucun médicament.
# 6. Pour une question médicale personnelle, oriente le patient
#    vers un professionnel de santé.
# 7. Utilise des phrases simples et compréhensibles.
# 8. Ne présente jamais une information inventée comme une
#    information officielle de l'hôpital.
# 9. Si le contexte ne permet pas de répondre, dis-le dans
#    la langue demandée.

# CONTEXTE DOCUMENTAIRE :

# {contexte}

# QUESTION DU PATIENT :

# {question}

# RÉPONSE EN {langue.upper()} :
# """


# # ==========================================================
# # 9. GESTION DES ERREURS GEMINI
# # ==========================================================

# def _est_quota(erreur) -> bool:

#     texte = str(erreur).upper()

#     return any(
#         mot in texte
#         for mot in (
#             "429",
#             "RESOURCE_EXHAUSTED",
#             "QUOTA",
#         )
#     )


# def _est_surcharge(erreur) -> bool:

#     texte = str(erreur).upper()

#     return any(
#         mot in texte
#         for mot in (
#             "503",
#             "UNAVAILABLE",
#             "OVERLOADED",
#             "HIGH DEMAND",
#         )
#     )


# # ==========================================================
# # 10. RECHERCHE DOCUMENTAIRE
# # ==========================================================

# def _rechercher(question: str):
#     """Recherche les passages les plus pertinents."""

#     retriever, modeles = _moteur()

#     documents = retriever.invoke(question)

#     return documents, modeles


# # ==========================================================
# # 11. GÉNÉRATION CLASSIQUE
# # ==========================================================

# def ask_ai(
#     question: str,
#     langue: str = "français",
# ) -> str:
#     """Génère une réponse complète."""

#     question = str(question or "").strip()
#     langue = normaliser_langue(langue)

#     if not question:
#         return "Veuillez saisir une question."

#     documents, modeles = _rechercher(question)

#     if not documents:
#         return _message_indisponible(langue)

#     contexte = "\n\n".join(
#         document.page_content
#         for document in documents
#     )

#     prompt = _construire_prompt(
#         contexte,
#         question,
#         langue,
#     )

#     derniere_erreur = None

#     for modele in modeles:
#         try:
#             reponse = modele.invoke(prompt)
#             resultat = _texte(reponse).strip()

#             if resultat:
#                 return resultat

#         except Exception as erreur:
#             derniere_erreur = erreur

#             if _est_quota(erreur) or _est_surcharge(erreur):
#                 continue

#             continue

#     if derniere_erreur:
#         raise RuntimeError(
#             "Impossible de générer une réponse avec Gemini. "
#             "Vérifie la clé API, le modèle et ton quota."
#         ) from derniere_erreur

#     return _message_indisponible(langue)


# # ==========================================================
# # 12. GÉNÉRATION AVEC STREAMING
# # ==========================================================

# def ask_ai_stream(
#     question: str,
#     langue: str = "français",
# ):
#     """
#     Génère une réponse progressivement.

#     Exemple :
#     for morceau in ask_ai_stream(question, langue):
#         st.write(morceau)
#     """

#     question = str(question or "").strip()
#     langue = normaliser_langue(langue)

#     if not question:
#         yield "Veuillez saisir une question."
#         return

#     memoire = _cache_reponses()

#     # La langue fait partie de la clé du cache
#     cle = (
#         langue,
#         " ".join(question.lower().split()),
#     )

#     # Réponse déjà disponible
#     if cle in memoire:

#         for morceau in re.split(
#             r"(\s+)",
#             memoire[cle],
#         ):
#             if morceau:
#                 yield morceau

#         return

#     documents, modeles = _rechercher(question)

#     if not documents:
#         yield _message_indisponible(langue)
#         return

#     contexte = "\n\n".join(
#         document.page_content
#         for document in documents
#     )

#     prompt = _construire_prompt(
#         contexte,
#         question,
#         langue,
#     )

#     texte_complet = ""
#     derniere_erreur = None

#     # Essai des modèles disponibles
#     for modele in modeles:

#         reussi = False

#         for tentative in range(2):

#             try:

#                 for morceau in modele.stream(prompt):

#                     extrait = _texte(morceau)

#                     if extrait:
#                         texte_complet += extrait
#                         yield extrait

#                 reussi = True
#                 break

#             except Exception as erreur:

#                 derniere_erreur = erreur

#                 # Si des morceaux ont déjà été envoyés,
#                 # on ne peut plus recommencer sans dupliquer.
#                 if texte_complet:
#                     raise

#                 # Quota : passer directement au modèle suivant
#                 if _est_quota(erreur):
#                     break

#                 # Surcharge : une seule nouvelle tentative
#                 if _est_surcharge(erreur) and tentative == 0:
#                     time.sleep(2)
#                     continue

#                 break

#         if reussi:
#             break

#     # Tous les modèles ont échoué
#     if not texte_complet.strip():

#         if derniere_erreur:
#             raise RuntimeError(
#                 "Les modèles Gemini ne sont pas disponibles. "
#                 "Vérifie ta clé API, ton quota et les noms des modèles."
#             ) from derniere_erreur

#         yield _message_indisponible(langue)
#         return

#     # Enregistrer uniquement les réponses complètes
#     memoire[cle] = texte_complet.strip()
#Fin 
# nouveau
