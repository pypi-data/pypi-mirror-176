import typer
import openai
import json
import importlib.resources
import pathlib
import sys
from typing import Any

PACKAGEDIR = pathlib.Path(__file__).parent.absolute()
app = typer.Typer()


def read_config():
    with open(PACKAGEDIR / "config.json") as f:
        config = json.load(f)
        return config


def write_config(config_dict):
    config = read_config()
    config.update(config_dict)
    with open(PACKAGEDIR / "config.json", "w") as f:
        json.dump(config, f)
        return config


@app.command()
def config():
    config = read_config()
    typer.echo(config)


@app.command()
def api(api_key: str):
    config = read_config()
    config["api_key"] = api_key
    write_config(config)
    print(config)
    typer.echo(f"API key {api_key} saved")


@app.command()
def temp(temperature: float):
    config = read_config()
    config["temperature"] = temperature
    write_config(config)
    print(config)
    typer.echo(f"Temperature {temperature} saved")


@app.command()
def tokens(tokens: int):
    config = read_config()
    config["max_tokens"] = tokens
    write_config(config)
    print(config)
    typer.echo(f"Tokens {tokens} saved")


@app.command()
def it(
    question: Any,
):
    """
    Welcome to ASK it, set your api with command "ask api "your open api key here".
    Then ask questions with "ask it "your question here?"
    Make sure to finish the question with a question mark.
    """
    config = read_config()
    if config["api_key"] == "":
        typer.echo("Please set your API key with command ask api")
        raise typer.Exit(1)
    else:
        openai.api_key = config["api_key"]
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=question,
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
        )
        typer.echo(response["choices"][0]["text"])


if __name__ == "__main__":
    app()
