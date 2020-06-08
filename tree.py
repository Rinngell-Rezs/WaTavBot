"""│├└░"""

tb = "⠀"

def tree(array,level = 0,eopb = False,HTML = False):
    row = ""

    if(level == 0):
        row += "│"

    if(eopb):
        pbs = ((level-1)*"│")+"⠀"
    else:
        pbs = level*"│"

    if(type(array) == dict):
        for key in array.keys() :
            if(key == list(array.keys())[-1]):
                branch = "└"
                eopb = True
            elif(key in list(array.keys())):
                branch = "├"
                eopb = False
            else:
                branch = "⠀"

            if(type(array[key]) not in [list,tuple,dict]):
                if(HTML == True):
                    row += "\n"+pbs+branch+"{}: <code>{}</code>".format(key,array[key])
                else:
                    row += "\n"+pbs+branch+"{}: {}".format(key,array[key])
            else:
                row += "\n"+pbs+branch+"{}:".format(key)
                row += tree(array[key],level+1,eopb,HTML)

    elif(type(array) in [list,tuple]):
        for key in array:

            if(key == array[-1]):
                branch = "└"
                eopb = True
            elif(key in array):
                branch = "├"
                eopb = False
            else:
                branch = "⠀"


            if(type(key) not in [list,tuple,dict]):
                if(HTML == True):
                    row += "\n"+pbs+branch+"<code>"+str(key)+"</code>"
                else:
                    row += "\n"+pbs+branch+str(key)
            else:
                row += "\n"+pbs+branch+"{}:".format(array.index(key))
                row += tree(key,level+1,eopb,HTML)

    else:
        return str(array)
    if(row == "│"):
        return("[Vacío]")
    return str(row)

if __name__ == "__main__":
    """array = {"chat": {
        "_": "pyrogram:Chat",
        "id": 408101137,
        "type": "private",
        "username": "chtwrsbot",
        "first_name": "Chat Wars",
        "photo": {
            "_": "pyrogram:ChatPhoto",
            "small_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABDWcZakiHvx8aKoAAgI",
            "big_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABANCIob9AaCNaqoAAgI"
        }
    }}"""
    array = {
        "_": "pyrogram:Message",
        "message_id": 1554,
        "date": 1533644960,
        "chat": {
            "_": "pyrogram:Chat",
            "id": 408101137,
            "type": "private",
            "username": "chtwrsbot",
            "first_name": "Chat Wars",
            "photo": {
                "_": "pyrogram:ChatPhoto",
                "small_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABDWcZakiHvx8aKoAAgI",
                "big_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABANCIob9AaCNaqoAAgI"
            }
        },
        "from_user": {
            "_": "pyrogram:User",
            "id": 408101137,
            "is_bot": True,
            "first_name": "Chat Wars",
            "username": "chtwrsbot",
            "photo": {
                "_": "pyrogram:ChatPhoto",
                "small_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABDWcZakiHvx8aKoAAgI",
                "big_file_id": "AQADAgADq6cxGxEhUxgACLTYDw4ABANCIob9AaCNaqoAAgI"
            }
        },
        "text": "Feeling an unsatisfiable lust for violence you set off to the nearest village. You will reach the nearest one in 2 minutes",
        "entities": [
            {
                "_": "pyrogram:MessageEntity",
                "type": "bold",
                "offset": 113,
                "length": 9
            }
        ],
        "outgoing": False,
        "reply_markup": {
            "_": "pyrogram:ReplyKeyboardMarkup",
            "keyboard": [
                [
                    "Attack",
                    "Defend",
                    "Quests"
                ],
                [
                    "Me",
                    "Castle",
                    "_"
                ]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False,
            "selective": False
        }
    }
    print(tree(array,HTML=False))
    input()
