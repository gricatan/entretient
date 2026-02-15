import asyncio
import os
from dotenv import load_dotenv
from mistralai import Mistral
import re

# Charger le .env
load_dotenv()


def nettoyer_texte(t) -> str:
    # enlever les échappements LaTeX
    t = t.replace("\\(", "(").replace("\\)", ")")
    t = t.replace("\\[", "[").replace("\\]", "]")

    # enlever les backslashes restants
    t = t.replace("\\", "")

    # enlever le gras Markdown
    t = t.replace("**", "")

    # enlever boxed{...}
    t = re.sub(r"boxed\{([^}]*)\}", r"\1", t)

    # enlever les crochets autour d'une expression
    t = re.sub(r"\[\s*(.*?)\s*\]", r"\1", t)

    # 🔥 corriger les mots collés : lettres collées à lettres
    t = re.sub(r"([a-zA-Zéèàùâêîôûç])([A-ZÉÈÀÙÂÊÎÔÛÇ])", r"\1 \2", t)

    # 🔥 corriger les chiffres collés aux lettres
    t = re.sub(r"(\d)([a-zA-Zéèàùâêîôûç])", r"\1 \2", t)
    t = re.sub(r"([a-zA-Zéèàùâêîôûç])(\d)", r"\1 \2", t)

    # 🔥 corriger les mots collés autour de la ponctuation
    t = re.sub(r"([a-zA-Zéèàùâêîôûç])(\()", r"\1 \2", t)
    t = re.sub(r"\)([a-zA-Zéèàùâêîôûç])", r") \1", t)

    return t


complete_answer = ""

API_KEY = os.getenv("MISTRAL_API_KEY")

if not API_KEY:
    raise ValueError("La clé API Mistral n'est pas définie dans .env")


async def main():
    model = "mistral-large-latest"
    global complete_answer
    client = Mistral(api_key=API_KEY)

    # prompt = "Salut, je teste comment fonctionne le chat, reponse courte souhaitée"
    # prompt = 'Refactorise en une seule ligne (avec compréhension ?) ce code :\nfor i in range(0, 10):\n    print(i, end=" ")'
    prompt = "Combien fait 3 ** 5 ?"

    response = await client.chat.stream_async(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Réponds toujours en texte brut, sans Markdown, sans LaTeX, sans mise en forme, sans parenthèses mathématiques, sans crochets, sans backslashes. Donne uniquement la réponse expliquée de manière simple et lisible.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    async for chunk in response:
        rep = None
        if chunk.data.choices[0].delta.content is not None:
            rep = chunk.data.choices[0].delta.content
            rep = nettoyer_texte(rep)
            complete_answer = complete_answer + rep

    # Affiche en console l'échange complet
    print(
        f'\nRéponse à la question "\033[32m{prompt}\033[0m" :\n\n\033[1;32m{complete_answer}\033[0m\n',
        end="\n",
        flush=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
