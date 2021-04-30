import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Detyra_3 import writeToFile
import pandas as pd
import tkinter.font as tkFont
from tkinter import ttk
import matplotlib
import math
from sklearn import preprocessing

from PIL import ImageTk, Image
# from pandas import DataFrame


def reset_btn_action():
    pandas_frame.grid_forget()
    label123.grid_forget()
    lbl.grid(columnspan=10, rowspan=10, column=0, row=0)


def onObjectClick(event, arg):

    # if(re.search("^.!frame.!label+[\\d]*[\\d]", str(frame.grid_slaves()[0]))):
    # if(str(frame.grid_slaves()[0]) == '.!frame.!label6' or str(frame.grid_slaves()[0]) == '.!frame.!label5'):
    # frame.grid_slaves()[0].destroy()
    label123.configure(text="Title: "+arg[2], fg="#800080", bg="cyan")
    label123.grid(row=2, column=0, columnspan=10)


def data_management(subreddit, sort_by="Hot"):
    if(subreddit == ""):
        subreddit = "Kosovo"
    if(sort_by == "Hot"):
        sort_by = ""
    doc = writeToFile(subreddit, sort_by)

    if not doc:
        # print("Error here")
        return None
    else:

        vlerat = []
        vlerat = list(doc.values())

        df = pd.DataFrame({'Title': vlerat[0], 'Author': vlerat[1],
                           'Likes': vlerat[3], '# of comments': vlerat[2]})

        return df


def go_btn_action():

    lbl.grid_forget()
    c_height = 350

    pandas_frame.delete('all')
    pandas_frame.grid(row=1, column=1, sticky="ew", padx=200, pady=100)
    # print(text_field.get("1.0", tk.END))
    reddit = text_field.get("1.0", tk.END).strip()

    sort = ((comboBox.get()).strip()).capitalize()
   # print(sort)
    if(sort == "" or sort == None):
        sort = "Hot"

    # print(sort)
    df = data_management(reddit, sort)
    try:
        if not df.empty:

            error_label.grid_forget()
            y_stretch = 1
            # print(df)

            # print(df_min)

            # gap between lower canvas edge and x axis
            y_gap = 0
            # stretch enough to get all data items in
            x_stretch = 20
            x_width = 70
            # gap between left canvas edge and y axis
            x_gap = 40

            # data2.values = list(data)
            # print(data)
            df2 = df.loc[:10, ('Title', 'Author', 'Likes', '# of comments')]

            df_min_max_scaled = df2.copy()
            df_min_max_scaled['Likes'] = (df_min_max_scaled['Likes'] - df_min_max_scaled['Likes'].min()) / (
                df_min_max_scaled['Likes'].max() - df_min_max_scaled['Likes'].min())

            z = df2['Likes'].values
            author = df2['Author'].values
            titles = df2['Title'].values
            rectangles = {}
            for x, y in enumerate(df_min_max_scaled['Likes']):
                # calculate reactangle coordinates (integers) for each bar

                x0 = (x * x_stretch + x * x_width + x_gap)
                # y0 = c_height + 0 - (y-df_min/(df_max-df_min))*y_stretch
                y0 = c_height + 0 - y*300 + y_gap*y_stretch
                # yo = y
                x1 = x * x_stretch + x * x_width + x_width + x_gap
                y1 = c_height - 20
                if(y0 > y1):
                    y0 = y1
                # draw the bar
                rect = pandas_frame.create_rectangle(
                    x0+20, y0, x1+20, y1, fill="royalblue")
                rectangles.update({x: rect})
                pandas_frame.tag_bind(rect,
                                      '<ButtonPress-1>', lambda event, args=[rect, x, titles[x]]: onObjectClick(event, args))
                # put the y value above each bar
                # print(y1, y0)
                if (y > 1000):
                    y = y/1000
                    y = str(y)+'k'
                y = str(y)

                likes = pandas_frame.create_text(
                    x0 + x_width/2, y0-5, anchor=tk.SW, text=(str(z[x]) + " likes"))
                authors = pandas_frame.create_text(
                    x0-x_gap + 30 + x_width/2, c_height+30, anchor=tk.SW, text=author[x], width=50, justify=tk.CENTER)
                pandas_frame.tag_bind(likes, '<ButtonPress-1>', lambda event,
                                      args=[rect, x, titles[x]]: onObjectClick(event, args))
                pandas_frame.tag_bind(authors, '<ButtonPress-1>', lambda event,
                                      args=[rect, x, titles[x]]: onObjectClick(event, args))

            # txt_edit.grid(row=0, column=1, sticky="w")

                # df = pd.DataFrame()

                # print(df.transpose())
                # df2 = pd.DataFrame(df.transpose, columns=doc.keys())

                # print(df)

        # def open_file():
        #     """Open a file for editing."""
        #     filepath = askopenfilename(
        #         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        #     )
        #     if not filepath:
        #         return
        #     txt_edit.delete(1.0, tk.END)
        #     with open(filepath, "r") as input_file:
        #         text = input_file.read()
        #         txt_edit.insert(tk.END, text)
        #     window.title(f"Simple Text Editor - {filepath}")
    except AttributeError:
        print("RIP")
        pandas_frame.grid_forget()
        lbl.grid(columnspan=10, rowspan=10, column=0, row=0)
        error_label.grid(row=2, column=2)


