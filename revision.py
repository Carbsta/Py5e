from random import randint
from heapq import nlargest, nsmallest

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

class Rollable:
    pass

class Op:
    highest = nlargest
    lowest = nsmallest

class Highest(Op):
    def __init__(self):
        self.operator = Op.highest

class Lowest(Op):
    def __init__(self):
        self.operator = Op.lowest

class DK:
    def __init__(self,drop=False,keep=False,operator=None,amount=0):
        self.drop = drop
        self.keep = keep
        if not isinstance(operator, Op):
            raise TypeError("operator should be an Op object")
        self.operator = operator
        self.amount = amount
        self.rolls = []

    def evaluate(self):
        print(self.rolls)
        if self.keep:
            result = self.operator.operator(self.amount,self.rolls)
        elif self.drop:
            if isinstance(self.operator, Highest):
                return Lowest().operator(len(self.rolls)-self.amount,self.rolls)
            elif isinstance(self.operator, Lowest):
                return Highest().operator(len(self.rolls)-self.amount,self.rolls)
        self.rolls = []
        return result

class Die(Rollable):
    dice = {4,6,8,10,12,20,100}
    def __init__(self,number):
        self.lower = 1
        self.upper = 20
        if number not in Die.dice:
            raise ValueError("{} is not a valid dice number.".format(number))
        else:
            self.upper = number

    def roll(self,dk=None):
        if dk is None:
            return self._roll(dk)
        else:
            self._roll()
            return sum(dk.evaluate())

    def _roll(self,dk=None):
        roll = randint(self.lower,self.upper)
        print(roll)
        if dk is None:
            return roll
        else:
            dk.rolls.append(roll)


    def __str__(self):
        return "d{}".format(self.upper)

class Roll(Rollable):
    def __init__(self, die=Die(20), mod=0, dk=None):
        if not isinstance(die, Die):
            raise TypeError("Roll die takes a Die object")
        self.die = die
        self.mod = mod
        if dk is not None and not isinstance(dk, DK):
            raise TypeError("Roll dk takes a DK object")
        self.dk = dk

    def roll(self,dk=None):
        if self.dk is None:
            return self._roll()
        else:
            mod = self._roll(dk=self.dk)
            rolls = self.dk.evaluate()
            result = sum(rolls)
            if mod is not None:
                result += mod
            return result


    def _roll(self,dk=None):
        roll = self.die.roll()
        if dk is None:
            if isinstance(self.mod, Rollable):
                return roll+self.mod.roll()
            else:
                return roll+self.mod
        else:
            dk.rolls.append(roll)
            if isinstance(self.mod, Rollable):
                self.mod._roll(dk=dk)
            else:
                return self.mod

    def __str__(self):
        if self.mod == 0:
            return str(self.die)
        else:
            return "{}+{}".format(self.die,self.mod)

advantage = DK(keep=True,operator=Highest(),amount=1)
disadvantage = DK(keep=True,operator=Lowest(),amount=1)
dl1 = DK(drop=True,operator=Lowest(),amount=1)
d20 = Die(20)
d6 = Die(6)
roll = Roll(d20,d20,advantage)
statsRoll = Roll(d6,Roll(d6,Roll(d6,Roll(d6))),dk=dl1)
print(statsRoll.roll())