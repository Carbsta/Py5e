from random import randint
from heapq import nlargest, nsmallest
from typing import Union, List, Dict
from math import floor
from dataclasses import dataclass, field

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

class DamageType:
    pass

class Poison(DamageType):
    pass

class Psychic(DamageType):
    pass

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
    def __init__(self,str=10,dex=10,con=10,int=10,wis=10,cha=10,
                 stat_dictionary: Union[Dict[str, Ability],None] = None,stat_array: Union[List[Ability],None] = None):
        if stat_dictionary is not None:
            self.str = stat_dictionary["str"]
            self.dex = stat_dictionary["dex"]
            self.con = stat_dictionary["con"]
            self.int = stat_dictionary["int"]
            self.wis = stat_dictionary["wis"]
            self.cha = stat_dictionary["cha"]
        elif stat_array is not None:
            self.str = stat_array[0]
            self.dex = stat_array[1]
            self.con = stat_array[2]
            self.int = stat_array[3]
            self.wis = stat_array[4]
            self.cha = stat_array[5]
        else:
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

    def get_stats_dict(self):
        return self.stats

    @staticmethod
    def gen_array():
        stat_dk = DK(drop=True,operator=Lowest(),amount=1)
        stat_roll = Roll(D6,Roll(D6,Roll(D6,D6)),stat_dk)
        stat_array = []
        for x in range(6):
            stat_array.append(Ability(stat_roll.roll()))
        return stat_array

    @staticmethod
    def print_array(array: List[Ability]):
        print(list(map(lambda x: x.__str__(), array)))

@dataclass
class Object:
    substance: str
    armour_class: int
    hit_points: Roll
    immunities: list = field(default_factory=list)
    vulnerabilities: list = field(default_factory=list)

class Name:
    def __init__(self,name,plural=None,adjective=None,possessive=None,possessive_plural=None):
        self.name, self.plural, self.adjective, self.possessive, self.possessive_plural = name, name, name, name, name
        if plural is not None:
            self.plural = plural
        if adjective is not None:
            self.adjective = adjective
        if possessive is not None:
            self.possessive = possessive
        if possessive_plural is not None:
            self.possessive_plural = possessive_plural

class AbilityScoreIncrease:
    def __init__(self,str=0,dex=0,con=0,int=0,wis=0,cha=0):
        self.str=str
        self.dex=dex
        self.con=con
        self.int=int
        self.wis=wis
        self.cha=cha

class Lifespan:
    def __init__(self,lower_bound,upper_bound,average=None):
        self.lowerBound = lower_bound
        self.upperBound = upper_bound
        self.average = average

class Age:
    def __init__(self,adult: int,lifespan: Lifespan,description: str):
        self.adult = adult
        self.lifespan = lifespan
        self.description = description

class Alignment:
    alignments = {"CG":"Chaotic Good","CN":"Chaotic Neutral","CE":"Chaotic Evil",
                  "NG":"Neutral Good","N":"True Neutral","NE":"Neutral Evil",
                  "LG":"Lawful Good","LN":"Lawful Neutral","LE":"Lawful Evil"}
    def __init__(self,shorthand,description):
        if shorthand not in Alignment.alignments:
            raise ValueError("shorthand takes an alignment in the form 'XY' with X being Chaotic-Lawful and Y being Good-Evil. True Neutral is represented with 'N'")
        self.shorthand = shorthand
        self.alignment = Alignment.alignments[shorthand]
        self.description = description

class Size:
    sizeClasses = {"Tiny":2.5,"Small":5,"Medium":5,"Large":10,"Huge":15,"Gargantuan":20}
    def __init__(self,size_class,lower_height,upper_height,average_weight,description):
        if size_class not in Size.sizeClasses:
            raise ValueError("size_class must be one of the 5e sizes")
        self.sizeClass = size_class
        self.squareFeet = Size.sizeClasses[size_class]
        self.lowerHeight = lower_height
        self.upperHeight = upper_height
        self.averageWeight = average_weight
        self.description = description

class Action:
    pass

class BonusAction:
    pass

class Race:
    name = Name("Singular","Plural","Adjective","Possessive","Possessive Plural")
    abilityScoreIncrease = AbilityScoreIncrease()
    age = Age(0,Lifespan(0,0),"A textual description of the race's lifespan")
    alignment = Alignment("N","A textual description of the race's alignment")
    size = Size("Medium",0,0,0,"A textual description of the race's build")
    speed = 30
    Languages = []

class Item:
    pass

class Proficiencies:
    pass

class Resistance:
    def __init__(self, damage_type):
        self.type = damage_type

class Condition:
    pass

##constants:
D6 = Die(6)