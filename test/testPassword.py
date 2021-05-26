import base64

if __name__ == "__main__":
    password = "olivier"
    encode_text = base64.b64encode(bytearray(password + "salage" + password, "utf8") )
    print(encode_text)
    
    cryptedpassword = encode_text.decode("utf-8") 
    totalpassword = str(base64.b64decode(bytearray(cryptedpassword, "utf8")), "utf8")
    password = totalpassword[:int((len(totalpassword) - 6) / 2)]
    print(password)
