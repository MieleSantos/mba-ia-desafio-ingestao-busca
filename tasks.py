from invoke import task
import subprocess
import sys

@task
def format(c):
    """Format code with black and isort"""
    print("Running black...")
    subprocess.run(["poetry", "run", "black", "src/"], check=True)
    print("Running isort...")
    subprocess.run(["poetry", "run", "isort", "src/"], check=True)
    print("Code formatted successfully!")

@task
def lint(c):
    """Run type checking with mypy"""
    print("Running mypy...")
    result = subprocess.run(["poetry", "run", "mypy", "src/"])
    if result.returncode == 0:
        print("Type checking passed!")
    else:
        print("Type checking failed!")
        sys.exit(1)

@task
def check(c):
    """Run all checks: format and lint"""
    format(c)
    lint(c)

@task
def ingest(c):
    """Run PDF ingestion"""
    print("Running PDF ingestion...")
    subprocess.run(["poetry", "run", "python", "src/ingest.py"], check=True)

@task
def chat(c):
    """Start chat interface"""
    print("Starting chat interface...")
    subprocess.run(["poetry", "run", "python", "src/chat.py"], check=True)

@task
def search(c, question=None):
    """Run search with optional question"""
    cmd = ["poetry", "run", "python", "src/search.py"]
    if question:
        cmd.extend(["--question", question])
    print(f"Running search: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)