import typer
import openai
import os
from pprint import pprint
from hildebert.memory import Memory

app = typer.Typer()
history = os.path.join(typer.get_app_dir("hildebert"), "history.json")
memory = Memory(history)

def main():
    typer.echo("Hello, world!")

@app.command()
def run(input: str):
    memory.add(input, "result")
    pprint(memory.get_last(3))
    
if __name__ == "__main__":
    typer.run(main)

