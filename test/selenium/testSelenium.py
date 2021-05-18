from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Créer une session Firefox
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

# Appeler l’application web
driver.get("http://www.google.fr")

# Localiser la zone de texte
search_field = driver.find_element_by_id("lst-ib")
search_field.clear()

# Saisir et confirmer le mot-clé
search_field.send_keys("Mot-clé")
search_field.submit()

# Consulter la liste des résultats affichés à la suite de la recherche
# à l’aide de la méthode find_elements_by_class_name
lists= driver.find_elements_by_class_name("_Rm")

# Passer en revue tous les éléments et restituer le texte individuel

i=0
for listitem in lists:
    print (listitem.get_attribute("innerHTML"))
    i=i+1
    if(i>10):
        break

# Fermer la fenêtre du navigateur
driver.quit()
