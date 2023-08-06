import pytest

from alge.genotype.creature import Creature
from alge.genotype.operatord.selection import Selection
from alge.genotype.phenotype import Phenotype
from alge.genotype.population import Population


@pytest.fixture
def population():
    result = Population([])
    result.add(Creature(Phenotype([False, True]), 20))
    result.add(Creature(Phenotype([True, True]), 10))
    result.add(Creature(Phenotype([True, False]), 40))
    result.add(Creature(Phenotype([False, False]), 30))
    return result


def test_selection(population):
    selection = Selection()
    result = selection.do(population)

    assert result.size() == 2
    assert result._population[0].fitness() == 40
    assert result._population[1].fitness() == 30


def test_selection_custom_elements_number(population):
    selection = Selection({Selection.CREATURES_TO_CHOOSE: 3})
    result = selection.do(population)

    assert result.size() == 3
    assert result._population[0].fitness() == 40
    assert result._population[1].fitness() == 30
    assert result._population[2].fitness() == 20
