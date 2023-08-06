from ...genotype.creature import Creature
from ...genotype.phenotyped.factory import  Factory as PhenotypeFactory


def test_creature_create():
    creature = Creature(PhenotypeFactory.create_from_string('1010101'))
    assert isinstance(creature, Creature)


def test_fitness():
    creature = Creature(PhenotypeFactory.create_from_string('1010101'), 10.10)
    assert creature.fitness() == 10.10
    creature.set_fitness(0.9)
    assert creature.fitness() == 0.9
