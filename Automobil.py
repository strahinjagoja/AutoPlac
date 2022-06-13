import json
class Automobil:
    staticni_podatak="podatak klase"
    def __init__(self, marka, model, godiste, cena):
        self.marka = marka
        self.model = model
        self.godiste = godiste
        self.cena = cena
    def to_json(self):
        return json.dumps(self.__dict__)
    def __str__(self):
        return self.marka+" "+self.model+ " " + self.godiste + " " + self.cena
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)
    @staticmethod
    def f(arg):
        print(Automobil.staticni_podatak+arg); #moze i ovo ali je vise za g.fun
        return

zapr='{"bla": "da"}'
Automobil1 = json.loads(zapr)
print(type(Automobil1))