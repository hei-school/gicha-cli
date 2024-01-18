from rich.console import Console
from rich.theme import Theme

theme = Theme({"title": "bold green", "banner": "reverse", "warn": "bold red"})
console = Console(theme=theme)


def print_banner(str):
    console.print("\n" + str, style="banner")


def print_title(str):
    console.print("\n" + str, style="title")


def print_warn(str):
    console.print("\n" + str, style="warn")


def print_normal(str):
    console.print(str)
