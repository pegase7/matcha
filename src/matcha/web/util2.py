

def verif_word(word):
    dicofr = open('static/dictionaries/dico_fr.txt', 'r')
    dicoen = open("static/dictionaries/dico_en.txt", 'r')
    dicocode = open("static/dictionaries/dico_codes.txt", 'r')
    dico_fr = dicofr.read()
    dico_en = dicoen.read()
    dico_code = dicocode.read()
    dicofr.close()
    dicoen.close()
    dicocode.close()
    if (word.lower() in dico_fr) or (word.lower() in dico_en) or (word.capitalize() in dico_code): 
        return True
    return False
    

def format_word(word):
    word = word.capitalize()
    return word