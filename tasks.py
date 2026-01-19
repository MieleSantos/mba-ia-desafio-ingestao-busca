from invoke import task
import subprocess
import sys
from loguru import logger


@task
def format(c):
    """Formata código com black e isort"""
    logger.info("Executando black...")
    subprocess.run(["poetry", "run", "black", "src/"], check=True)
    logger.info("Executando isort...")
    subprocess.run(["poetry", "run", "isort", "src/"], check=True)
    logger.success("Código formatado com sucesso!")


@task
def lint(c):
    """Executa verificação de tipos com mypy"""
    logger.info("Executando mypy...")
    result = subprocess.run(["poetry", "run", "mypy", "src/"])
    if result.returncode == 0:
        logger.success("Verificação de tipos aprovada!")
    else:
        logger.error("Falha na verificação de tipos!")
        sys.exit(1)


@task
def check(c):
    """Executa todas as verificações: formatação e lint"""
    format(c)
    lint(c)


@task
def ingest(c):
    """Executa ingestão de PDF"""
    logger.info("Executando ingestão de PDF...")
    subprocess.run(["poetry", "run", "python", "src/ingest.py"], check=True)


@task
def chat(c):
    """Inicia interface de chat"""
    logger.info("Iniciando interface de chat...")
    subprocess.run(["poetry", "run", "python", "src/chat.py"], check=True)


@task
def search(c, question=None):
    """Executa busca com pergunta opcional"""
    cmd = ["poetry", "run", "python", "src/search.py"]
    if question:
        cmd.extend(["--question", question])
    logger.info(f"Executando busca: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
