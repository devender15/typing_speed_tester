from datetime import datetime
from time import sleep
from tkinter import*
import tkinter.messagebox as tmsg
import threading

# Global variables for stopwatch
counter = 66600
running = False
time_took = ""

def start_timer(label):
	global running
	global timer_frame
	global start_btn
	global type_box

	# disabling the start button if once pressed, so that it can't be clicked twice
	start_btn['state'] = 'disabled'	

	# enabling the entry widget
	type_box['state'] = 'normal'

	running = True	

	counter_label(label)

def counter_label(label):
	def count():
		global time_took

		display = ""
		time_took = ""

		if(running):

			global counter

			# to manage the initial delay
			if(counter==66600):
				print("")

			else:
				tt = datetime.fromtimestamp(counter)
				string = tt.strftime("%H:%M:%S")
				time_took = tt.strftime("%S")
				display = string

			label['text'] = display

			label.after(1000, count)
			counter += 1
			
	# trigerring the start of the count function
	count()

# using thread to start the checking function
def start(e):
	global type_box

	t1 = threading.Thread(target=check)
	t1.start()

	# after submission of the answer, box should be disabled again
	type_box['state'] = 'disabled'


def next_level(label):
	global para_text
	global file_arr
	global score_frame
	global start_btn
	global counter
	counter = 66600

	# reseting the timer
	label['text'] = '00:00:00'

	# finding the index of the printed line
	index = file_arr.index(para_text['text'])

	# enabling the start button, so that it can be pressed
	start_btn['state'] = 'normal'	

	# checking that, the visible line is in our line array or not. And if so, then by incrementing the index, we will get the next line.
	for got in range(len(file_arr)):
		if(para_text['text']==file_arr[got]):
			try:
				para_text['text'] = file_arr[index+1]
			except Exception as e:
				tmsg.showinfo("Finished!", "You have completed all levels!")

	# clearing our score frame by deleting all the widgets which are in this frame
	for widget in score_frame.winfo_children():
		widget.destroy()

def check():
	global file_arr
	global typ
	global para_text
	global score_frame
	global running
	
	# making running false because it will then change the condition and timer will get stop
	running = False

	# splitting the user-entered line, to get the no of words
	words_arr = typ.get().split()
	time_taken = time_took
	speed = round(len(words_arr) * 60/int(time_taken))


	for matched in range(len(file_arr)):

		# making both to lowercase because if your typed any of the character in lower or upper case but still the line is same then he/she shouldn't get the error
		if(typ.get().lower()==file_arr[matched].lower()):
			Label(score_frame, text=f"Speed: {speed} wpm !", font='Corbel 15 bold', bg='blue').pack()
			Label(score_frame, text=f"Time Taken: {time_taken} seconds", font='Corbel 15 bold', bg='blue').pack()
			typ.set("")

def window():

	global file_arr
	global typ
	global para_text
	global score_frame
	global timer_frame
	global start_btn
	global type_box	


	# customizing window
	root = Tk()
	root.title("Typing GrandMaster")
	root.geometry("500x500")
	root.resizable(0,0)

	# creating frames
	header_frame = Frame(root, bg='red', height=50)
	header_frame.pack(fill=X)

	paragraph_frame = Frame(root, bg='green', height=120, pady=20)
	paragraph_frame.pack(fill=X)

	inp_frame = Frame(root, bg='pink', height=100, bd=3, relief=GROOVE)
	inp_frame.pack(fill=X)

	score_frame = Frame(root, bg='blue', height=100, bd=5, relief=SUNKEN)
	score_frame.pack(fill=X)

	timer_frame = Frame(root, bg='gray', height=100, bd=5, relief=SUNKEN)
	timer_frame.pack(fill=X)

	footer_frame = Frame(root, bg='white', height=50, bd=5, relief=SUNKEN)
	footer_frame.pack(fill=X)

	# making labels
	Label(header_frame, text='Typing GrandMaster', font='lucida 25 bold', fg='blue', bg='red').pack()

	timer_label  = Label(timer_frame, text="00:00:00", font='Corbel 25 bold', bg='gray')
	timer_label.pack()


	# creating buttons
	start_btn = Button(footer_frame, text="Start > ", bg='red', command=lambda: start_timer(timer_label), height=4)
	start_btn.pack(fill=X)

	next_btn = Button(footer_frame, text="Next > ", bg='Green', command=lambda: next_level(timer_label), fg='white', height=3)
	next_btn.pack(fill=X)

	exit_btn = Button(footer_frame, text="Exit", bg='pink', fg='blue', command=lambda: root.destroy(), height=3)
	exit_btn.pack(fill=X)

	# importing all the lines from a text file to show on the screen
	with open("paragraphs.txt", "r") as f:
		file = f.read()
		file_arr = file.split("\n")

	# printing line which user have to type
	para_text = Label(paragraph_frame, text=file_arr[0], font="Corbel 15 italic")
	para_text.pack()

	# making the entry field for typing
	typ = StringVar()
	type_box = Entry(inp_frame, state='disabled', textvar=typ, width=60, bg='white', fg='black', justify=CENTER, font='lucida 18 bold')
	type_box.pack()

	# when user press enter key, then start function will be called
	root.bind("<Return>", start)

	root.mainloop()

if __name__ == '__main__':
	window()