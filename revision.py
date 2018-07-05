from random import randint
from heapq import nlargest, nsmallest
from typing import Union, List
from math import floor

class Ability:
    def __init__(self,base_score : int,bonuses=0,temporary=0):
        self.baseScore = base_score
        self.bonuses = bonuses
        self.temporary = temporary
        self.score = 0
        self.modifier = 0
        self.calc()

    def __str__(self):
        return "{}({:+d})".format(self.score,self.modifier)

    def calc(self):
        self.score = self.baseScore + self.bonuses + self.temporary
        self.modifier = floor((self.score - 10) / 2)

class Agent:
    def __init__(self,str=10,dex=10,con=10,int=10,wis=10,cha=10):
        self.str = Ability(str)
        self.dex = Ability(dex)
        self.con = Ability(con)
        self.int = Ability(int)
        self.wis = Ability(wis)
        self.cha = Ability(cha)
        self.stats = {"str":self.str,"dex":self.dex,"con":self.con,"int":self.int,"wis":self.wis,"cha":self.cha}

    def update(self):
        for stat in self.stats.values():
            stat.calc()

    def __str__(self):
        output = ""
        for name, stat in self.stats.items():
            output += "{} = {}, ".format(name,stat)
        output = output[:-2]
        return output

    @staticmethod
    def gen_array():
        stat_dk = DK(drop=True,operator=Lowest(),amount=1)
        stat_roll = Roll(D6,Roll(D6,Roll(D6,D6)),stat_dk)
        stats = []
        for x in range(6):
            stats.append(Ability(stat_roll.roll()))
        return stats

    @staticmethod
    def print_array(array: List[Ability]):
        print(list(map(lambda x: x.__str__(), array)))

class Item:
    pass

class Proficiencies:
    pass

class Condition:
    pass

class Rollable:
    def roll(self):
        pass

    def _roll(self,dk):
        pass

class Op:
    highest = nlargest
    lowest = nsmallest
    def __init__(self,op):
        self.operator = op

class Highest(Op):
    def __init__(self):
        super().__init__(Op.highest)

class Lowest(Op):
    def __init__(self):
        super().__init__(Op.lowest)

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
        result = 0
        if self.keep:
            result = self.operator.operator(self.amount,self.rolls)
        elif self.drop:
            if isinstance(self.operator, Highest):
                result = Lowest().operator(len(self.rolls)-self.amount,self.rolls)
            elif isinstance(self.operator, Lowest):
                result = Highest().operator(len(self.rolls)-self.amount,self.rolls)
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
        result = randint(self.lower,self.upper)
        print(result)
        if dk is None:
            return result
        else:
            dk.rolls.append(result)


    def __str__(self):
        return "d{}".format(self.upper)

class Roll(Rollable):
    def __init__(self, die=Die(20), mod: Union[int, Rollable] = 0, dk=None):
        if not isinstance(die, Die):
            raise TypeError("Roll die takes a Die object")
        self.die = die
        self.mod = mod
        if dk is not None and not isinstance(dk, DK):
            raise TypeError("Roll dk takes a DK object")
        self.dk = dk

    def roll(self):
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
        result = self.die.roll()
        if dk is None:
            if isinstance(self.mod, Rollable):
                return result+self.mod.roll()
            else:
                return result+self.mod
        else:
            dk.rolls.append(result)
            if isinstance(self.mod, Rollable):
                return self.mod._roll(dk=dk)
            else:
                return self.mod

    def __str__(self):
        if self.mod == 0:
            return str(self.die)
        else:
            return "{}+{}".format(self.die,self.mod)

##constants:
D6 = Die(6)


stats = Agent.gen_array()
Agent.print_array(stats)

