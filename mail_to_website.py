from imap_tools import MailBox, AND
import datetime
# $ pip install imap-tools
import os
import json
import pprint

json_pswd_filename = "pswd.json"
json_team_filename = "team.json"
site_foldername = "site"
publi_foldername = "publi"



class Publi :
    def __init__(self, msg):
        self.content = {
                "title" : msg.subject,
                "authors" : [msg.from_, *msg.cc],
                "date" : str(msg.date),
                "text" : msg.text,
                "html" : msg.html,
                "filename" : valid_filename(f"{str(msg.date)[:19]} - {msg.subject}"), 
                }
 
    def to_json(self) :
        json_save(self.content, os.path.join(publi_foldername, f"{self.content['filename']}.json"))

def valid_filename(st:str="") -> str:
    st = st.replace('/', '-')
    st = st.replace(':', '-')
    return "".join(x for x in st if x.isalnum() or x in "._- ()[]")[:255]

 
def json_load(filename:str=json_pswd_filename) -> dict:
    """Read a json file containing email account information"""
    try :
        with open(filename, 'r', encoding='utf-8') as file:
            print(f"loading {filename}")
            data = json.load(file)
            if isinstance(data, dict) and "server" in data.keys() and "port" in data.keys() and "user" in data.keys() and "password" in data.keys() :
                return data
            else :
                raise NameError("Incorrect json")
    except Exception as e :
        print(f"Exception : {e} \n Trying to create a new json file {filename}")
        data = input_account_info()
        json_save(data, filename)
        return data


def json_save(data:dict, filename:str=json_pswd_filename) :
    """Save a json file containing email account information"""
    try :
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            print(f"saved as {filename}")
    except Exception as e :
        print(f"Exception : {e}")


def input_account_info() -> dict:
    """Get email account information"""
    data = {}
    data["server"] = input("Enter webmail imap server address :\n")
    data["port"] = input("Enter email imap port :\n")
    if not data["port"] :
        data["port"] = 993
    else :
        try :
            data["port"] = int(data["port"])
        except :
            data["port"] = 993
    data["user"] = input("Enter username :\n")
    data["password"] = input("Enter password :\n")
    return data

def mailbox_connect(account_data:dict={}, filename:str=json_pswd_filename):
    """Imap connexion"""
    if not account_data:
        account_data = json_load(filename)
    # Login :
    mb = MailBox(account_data["server"]).login(account_data["user"], account_data["password"])
    return [Publi(msg) for msg in mb.fetch()]


def empty_line(st:str):
    """Show if a line only contains tabs and spaces, ie is blank"""
    spaces, tabs = st.count(" "), st.count("\t")
    return len(st) == spaces + tabs


def text_to_html(text:str):
    """Plain text file to html"""
    spaces = 4
    html = ""
    lines = text.split('\n')
    parag = []
    for line in lines :
        print(line)
        if empty_line(line) :
            if parag :
                html += f"<p>\n{spaces*' '}" + f" <br>\n{spaces*' '}".join(parag) + "\n</p>\n\n"
                parag = []
        else :
            parag.append(line)
    html += f"<p>\n{spaces*' '}" + f" <br>\n{spaces*' '}".join(parag) + "\n</p>\n\n"
    return html


def html_to_file(content:str, filename:str="html_out.html"):
    """html to text file"""
    with open(filename+".html", "w") as file:
        file.write(content)


if __name__ == "__main__":
    publications = mailbox_connect()
    for publi in publications :
        publi.to_json()
        print(publi.content["html"])
        
