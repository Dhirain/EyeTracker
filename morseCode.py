import re

code_dic = {
    ".-": "A",
    '-...': "B",
    "-.-.": "C",
    '-..': "D",
    '.': "E",
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '---': 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z'
}

def get_real_text(text: str):
    if text.endswith('////'):
        text = text.replace('////','')
    text = text.replace('//','/&/')
    split_text = text.split('/')
    output_word_str = ''
    for s in split_text:
        if s in code_dic.keys():
            s = code_dic.get(s)
        elif s == '&':
            s = ' '
        output_word_str = output_word_str + s

    return output_word_str

# print(get_real_text('..../..//-/...././.-././///'))

# print(".//-".split('//'))
