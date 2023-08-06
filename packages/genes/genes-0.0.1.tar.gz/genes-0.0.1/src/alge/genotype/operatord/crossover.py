from random import randint
from typing import Tuple
from alge.genotype.operator import Operator
from alge.genotype.creature import Creature
from alge.genotype.population import Population
from alge.genotype.phenotype import Phenotype


class Crossover(Operator):

    POPULATION_SIZE = 'population_size'
    CHILDREN_PER_PARENTS = 'children_per_parents'

    _config: dict = {
        POPULATION_SIZE: 10,
        CHILDREN_PER_PARENTS: 2,
    }

    def __init__(self, config: dict = None):
        if config is not None:
            self._config = config

    def do(self, population: Population) -> Population:
        next_generation = Population([])
        parent_index = 0
        while next_generation.size() < self._config[self.POPULATION_SIZE]:
            parents: Tuple[Creature, Creature] = self.choose_parents(parent_index, population)
            for i in range(0, self._config[self.CHILDREN_PER_PARENTS]):
                next_generation.add(self.child(parents))
            parent_index += 2
        return next_generation

    @staticmethod
    def child(parents: Tuple[Creature, Creature]) -> Creature:
        phenotype_len = len(parents[0].phenotype())
        # if len(parents[1].phenotype()) is not phenotype_len:
        #     raise Exception('Parents have different phenotypes lengths!')

        cross_point = randint(1, phenotype_len - 1)
        # part1 = parents[0].phenotype()._data[0:cross_point]
        # part2 = parents[1].phenotype()._data[cross_point:]
        child_phenotype = Phenotype(
            parents[0].phenotype()._data[0:cross_point] + parents[1].phenotype()._data[cross_point:]
        )

        return Creature(child_phenotype)

    @staticmethod
    def choose_parents(parent_index: int, population: Population) -> Tuple[Creature, Creature]:
        parent1 = population[parent_index]
        parent2 = population[parent_index + 1]
        return parent1, parent2
