from random import choice, shuffle
from time import sleep
from PyQt5.QtWidgets import QApplication

from main_window import *
from menu_window import *

class Question():
    def __init__ (self, question, answer, wrong_ans1, wrong_ans2, wrong_ans3):
        self.question = question
        self.answer = answer
        self.wrong_ans1 = wrong_ans1
        self.wrong_ans2 = wrong_ans2
        self.wrong_ans3 = wrong_ans3
        self.isAsking = True
        self.count_ask = 0
        self.count_right = 0
    def got_right(self):
        self.count_ask += 1
        self.count_right += 1
    def got_wrong(self):
        self.count_ask += 1

q1 = Question('Яблуко', 'apple', 'application', 'pineapple', 'apply')
q2 = Question('Дім', 'house', 'horse', 'hurry', 'hour')
q3 = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')
q4 = Question('Число', 'number', 'digit', 'intager', 'amount')

radio_buttons = [rb_ans1, rb_ans2, rb_ans3, rb_ans4]
questions = [q1, q2, q3, q4]

def new_question():
    global cur_q
    cur_q = choice(questions)
    lb_question.setText(cur_q.question)
    lb_right_answer.setText(cur_q.answer)
    shuffle(radio_buttons)
    radio_buttons[0].setText(cur_q.wrong_ans1)
    radio_buttons[1].setText(cur_q.wrong_ans2)
    radio_buttons[2].setText(cur_q.wrong_ans3)
    radio_buttons[3].setText(cur_q.answer)

new_question()

def check():
    RadioGroup.setExclusive(False)
    for answer in radio_buttons:
        if answer.isChecked():
            if answer.text() == lb_right_answer.text():
                cur_q.got_right()
                lb_result.setText('Вірно!')
                answer.setChecked(False)
                break
    else:
        lb_result.setText('Не вірно!')
        cur_q.got_wrong()
    
    for answer in radio_buttons:
        answer.setChecked(False)
        RadioGroup.setExclusive(True)

def click_ok():
    if btn_next.text() == "Відповісти":
        check()
        gb_question.hide()
        gb_answer.show()
        btn_next.setText('Наступне запитання')

    else:
        new_question()
        gb_answer.hide()
        gb_question.show()
        btn_next.setText('Відповісти')
btn_next.clicked.connect(click_ok)

def rest():
    window.hide()
    n = sp_rest.value() * 60
    sleep(n)
    window.show()

btn_rest.clicked.connect(rest)


def open_menu():
    total_ask = sum(q.count_ask for q in questions)
    total_right = sum(q.count_right for q in questions)

    if total_ask == 0:
        c = 0
    else:
        c = (total_right / total_ask) * 100
    text = f'Разів відповіли: {total_ask}\n' \
           f'Вірних відповідей: {total_right}\n' \
           f'Успішність: {round(c, 2)}%'
    lb_statistic.setText(text)
    menu_win.show()
    window.hide()

btn_menu.clicked.connect(open_menu)

def back_menu():
    menu_win.hide()
    window.show()
btn_back.clicked.connect(back_menu)

def clear():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()

btn_clear.clicked.connect(clear)

def add_question():
    new_q = Question(le_question.text(), le_right_ans.text(), le_wrong_ans1.text(), le_wrong_ans2.text(), le_wrong_ans3.text())
    questions.append(new_q)
    clear()
btn_add_question.clicked.connect(add_question)


window.show()
app.exec_()