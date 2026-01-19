from langchain_google_genai import ChatGoogleGenerativeAI

from search import search_prompt
from loguru import logger


def main():
    question = input("Pressione Enter para iniciar o chat...\n\nPergunta: ")
    if not question:
        logger.error("Nenhuma pergunta foi fornecida.")
        return

    chain = search_prompt(question)

    if not chain:
        logger.error(
            "Não foi possível iniciar o chat. Verifique os erros de inicialização."
        )
        return

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")  # , temperature=0)
    response = llm.invoke(chain)

    print(response.content)


if __name__ == "__main__":
    main()
