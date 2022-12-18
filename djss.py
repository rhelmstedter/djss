import csv
import os
from collections import namedtuple
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt, Prompt

import plotly.graph_objects as go
import plotly.offline as pyo

MALE_STANDARDS: dict[str, Path] = {
    "push": Path("./standards/male_push.csv"),
    "pull": Path("./standards/male_pull.csv"),
    "hinge": Path("./standards/male_hinge.csv"),
    "squat": Path("./standards/male_squat.csv"),
}
FEMALE_STANDARDS: dict[str, Path] = {
    "push": Path("./standards/female_push.csv"),
    "pull": Path("./standards/female_pull.csv"),
    "hinge": Path("./standards/female_hinge.csv"),
    "squat": Path("./standards/female_squat.csv"),
}

COLUMNS = ["level", "movement", "load", "reps"]
Level = namedtuple("Level", COLUMNS)


def main():
    sex = Prompt.ask("Are you male or female?", choices=["male", "female"])
    if sex == "male":
        standards = MALE_STANDARDS
    else:
        standards = FEMALE_STANDARDS
    user_levels = []
    for movement in standards.keys():
        get_level(standards, movement, user_levels)
        os.system("clear")
    plotter(user_levels)


def build_movement_tuples(standards_path: Path) -> list[Level]:
    levels = []
    with open(standards_path) as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=COLUMNS)
        for row in reader:
            levels.append(Level(**row))
    return levels


def get_level(standards: dict, movement: str, user_levels: list) -> None:
    levels = build_movement_tuples(standards[movement])
    console = Console()
    table = Table(title=f"{movement.title()} Standards")
    for column in COLUMNS:
        table.add_column(column.title(), justify="center")

    for level in levels:
        table.add_row(
            level.level,
            level.movement,
            level.load,
            f"{level.reps:0>2}",
        )
    console.print(table)
    user_levels.append(IntPrompt.ask(f"Enter your level for the {movement}"))


def plotter(user_levels: list) -> None:
    movements = [*list(MALE_STANDARDS.keys()), list(MALE_STANDARDS.keys())[0]]
    user_levels = [*user_levels, user_levels[0]]
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=[7, 7, 7, 7],
                theta=movements,
                fill="none",
                name="Strength standards",
                dr=1,
                opacity=0,
            ),
            go.Scatterpolar(
                r=user_levels,
                theta=movements,
                fill="toself",
                name="Strength Levels",
                dr=1,
                marker={"color": "#2186EB"},
            ),
        ],
        layout=go.Layout(
            title=go.layout.Title(text="Dan John's Strength Standards"),
            polar={"radialaxis": {"visible": True}},
            showlegend=False,
        ),
    )

    pyo.plot(fig)


if __name__ == "__main__":
    main()
