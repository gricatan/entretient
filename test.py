import asyncio
import os

from mistralai import Mistral

contenu  = ""

async def main():
    api_key = "gY80p6a14yvu0jfMzv1SSeiXl43hn8QB"
    model = "mistral-large-latest"
    global contenu
    client = Mistral(api_key=api_key)

    response = await client.chat.stream_async(
        model=model,
        messages=[
             {
                  "role": "user",
                  "content": "Salut, je teste comment fonctionne le chat, reponse courte",
              },
        ],
    )

    # If you want to print the stream text to the console
    async for chunk in response:
        if chunk.data.choices[0].delta.content is not None:
            print(chunk.data.choices[0].delta.content, end="")
            contenu = contenu + chunk.data.choices[0].delta.content
    print(f"contenu{contenu}")
if __name__ == "__main__":
    asyncio.run(main())
    print(f"contenu{contenu}")

