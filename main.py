import tkinter
import pandas
import random
import pronouncing
import playsound
import threading

from gtts import gTTS

BACKGROUND_COLOR = "#B1DDC6"
list_of_words = pandas.read_csv("data/eng-pl.csv").to_dict(orient="records")
word = {}
words_for_lvl = []
LEVEL = 1


def skip():
    window.after_cancel(timer)
    threading.Thread(target=swap_card).start()

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = f"mp3s/{text}.mp3"
    tts.save(filename)


def play(filename):
    playsound.playsound(filename)


def get_words_for_lvl():
    global words_for_lvl
    words_for_lvl = list_of_words[(LEVEL*100)-99:LEVEL*100]


def get_level():
    global LEVEL
    try:
        with open("data/progress.txt", 'r') as file:
            LEVEL = int(file.read())
            words_from_file()
    except FileNotFoundError:
        LEVEL = 1
        level_to_file()
        get_words_for_lvl()


def level_to_file():
    global LEVEL
    with open("data/progress.txt", 'w') as file:
        file.write(str(LEVEL))


def words_to_file():
    with open("data/curr_words.csv", 'w', encoding="utf-8") as file:
        file.write("english,polish\n")
        for i in words_for_lvl:
            file.write(f"{i['english']},{i['polish']}\n")


def words_from_file():
    global words_for_lvl
    words_for_lvl = pandas.read_csv("data/curr_words.csv", encoding="utf-8").to_dict(orient="records")


def approval():
    global words_for_lvl, LEVEL
    words_for_lvl = [i for i in words_for_lvl if not (i['english'] == word['english'])]
    if len(words_for_lvl) == 0:
        LEVEL += 1
        level_to_file()
        get_words_for_lvl()
    words_to_file()
    get_word()


def get_word():
    global word, timer
    word = random.choice(words_for_lvl)
    window.after_cancel(timer)
    canvas.itemconfigure(text_level, text=f"Top {LEVEL*100} the most common words", fill="black")
    canvas.itemconfigure(text_lang, text="english", fill="black")
    canvas.itemconfigure(text_word, text=word['english'], fill="black")
    canvas.itemconfigure(eng_text, text="", fill="black")
    canvas.itemconfigure(lower_text, text="", fill="black")
    canvas.itemconfigure(image, image=img_front)
    button_skip.place(x=700, y=200)
    timer = window.after(3000, swap_card)


def swap_card():
    canvas.itemconfigure(text_level, text=f"Top {LEVEL * 100} the most common words", fill="white")
    canvas.itemconfigure(text_lang, text="polish", fill="white")
    canvas.itemconfigure(text_word, text=word['polish'], fill="white")
    canvas.itemconfigure(eng_text, text=word['english'], fill="white")
    button_skip.place_forget()
    canvas.itemconfigure(lower_text, text=pronouncing.phones_for_word(word['english']), fill="white")
    canvas.itemconfigure(image, image=img_back)
    speak(word['english'])
    play(f"mp3s/{word['english']}.mp3")


window = tkinter.Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.eval('tk::PlaceWindow . center')
timer = window.after(3000, swap_card)


canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
img_back = tkinter.PhotoImage(file="images/card_back.png")
img_front = tkinter.PhotoImage(file="images/card_front.png")
image = canvas.create_image(400, 263, image=img_front)
text_lang = canvas.create_text(400, 150, text="French", fill="black", font='Ariel 40 italic')
lower_text = canvas.create_text(400, 450, text="", fill="black", font='Ariel 20 italic')
eng_text = canvas.create_text(400, 400, text="", fill="black", font='Ariel 20 italic')
text_level = canvas.create_text(400, 20, text=f"Top {LEVEL*100} the most common words", fill="black", font='Ariel 15 italic')
text_word = canvas.create_text(400, 263, text="HELLO WORLD", fill="black", font='Ariel 60 italic')
canvas.grid(column=0, row=0, columnspan=2)

my_image_wrong = tkinter.PhotoImage(file="images/wrong.png")
button_wrong = tkinter.Button(image=my_image_wrong, highlightthickness=0, borderwidth=0, command=get_word)
button_wrong.grid(column=0, row=1)

my_image_right = tkinter.PhotoImage(file="images/right.png")
button_right = tkinter.Button(image=my_image_right, highlightthickness=0, borderwidth=0, command=approval)
button_right.grid(column=1, row=1)


my_skip = tkinter.PhotoImage(file="images/next.png")
button_skip = tkinter.Button(image=my_skip, highlightthickness=0, borderwidth=0, command=skip, bg="white")
button_skip.place(x=700, y=200)

get_level()
get_word()

window.mainloop()