window = tk.Tk()
bg = ImageTk.PhotoImage(Image.open("reddit_logo_main.jpg"))
custom_font = tkFont.Font(family="Times New Roman", size=15)
window.title("Browse Reddit")
window.rowconfigure(0, minsize=100, weight=1)
window.columnconfigure(1, minsize=1100, weight=1)


lbl = tk.Label(window, image=bg, width=1200,
               height=700)
lbl.grid(columnspan=10, rowspan=10, column=0, row=0)


frame = tk.Frame(window, relief=tk.RAISED, bg="orange")
frame.grid(row=0, column=1, sticky="n", pady=0)


label = tk.Label(frame, height=1, text="Write subreddit: ",
                 bg="orange", font=custom_font)
label.grid(row=0, column=0, pady=10, padx=10)

label = tk.Label(frame, height=1, text="R/",
                 bg="orange", font=tkFont.Font(weight="bold"))

error_label = tk.Label(frame)
# error_label.grid(row=0, column=0)


label.grid(row=0, column=1)
text_field = tk.Text(frame, height=1, width=50, font=custom_font)
text_field.grid(row=0, column=2, padx=10, sticky="w")
text_field.insert(tk.END, "")


combobox_values = ['Hot', 'New', 'Rising', 'Top', 'Gilded']
comboBox = ttk.Combobox(frame, values=combobox_values,
                        state="readonly", font=custom_font)
comboBox.grid(row=0, column=3, padx=10, sticky="e")
c_width = 400
c_height = 350
# pandas_frame = tk.Canvas(window, relief=tk.RAISED,
#                          bg="white", width=c_width, height=c_height)

# pandas_frame.grid(row=0, column=1, sticky="ew", padx=20)


button = tk.Button(frame, text="Go!!", command=go_btn_action)
button.grid(row=0, column=4, sticky='ew', padx=10)

resetBtn = tk.Button(frame, text="Reset!", command=reset_btn_action)
resetBtn.grid(row=0, column=5, sticky='ew', padx=10)
# pandas_frame.pack()
# btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
# btn_save.grid(row=1, column=0, sticky="ew", padx=5)

# data_management("Kosovo")

error_label_txt = "Something bad happened! Perhaps you've given a non-existing subreddit"
error_label = tk.Label(frame, text=error_label_txt)
error_label.config(font=tkFont.Font(weight="bold"), fg="red")

pandas_frame = tk.Canvas(window, relief=tk.RAISED,
                         bg="white", width=c_width, height=c_height+50)

pandas_frame.grid(row=1, column=1, sticky="ew", padx=200, pady=100)

pandas_frame.grid_forget()

# window.geometry("{0}x{1}+0+0".format(
#     window.winfo_screenwidth()-3, window.winfo_screenheight()-3))
# window.attributes("-fullscreen", True)
window.configure(bg='orange')
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))

# window.resizable(False, False)
# window.attributes('-maximized', True)


label123 = tk.Label(frame, height=3, bg="orange",
                    font=tkFont.Font(weight="bold", family='Times New Roman', size=17), wraplength=1000, justify=tk.LEFT)
window.mainloop()
