import os
import tkinter as tk
 
fenetre = tk.Tk()
 
photo = tk.PhotoImage(file='matcha/web/static/photo/de.png')
 
label = tk.Label(fenetre, image=photo)
label.pack()
 
fenetre.mainloop()
#os.remove('matcha/web/static/photo/pegase73.jpg')
#fichier = open("pegase.txt", "w")
#fichier.close