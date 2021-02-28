from tkinter import *
from tkinter import filedialog
from Naked.toolshed.shell import execute_js, muterun_js
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import ImageTk
import tqdm


def main(file,name):
    tess_dir = r"D:\HackerBash\AutoGrader\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = tess_dir

    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    def semantic_similarity_roberta(model,sentences):
        # sentences = ["Nishit plays badminton", "Badminton is played by Nishit"]
        sentence_embeddings = model.encode(sentences)
        li = []
        for sentence, embedding in zip(sentences, sentence_embeddings):
            print("Sentence:", sentence)
            # print("Embedding:", embedding)
            li.append(embedding)
            print("Embedding:", embedding.shape)

        dot = sum(a * b for a, b in zip(li[0], li[1]))
        norm_a = sum(a * a for a in li[0]) ** 0.5
        norm_b = sum(b * b for b in li[1]) ** 0.5

        cos_sim = dot / (norm_a * norm_b)

        print(cos_sim)

        return cos_sim


    def contents():
        with open("output.txt", "rt") as myfile:# open lorem.txt for reading text
            contents = myfile.read()         # read the entire file to string
            myfile.close()                   # close the file
            x = contents
            print(x)                 # print string contents
            y = x[36:-2]
            print(y)
            return y

    def ans_contents():
        with open("ans_output.txt", "rt") as myfile:# open lorem.txt for reading text
            contents = myfile.read()         # read the entire file to string
            myfile.close()                   # close the file
            x = contents
            print(x)                 # print string contents
            y = x[36:-2]
            print(y)
            return y

    # v = "pages/page0.jpg"
    # js_command = "node"+"test.js" + " " + v
    # result = execute_js("test.js")

    # # Store Pdf with convert_from_path function
    # images = convert_from_path(r'C:\Users\tusha\Downloads\1911050_TUSHAR_COA.pdf')

    def teacher_ans(images):
        di = {}
        for i in range(len(images)):
            images[i].save('ans_page1' + '.jpg', 'JPEG')
            result = execute_js("ans_test.js")
            di[str(i)] = ans_contents()
        return di


    def check(ans_images,images):
        li_marks =[]
        full_paper_student = ""
        full_paper_teacher = ""
        ans_key = teacher_ans(ans_images)
        for i in range(len(images)):
            try:
                li_sentences = []
                images[i].save('page1' + '.jpg', 'JPEG')
                result = execute_js("test.js")
                com2 = contents().replace('\n',' ').replace('\\n',' ').replace('\r',' ').lower()
                full_paper_student += com2
                ans_page = ans_key[str(i)].replace('\n',' ').replace('\\n',' ').replace('\r',' ').lower()
                full_paper_teacher += ans_page
                li_sentences.extend([com2,ans_page])
                print("cleaned",li_sentences)
                marks = semantic_similarity_roberta(model,li_sentences)
                li_marks.append(marks)
            except:
                pass

        final_calculations = semantic_similarity_roberta(model, [full_paper_student,full_paper_teacher])
        return li_marks,final_calculations

    def input_docs(file,name,total_marks=80):
        images_ans = convert_from_path(filename_ans)
        images = convert_from_path(file)
        interm_marks,results = check(images_ans,images)
        print("Results",results)
        print(type(results))
        print(type(total_marks))
        tot = int(results*int(total_marks))
        print(tot)
        print(type(tot))
        df = pd.DataFrame(columns=["Pages","Percentage of marks alloted"])
        col1 = [i for i in range(len(interm_marks))]
        col1.extend([np.nan,"Total Marks"])
        interm_marks.extend([np.nan,tot])
        df.Pages = col1
        df["Percentage of marks alloted"] = interm_marks
        df.to_csv(filename_out+"/" +name+"_"+"marks_Scored"+str(tot)+".csv",index=False)
        print(interm_marks,results)
        return results*total_marks,

    return input_docs(file,name)







# Function for opening the
# file explorer window

def browseFiles():
    global filename
    filename = filedialog.askdirectory(initialdir="/",
                                          title="Select a File",
                                          )

def browseFilesAnswer():
    global filename_ans

    filename_ans = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          )

def browseFilesOut():
    global filename_out

    filename_out = filedialog.askdirectory(
                                          title="Select a File",
                                          )

def run():
    for file in os.listdir(filename):
        print(file)
        print(filename+"/"+file)
        main(filename+"/"+file,file)

# button_explore = Button(window,
#                         text="Directory of targets",
#                         command=browseFiles)
# button_explore.place(x=80, y=50)
#
# button_explore1= Button(window,
#                         text="Answer Key path",
#                         command=browseFilesAnswer)
# button_explore1.place(x=80, y=90)
#
# button_explore2= Button(window,
#                         text="Directory to store Outputs",
#                         command=browseFilesOut)
# button_explore2.place(x=65, y=130)
#
# btn = Button(window,
#                      text="Run",
#                      command=run)
#
# btn.place(x=120, y=170)
# lbl=Label(window, text="Auto Grading for PDFs", fg='blue', font=("Helvetica", 12))
# lbl.place(x=60, y=10)

class Auto:
    def __init__(self,root ):
        self.root = root
        self.root.title('Auto Grader')
        self.root.geometry("915x600+100+50")
        self.bg = ImageTk.PhotoImage(file=r'D:\HackerBash\AutoGrader\im3.jpg')
        self.bg_image = Label(self.root,image = self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        frame = Frame(self.root,bg="white")
        frame.place(x=50,y=300,height= 250,width = 300)

        title = Label(frame,text="Auto Grader",font=("Impact",35,"bold"),fg= "black",bg="white").place(x=30,y=10)
        button_explore = Button(frame,
                                text="Directory of targets",
                                command=browseFiles)
        button_explore.place(x=90, y=80)

        button_explore1= Button(frame,
                                text="Answer Key path",
                                command=browseFilesAnswer)
        button_explore1.place(x=97, y=120)

        button_explore2= Button(frame,
                                text="Directory to store Outputs",
                                command=browseFilesOut)
        button_explore2.place(x=75, y=160)

        btn = Button(frame,
                             text="Run",
                             command=run)

        btn.place(x=130, y=200)


root = Tk()
obj = Auto(root)
root.mainloop()

