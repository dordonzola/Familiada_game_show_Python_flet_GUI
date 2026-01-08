import flet as ft
from flet import TextField, ElevatedButton, Text, Row, Column
from playsound3 import playsound
import asyncio
import threading
import json
import random


# =======================
# Pomocnicze
# =======================

def play_sound(file):
    threading.Thread(
        target=playsound,
        args=(file,),
        daemon=True
    ).start()


# =======================
# Główna aplikacja
# =======================

async def main(page: ft.Page) -> None:
    # ---------- Dane ----------
    with open("questions.json", "r", encoding="UTF-8") as file:
        json_data = file.read()

    q_and_a = json.loads(json_data)

    teams = ["", ""]
    team_points = [0, 0]

    # ---------- Stan gry ----------
    rounds = 3
    round_num = -1

    good_answers = 0
    mistakes = 0

    current_team = 0        # kto aktualnie odpowiada
    starting_team = 0       # kto zaczyna nową rundę
    team_switched = False   # zabezpieczenie przed wielokrotną zmianą drużyny

    finish_round = False

    # ---------- Pytania ----------
    questions = list(q_and_a.keys())
    random.shuffle(questions)
    question = Text(questions[0], size=20)

    # ---------- UI: elementy ----------
    who = Text("")

    left_x = [ft.Text("X", size=50) for _ in range(3)]
    right_x = [ft.Text("X", size=50) for _ in range(3)]

    answer_texts = [
        Text(". . . . . . . . . . . . .    . . . .", size=20)
        for _ in range(5)
    ]

    # ---------- Ustawienia strony ----------
    page.title = "Familiada"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "dark"

    splash = Column(
        [Text("FAMILIADA", size=60)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=1500
    )

    # ---------- UI: nazwy drużyn ----------
    button_name = ElevatedButton(text="Zatwierdź", width=80, disabled=True)

    name1 = TextField(label="Drużyna 1", width=300)
    name2 = TextField(label="Drużyna 2", width=300)

    input_names = Column(
        [
            Row([Text("Wprowadź nazwę drużyny 1:")], alignment=ft.MainAxisAlignment.CENTER),
            Row([name1], alignment=ft.MainAxisAlignment.CENTER),
            Row([Text("Wprowadź nazwę drużyny 2:")], alignment=ft.MainAxisAlignment.CENTER),
            Row([name2], alignment=ft.MainAxisAlignment.CENTER),
            Row([button_name], alignment=ft.MainAxisAlignment.CENTER),
        ]
    )

    # ---------- UI: odpowiedzi ----------
    text_answer = TextField(label="Odpowiedź", width=300)
    button_submit = ElevatedButton(text="Zatwierdź", width=80, disabled=True)

    # =======================
    # Logika rundy
    # =======================

    def update_round():
        nonlocal round_num, good_answers, mistakes, finish_round
        nonlocal current_team, starting_team, team_switched

        team_switched = False
        round_num += 1

        if round_num <= rounds:
            question.value = questions[round_num]
        else:
            page.controls.clear()
            if team_points[0] > team_points[1]:
                text = f"Wygrywają {teams[0]}\n{team_points[0]}:{team_points[1]}"
            elif team_points[0] < team_points[1]:
                text = f"Wygrywają {teams[1]}\n{team_points[1]}:{team_points[0]}"
            else:
                text = f"Remis {team_points[0]}:{team_points[1]}!"

            page.add(
                Column(
                    [Text(text, size=40)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=1500
                )
            )
            page.update()
            return

        good_answers = 0
        mistakes = 6
        finish_round = False

        for text in answer_texts:
            text.value = ". . . . . . . . . . . . .    . . . ."

        for x in left_x + right_x:
            x.color = ft.Colors.WHITE

        current_team = starting_team
        who.value = teams[current_team]
        page.update()

    # =======================
    # Callbacki UI
    # =======================

    async def submit_names(e):
        nonlocal teams, current_team

        teams[0] = name1.value
        teams[1] = name2.value

        current_team = 0
        who.value = teams[current_team]

        page.controls.clear()
        page.add(
            Column(
                [Text(f"{teams[0]} VS {teams[1]}", size=40)],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=1500
            )
        )
        page.update()

        await asyncio.sleep(3)

        page.controls.clear()
        page.add(
            Row([who], alignment=ft.MainAxisAlignment.CENTER),
            Row([question], alignment=ft.MainAxisAlignment.CENTER),
            Row(
                [Column(left_x), Column(answer_texts), Column(right_x)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=60
            ),
            Row([text_answer, button_submit], alignment=ft.MainAxisAlignment.CENTER),
        )

        update_round()

    def validate_names(e):
        button_name.disabled = not bool(e.control.value)
        page.update()

    def validate(e):
        button_submit.disabled = not bool(e.control.value)
        page.update()

    def check_answer(e):
        nonlocal good_answers, mistakes, current_team, starting_team, team_switched

        any_correct = False
        ans_lower = text_answer.value.lower()

        if ans_lower in q_and_a[question.value]:
            good_answers += 1
            idx_map = {k: i for i, k in enumerate(q_and_a[question.value])}
            index = idx_map[ans_lower]
            points = q_and_a[question.value][ans_lower]

            team_points[current_team] += points
            answer_texts[index].value = f"{ans_lower}    {points}"
            any_correct = True
        else:
            mistakes -= 1
            if mistakes >= 3:
                left_x[5 - mistakes].color = ft.Colors.RED
            else:
                right_x[2 - mistakes].color = ft.Colors.RED

        page.update()

        playsound("correct.mp3" if any_correct else "wrong.mp3")

        if mistakes == 3 and not team_switched:
            current_team = (current_team + 1) % 2
            who.value = teams[current_team]
            team_switched = True
            page.update()
            return

        if good_answers == 5:
            starting_team = (starting_team + 1) % 2
            update_round()
        elif mistakes == 0:
            update_round()

    # =======================
    # Podpięcie zdarzeń
    # =======================

    name1.on_change = validate_names
    name2.on_change = validate_names
    button_name.on_click = submit_names

    text_answer.on_change = validate
    button_submit.on_click = check_answer

    # =======================
    # Start aplikacji
    # =======================

    page.add(splash)
    page.update()

    play_sound("intro.mp3")
    await asyncio.sleep(2)

    page.controls.clear()
    page.add(input_names)


if __name__ == "__main__":
    ft.app(target=main)
