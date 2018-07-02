from random import randint

class Agent:
    def __init__(self):
        self.str, self.dex, self.con, self.int, self.wis, self.cha = 10,10,10,10,10,10
        self.proficiencies = None

class Item:
    pass

class Proficiencies:
    pass

class Condition:
    pass

class Die:
    dice = {4,6,8,10,12,20,100}
    def __init__(self,number):
        self.lower = 1
        self.upper = 20
        if number not in Die.dice:
            raise ValueError("{} is not a valid dice number.".format(number))
        else:
            self.upper = number

    def roll(self):
        return randint(self.lower,self.upper)

    def __str__(self):
        return "d{}".format(self.upper)

class DK:
    def __init__(self,drop=False,keep=False,highest=False,lowest=False,amount=0,die=None):
        self.drop = drop
        self.keep = keep
        self.highest = highest
        self.lowest = lowest
        self.amount = amount
        self.die = die

class Roll:
    def __init__(self, die=Die(20), mod=0, dk=None):
        if not isinstance(die, Die):
            raise TypeError("Roll die takes a Die object")
        self.die = die
        self.mod = mod
        if dk is not None and not isinstance(dk, DK):
            raise TypeError("Roll dk takes a DK object")
        self.dk = dk

    def roll(self):
        if self.dk is None:
            if isinstance(self.mod, Roll) or isinstance(self.mod, Die):
                return self.die.roll()+self.mod.roll()
            else:
                return self.die.roll()+self.mod
        else:
            if isinstance(self.mod, Roll) or isinstance(self.mod, Die):
                return [self.die.roll()].append(self.mod.roll())
            else:
                return 0


    def __str__(self):
        if self.mod == 0:
            return str(self.die)
        else:
            return "{}+{}".format(self.die,self.mod)

print(Roll(Die(6),Roll(Die(6),Roll(Die(6)))).roll())