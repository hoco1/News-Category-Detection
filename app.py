import tkinter,nltk,pickle
from tkinter import BOTH,END
from hazm.Stemmer import Stemmer
from hazm import word_tokenize
#Pickle File
path = 'D:\\Project\\Scraping\\MehrNews\\pickle\\'
vec_file = open(path+'vectorizer.norouzi','rb')
vec = pickle.load(vec_file)
vec_file.close()

le_file = open(path+'LabelEncoder.norouzi','rb')
le = pickle.load(le_file)
le_file.close()

sgd_file = open(path+'sgdAL.norouzi','rb')
sgd = pickle.load(sgd_file)
sgd_file.close()

#Stop Words 
nltk_stopwords = nltk.corpus.stopwords.words('english')

chars   = 'D:\\Project\\Scraping\\MehrNews\\StopwordFarsi\\chars.txt'
persian = 'D:\\Project\\Scraping\\MehrNews\\StopwordFarsi\\persian.txt'

with open(persian,encoding='utf8') as stopWords_file:
    stopwords = stopWords_file.readlines()
stopwords = [str(line).replace('\n', '') for line in stopwords]
with open(chars,encoding='utf8') as stopWords_file:
    stopwords = stopWords_file.readlines()
chars = [str(line).replace('\n', '') for line in stopwords]

nltk_stopwords.extend(stopwords)
nltk_stopwords.extend(chars)

#Style
input_color  = "#2a4494"
output_color = "#4ea5d9"
root_color = "#123456"

#Define Window
root = tkinter.Tk()
root.title('News Category Detection (Farsi)')
root.iconbitmap('D:\\Project\\Scraping\\MehrNews\\img\\news.ico')
root.geometry('700x600')
root.resizable(0,0)
root.config(bg=root_color)

#Define Function
def label_detection(count):
    global value_count
    stemmer = Stemmer()
    news = text_entry.get('1.0',END)

    tokenized = word_tokenize(news)
    tokenized_filtered = [w for w in tokenized if not w in nltk_stopwords]
    tokenized_filtered_stemming = [stemmer.stem(w) for w in tokenized_filtered]
    news_preprocess = [' '.join(tokenized_filtered_stemming)]

    x_v = vec.transform(news_preprocess)

    temp = str(count)+' : '+str(le.inverse_transform(sgd.predict(x_v)))
    my_listbox.insert(END,temp)
    
    value_count = count + 1
    text_entry.delete('1.0', END)

#Define Frames
input_frame = tkinter.LabelFrame(root,bg=input_color,text='MohammadReza Norouzi',fg='white')
output_frame = tkinter.LabelFrame(root,bg=output_color,text='Output Frame')
input_frame.pack(padx=10)
output_frame.pack(padx=10,pady=(0,10),fill=BOTH,expand=True)


def make_menu(w):
    global the_menu
    the_menu = tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)



#Input Frame
text_entry = tkinter.Text(input_frame,height=15)
text_entry.grid(row=0,column=0,padx=5,pady=5)

value_count = 0
cal_btn = tkinter.Button(input_frame,text='Category Detection',command=lambda:label_detection(value_count))
cal_btn.grid(row=1,column=0,padx=5,pady=5,sticky='WE')

make_menu(input_frame)
text_entry.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

#Output Frame
my_scrollbar = tkinter.Scrollbar(output_frame)
my_listbox = tkinter.Listbox(output_frame,height=15,width=108,borderwidth=3,yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)
my_listbox.grid(row=0,column=0,pady=5)
my_scrollbar.grid(row=0,column=1,sticky='NS')

root.mainloop()