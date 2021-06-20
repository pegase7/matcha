

def verif_word(word):
    dico = open('static/dico_fr.txt', 'r')
    list_dico = dico.read()
    dico.close()
    if word.lower() in list_dico:
        return True
    return False
    

def format_word(word):
    word = word.capitalize()
    return word