from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Charger le modèle d'embeddings (Ollama, identique à celui de la base chroma_db)
embeddings = OllamaEmbeddings(
    model="bge-m3"
)


# 2. Charger la base de connaissances
vectorstore = Chroma(
    collection_name="radiologie",
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# 3. Créer le moteur de recherche
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


# 4. Charger le modèle Gemma (via Ollama, gratuit et local)
llm = ChatOllama(
    model="gemma4:e4b",
    temperature=0.1,
    top_p=0.99
)


# 5. Fonction principale du chatbot
def ask_ai(question: str) -> str:

    # Rechercher les passages correspondant à la question
    documents = retriever.invoke(question)

    # Vérifier si des informations ont été trouvées
    if not documents:
        return (
            "Je ne trouve pas cette information dans "
            "les documents du service de radiologie. "
            "Veuillez contacter l'accueil de l'hôpital."
        )

    # Récupérer le contenu des passages
    contexte = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Construire le prompt
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

    # Envoyer le prompt au modèle
    reponse = llm.invoke(prompt)

    return reponse.content