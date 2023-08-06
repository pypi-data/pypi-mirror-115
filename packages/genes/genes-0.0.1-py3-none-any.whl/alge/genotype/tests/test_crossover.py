import pytest

from alge.genotype.creature import Creature
from alge.genotype.operatord.crossover import Crossover
from alge.genotype.operatord.selection import Selection
from alge.genotype.phenotype import Phenotype
from alge.genotype.population import Population


@pytest.fixture
def population():
    result = Population([])
    result.add(Creature(Phenotype([False, False])))
    result.add(Creature(Phenotype([True, True])))
    return result


def test_crossover(population):
    crossover = Crossover({
        Crossover.POPULATION_SIZE: 1,
        Crossover.CHILDREN_PER_PARENTS: 1,
    })
    result = crossover.do(population)

    assert result.size() == 1
    assert result._population[0].phenotype()._data == [False, True]


def test_crossover_multi(population):
    crossover = Crossover({
        Crossover.POPULATION_SIZE: 2,
        Crossover.CHILDREN_PER_PARENTS: 2,
    })
    result = crossover.do(population)

    assert result.size() == 2
    assert result._population[0].phenotype()._data == [False, True]
    assert result._population[1].phenotype()._data == [False, True]
