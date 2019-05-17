

class Util:

    def EmparejarDosListas(self, lista1, lista2):
        return zip(lista1, lista2)



lista1 = ["uno", "dos", "tres", "cuatro"]
lista2 = [1,2,3,4]

emparejado = Util().EmparejarDosListas(lista1, lista2)
print(emparejado)