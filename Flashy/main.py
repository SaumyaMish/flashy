from tkinter import *
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

# -------------------Data setup-------------------#

current_record={}
to_learn={}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
    # raise exception if file is empty
    if data.empty:
        raise pandas.errors.EmptyDataError("Empty file")

except (FileNotFoundError,pandas.errors.EmptyDataError):
    data = pandas.read_csv("data/french_words.csv")
    to_learn= data.to_dict(orient="records")

else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_record,flip_timer
    window.after_cancel(flip_timer)
    current_record = random.choice(to_learn)
    canvas.itemconfig(card_title, text ='French',fill="black")
    canvas.itemconfig(card_word, text =current_record["French"],fill="black")
    canvas.itemconfig(card_background,image= white_img)
    flip_timer = window.after(3000, func=card_flip)


def card_flip():
    global current_record
    canvas.itemconfig(card_background,image= blue_img)
    canvas.itemconfig(card_title, text='English',fill= "White")
    canvas.itemconfig(card_word, text= current_record["English"],fill= "White")

def is_known():
    to_learn.remove(current_record)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index= False)
    next_card()



# -------------------gui setup-------------------#

window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50,background=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=card_flip)

# Canvas setup
canvas = Canvas(width=800,height=526,background=BACKGROUND_COLOR)

# Front card image set
white_img = PhotoImage(file="images/card_front.png")
card_background = canvas.create_image(400,263,image=white_img)

# Back card image set
blue_img = PhotoImage(file="images/card_back.png")


# Add text on card
card_title = canvas.create_text(400,150 ,text="",font=('Ariel',40,'italic'))
card_word = canvas.create_text(400,263,text="",font=('Ariel',60,'bold'))
canvas.config(highlightthickness=0)
canvas.grid(column=0,row=0,columnspan=2)

# Cross Button
cross_img = PhotoImage(file="images/wrong.png")
cross_btn= Button(image=cross_img,highlightthickness=0,borderwidth=0,command=next_card)
cross_btn.grid(row=1,column=0)

# right Button
right_img = PhotoImage(file="images/right.png")
right_btn= Button(image=right_img,highlightthickness=0,borderwidth=0,command=is_known)
right_btn.grid(row=1,column=1)

next_card()

window.mainloop()