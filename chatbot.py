"""Moteur RAG de RadiologyBot AI (version cloud : Google Gemini).

Aucun serveur local : tout passe par l'API Gemini. La base de
connaissances est construite en mémoire à partir de radiologie.txt.
"""

import os
from pathlib import Path

import streamlit as st
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

FICHE = Path(__file__).parent / "radiologie.txt"


def _secret(nom: str, defaut: str = "") -> str:
    """Lit un secret Streamlit, sinon une variable d'environnement."""
    try:
        valeur = st.secrets.get(nom)
    except Exception:
        valeur = None
    return str(valeur or os.environ.get(nom, defaut))


def service_pret() -> bool:
    """True si la clé API et la fiche du service sont disponibles."""
    return bool(_secret("GOOGLE_API_KEY")) and FICHE.exists()


@st.cache_resource(show_spinner=False)
def _moteur():
    """Construit (une seule fois) la recherche et le modèle."""
    cle = _secret("GOOGLE_API_KEY")
    if not cle:
        raise RuntimeError(
            "Clé GOOGLE_API_KEY absente : ajoutez-la dans les Secrets de l'application."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=_secret("MODELE_EMBEDDINGS", "gemini-embedding-001"),
        google_api_key=cle,
    )

    # Un passage par section "## ...", puis découpe des sections trop longues
    texte = FICHE.read_text(encoding="utf-8")
    sections = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("##", "section")],
        strip_headers=False,
    ).split_text(texte)
    passages = RecursiveCharacterTextSplitter(
        chunk_size=900, chunk_overlap=100
    ).split_documents(sections)

    base = InMemoryVectorStore.from_documents(passages, embeddings)
    retriever = base.as_retriever(search_kwargs={"k": 4})

    # Si vous passez à un modèle Gemini 3 ou plus récent, supprimez temperature.
    llm = ChatGoogleGenerativeAI(
        model=_secret("MODELE_LLM", "gemini-2.5-flash"),
        temperature=0.1,
        google_api_key=cle,
    )
    return retriever, llm


def _texte(reponse) -> str:
    """Extrait le texte de la réponse, quelle que soit la version de LangChain."""
    texte = getattr(reponse, "text", None)
    if callable(texte):
        texte = texte()
    if isinstance(texte, str) and texte.strip():
        return texte
    contenu = reponse.content
    if isinstance(contenu, list):
        return "".join(
            bloc.get("text", "") if isinstance(bloc, dict) else str(bloc)
            for bloc in contenu
        )
    return str(contenu)


def ask_ai(question: str) -> str:

    retriever, llm = _moteur()

    documents = retriever.invoke(question)

    if not documents:
        return (
            "Je ne trouve pas cette information dans "
            "les documents du service de radiologie. "
            "Veuillez contacter l'accueil de l'hôpital."
        )

    contexte = "\n\n".join(d.page_content for d in documents)

    prompt = f"""
Tu es RadiologyBot AI, un assistant d'information
du service de radiologie de l'hôpital régional de Thiès.

Ta mission est de répondre aux questions des patients.

RÈGLES IMPORTANTES :
- Utilise uniquement les informations du contexte.
- N'invente jamais d'horaires, de tarifs ou de prestations.
- Si la réponse n'est pas dans le contexte, dis-le clairement.
- Ne donne pas de diagnostic médical.
- Oriente le patient vers le personnel hospitalier
  pour toute question médicale personnelle.
- Réponds en français simple et compréhensible.

CONTEXTE :
{contexte}

QUESTION DU PATIENT :
{question}

RÉPONSE :
"""

    return _texte(llm.invoke(prompt))
