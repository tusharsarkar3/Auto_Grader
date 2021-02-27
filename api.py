from Naked.toolshed.shell import execute_js, muterun_js
import execjs
import os
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
import numpy as np
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
    ans_key = teacher_ans(ans_images)
    for i in range(len(images)):
        li_sentences = []
        images[i].save('page1' + '.jpg', 'JPEG')
        result = execute_js("test.js")
        com2 = contents()
        ans_page = ans_key[str(i)]
        li_sentences.extend([com2,ans_page])
        marks = semantic_similarity_roberta(model,li_sentences)
        li_marks.append(marks)
    return li_marks

def input_docs():
    images_ans = convert_from_path(r'C:\Users\tusha\Downloads\1911050_TUSHAR_COA.pdf')
    images = convert_from_path(r'C:\Users\tusha\Downloads\1911050_TUSHAR_COA.pdf')
    x = check(images_ans,images)
    print(x)

if __name__ == "__main__":
    input_docs()




# for i in os.listdir("pages"):
#     with open("imageName.txt","w") as f:
#         f.write(str(i))
#     break

# result = execute_js("test.js")

# def answer_key():
#     pass
#
# file = input("Enter address of pdf")

