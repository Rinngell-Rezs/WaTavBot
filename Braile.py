
braile = {
            'a':'⠁','1':'⠼⠁','á':'⠷',
            'b':'⠃','2':'⠼⠃',
            'c':'⠉','3':'⠼⠉',
            'd':'⠙','4':'⠼⠙',
            'e':'⠑','5':'⠼⠑','é':'⠮',
            'f':'⠋','6':'⠼⠋',
            'g':'⠛','7':'⠼⠛',
            'h':'⠓','8':'⠼⠓',
            'i':'⠊','9':'⠼⠊','í':'⠌',
            'j':'⠚','0':'⠼⠚',
            'k':'⠅',
            'l':'⠇',
            'm':'⠍',
            'n':'⠝',
            'ñ':'⠻',
            'o':'⠕','ó':'⠬',
            'p':'⠏',
            'q':'⠟',
            'r':'⠗',
            's':'⠎',
            't':'⠞',
            'u':'⠥','ú':'⠳',
            'v':'⠧',
            'w':'⠺',
            'x':'⠭',
            'y':'⠽',
            'z':'⠵',
            '?':'⠢','!':'⠖',
            '.':'⠄',':':'⠒',
            ',':'⠂',';':'⠆',
            '"':'⠦','\'':'⠦',
            '(':'⠣',')':'⠜',
            '-':'⠤',
            ' ':' ',
            '#':'⠼',
            'MAYUS':'⠨'
        }
MAYUS = ['R','T','Y','U','I','O','P','P','A','S','D','F','G','H','J','K','L','Ñ','Z','X','C','V','B','N','M']

def toBraile(txt):
    global MAYUS
    braile_txt = ""
    for l in txt:
        add = ""
        try:
            if(l in MAYUS):
                add += braile['MAYUS']
            add += braile[l.lower()]
            braile_txt += add
        except KeyError:
            braile_txt += l

    return braile_txt

if __name__ == "__main__":
    txt = input("Por favor, ingrese texto :y\n\n")
    print(toBraile(txt))
    input()
