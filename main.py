import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
list = pandas.read_csv("data/eng-pl.csv").to_dict(orient="records")
word = {}

# TODO: zrobic u gory napis lvl i top ile sa to najpopularnijesze slowa.
# TODO: zrrobic save your progress z zadania


try:
    with open("data/progress.txt", 'r') as file:
        LEVEL = int(file.read())
except FileNotFoundError:
    with open("data/progress.txt", 'w') as file:
        file.write("1")

def get_word():
    global word, timer
    word = random.choice(list)
    window.after_cancel(timer)
    canvas.itemconfigure(text_lang, text="english", fill="black")
    canvas.itemconfigure(text_word, text=word['english'], fill="black")
    canvas.itemconfigure(image, image=img_front)
    timer = window.after(3000, swap_card)

def swap_card():
    canvas.itemconfigure(text_lang, text="polish", fill="white")
    canvas.itemconfigure(text_word, text=word['polish'], fill="white")
    canvas.itemconfigure(image, image=img_back)

window = tkinter.Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.eval('tk::PlaceWindow . center')
timer = window.after(3000, swap_card)

canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
img_back = tkinter.PhotoImage(file="images/card_back.png")
img_front = tkinter.PhotoImage(file="images/card_front.png")
image = canvas.create_image(400, 263, image=img_front)
text_lang= canvas.create_text(400, 150, text="French", fill="black", font=('Ariel 40 italic'))
text_word = canvas.create_text(400, 263, text="HELLO WORLD", fill="black", font=('Ariel 60 italic'))
canvas.grid(column=0, row=0, columnspan=2)

my_image_wrong = tkinter.PhotoImage(file="images/wrong.png")
button_wrong = tkinter.Button(image=my_image_wrong, highlightthickness=0, borderwidth=0, command=get_word)
button_wrong.grid(column=0, row=1)

my_image_right = tkinter.PhotoImage(file="images/right.png")
button_right = tkinter.Button(image=my_image_right, highlightthickness=0, borderwidth=0, command=get_word)
button_right.grid(column=1, row=1)
get_word()

window.mainloop()