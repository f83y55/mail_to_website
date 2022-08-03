import os
import re

def empty_line(st:str):
    """Show if a line only contains tabs and spaces, ie is blank"""
    spaces, tabs = st.count(" "), st.count("\t")
    return st[-1] == "\n" and len(st) == spaces + tabs + 1

def text_to_data(filename:str):
    """Text file to [ [..., ...]:lines ]:parag conversion"""
    data = []
    with open(filename) as file:
        lines = file.readlines()
        parag = []
        for line in lines :
            if empty_line(line) :
                if parag :
                    data.append(parag)
                parag = []
            else :
                parag.append(line.strip())
        data.append(parag)
    return data

def data_to_html(data:list):
    spaces = 4
    html = ""
    for parag in data :
        html += f"<p>\n{spaces*' '}" + f"<br>\n{spaces*' '}".join(parag) + "\n</p>\n\n"
    return html

def text_to_html(filename:str):
    """Text file to html"""
    spaces = 4
    html = ""
    with open(filename) as file:
        lines = file.readlines()
        parag = []
        for line in lines :
            if empty_line(line) :
                if parag :
                    html += f"<p>\n{spaces*' '}" + f" <br>\n{spaces*' '}".join(parag) + "\n</p>\n\n"
                parag = []
            else :
                parag.append(line.strip())
        html += f"<p>\n{spaces*' '}" + f" <br>\n{spaces*' '}".join(parag) + "\n</p>\n\n"
    return html

def html_to_file(filename:str, content:str):
    """html to text file"""
    with open(filename+".html", "w") as file:
        file.write(content)


if __name__ == "__main__":
    filename = "test.txt"
    html_to_file(filename, text_to_html(filename))

