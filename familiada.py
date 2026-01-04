import flet as ft
from flet import TextField, ElevatedButton, Text, Row, Column
from playsound3 import playsound
import asyncio
import threading
import json
import random


def play_sound(file):
    threading.Thread(
        target=playsound,
        args=(file,),
        daemon=True
    ).start()


async def main(page: ft.Page) -> None:
    with open("questions.json", "r", encoding='UTF-8') as file:
        json_data = file.read()

    teams = ["", ""]

    who = Text("")
    q_and_a = json.loads(json_data)
    values = list(q_and_a.values())[0]
    answers = list(values.values())
    points = list(values.keys())

    # Pytania w losowej kolejnosci
    questions = list(q_and_a.keys())
    random.shuffle(questions)
    question = Text(questions[0], size=20)


    rounds = 3
    round_num = -1
    good_answers = 0
    mistakes = 0
    team_num = 0


    finish_round = False
    answers = [". . . . . . . . . . . . .    . . . ." for i in range(5)]
    left_x = [ft.Text("X", size=50) for _ in range(3)]
    right_x = [ft.Text("X", size=50) for _ in range(3)]

    page.title = "Familiada"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'dark'

    splash = ft.Column([Text("FAMILIADA", size=60)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                       width=1500
    )



    button_name = ElevatedButton(
        text="Zatwierdź",
        width=80,
        disabled=True
    )

    name1 = TextField(
        label="Drużyna 1",
        text_align=ft.TextAlign.LEFT,
        width=300
    )

    name2= TextField(
        label="Drużyna 2",
        text_align=ft.TextAlign.LEFT,
        width=300
    )

    input_names = Column(
        [
            Row(
                [Text("Wprowadź nazwę drużyny 1:")],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                [name1],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                [Text("Wprowadź nazwę drużyny 2:")],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                [name2],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            Row(
                [button_name],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ]
    )

    text_answer = TextField(
        label="Odpowiedź",
        text_align=ft.TextAlign.LEFT,
        width=300
    )

    button_submit = ElevatedButton(
        text="Zatwierdź",
        width=80,
        disabled=True
    )

    answer_texts = [Text(". . . . . . . . . . . . .    . . . .", size = 20) for _ in range(5) ]

    team_points = [0, 0]


    def update_round():
        nonlocal question, good_answers, finish_round, mistakes, round_num, answers, left_x, right_x, team_num


        round_num += 1
        if round_num <= rounds:
            question.value = questions[round_num]
        elif team_points[0] > team_points[1]:
            page.controls.clear()
            page.add(ft.Column([Text(f"Wygrywają {teams[0]}\n {team_points[0]}:{team_points[1]}", size=40)],
                               alignment=ft.MainAxisAlignment.CENTER,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               width=1500))
            page.update()
        elif team_points[0] < team_points[1]:
            page.controls.clear()
            page.add(ft.Column([Text(f"Wygrywają {teams[1]}! \n {team_points[1]}:{team_points[0]}", size=40)],
                               alignment=ft.MainAxisAlignment.CENTER,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               width=1500))
            page.update()
        else:
            page.controls.clear()
            page.add(ft.Column([Text(f"Remis {team_points[0]}:{team_points[1]}!", size=40)],
                               alignment=ft.MainAxisAlignment.CENTER,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               width=1500))
            page.update()

        good_answers = 0
        mistakes = 6
        finish_round = False

        for i in range(5):
            answer_texts[i].value = ". . . . . . . . . . . . .    . . . ."

        for i in range(3):
            left_x[i].color =ft.Colors.WHITE
            right_x[i].color =ft.Colors.WHITE

        who.value = teams[team_num]
        page.update()
        team_num = (team_num + 1) % 2


    async def submit_names(e):
        nonlocal teams, team_num

        teams[0] = name1.value
        teams[1] = name2.value
        team_num = 0
        who.value = teams[team_num]

        page.controls.clear()
        page.add(
            ft.Column(
                [Text(f"{teams[0]} VS {teams[1]}", size=40)],
                alignment=ft.MainAxisAlignment.CENTER,
                width = 1500,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
        await asyncio.sleep(3)

        page.controls.clear()

        page.add(
            Row([who], alignment=ft.MainAxisAlignment.CENTER),
            Row([question], alignment=ft.MainAxisAlignment.CENTER),
            Row(
                [
                    Column(left_x),
                    Column(answer_texts),
                    Column(right_x),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=60,
            ),
            Row([text_answer, button_submit], alignment=ft.MainAxisAlignment.CENTER),
        )
        #sztuczna zmiana druzyny
        # team_num = (team_num + 1) % 2
        update_round()
        page.update()

    def validate_names(e):
        nonlocal teams
        button_name.disabled = not bool(e.control.value)
        page.update()


    def validate(e):
        button_submit.disabled = not bool(e.control.value)
        page.update()

    def check_answer(e):
        nonlocal finish_round, good_answers, mistakes, team_points, \
            answers, questions, team_num, rounds, round_num, left_x, right_x, question


        any_correct = False
        ans_lower = text_answer.value.lower()

        if ans_lower in q_and_a[question.value]:
            good_answers += 1

            idx_map = {key: i for i, key in enumerate(q_and_a[question.value])}
            index = idx_map.get(ans_lower)
            points = q_and_a[question.value][ans_lower]
            team_points[team_num] += points

            answer_texts[index].value = ans_lower + "    " + str(points)
            any_correct = True

        elif mistakes > 3:
            left_x[6-mistakes].color =ft.Colors.RED
            mistakes -= 1
        else:
            right_x[3 - mistakes].color = ft.Colors.RED
            mistakes -= 1


        page.update()

        if any_correct:
            playsound('correct.mp3')
        else:
            playsound('wrong.mp3')

        if mistakes == 3:
            team_num = (team_num + 1) % 2
            who.value = teams[team_num]
            page.update()
            return

        if good_answers == 5 or mistakes == 0:
            update_round()

    name1.on_change = validate_names
    name2.on_change = validate_names
    button_name.on_click = submit_names
    text_answer.on_change = validate
    button_submit.on_click = check_answer



    page.add(splash)
    page.update()

    play_sound('intro.mp3')

    await asyncio.sleep(2)

    page.controls.clear()

    page.add(input_names)



if __name__ == '__main__':
    ft.app(target=main)
