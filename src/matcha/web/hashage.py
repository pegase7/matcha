import hashlib

class hashit:
    def hashing(self,texte,hash_type):
        texte=texte.encode('utf-8')     
        hash_1=hashlib.new(hash_type)
        hash_1.update(texte)           
        return hash_1.hexdigest()

def hash_pwd(pwd,login):
    Hash=hashit()
    pwd=pwd+login[:2] #salage avec le 2 premieres lettres du login
    result_hash=Hash.hashing(pwd,'SHA1')
    return result_hash