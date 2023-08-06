
from typing import List, Optional
from logging import Logger
from .config import Config
from ..genotype.operator import Operator
from ..genotype.population import Population
from ..genotype.fitness_function import FitnessFunction
# from ..genom.operator import Operator
from alge.genalg.stats import Stats


class GeneticAlgorithmApi():

    # _logger: Logger
    # _config: Config
    # _population: Population = None
    # _fitness_function: FitnessFunction
    # _actions: List[Action]

    def __init__(self,
                 logger: Optional[Logger],
                 config: Config,
                 fitness_function: FitnessFunction,
                 actions: List[Operator],
                 stats: Stats = None
                 ):
        self._logger = logger
        self._config = config
        self._fitness_function = fitness_function
        self._actions: List[Operator] = actions
        self._population: Population = Population([])
        self._stats: Stats = stats

    def init_population(self, population: Population) -> None:
        self._population = population
        self._fit_population()

    def population(self) -> Population:
        return self._population

    def next_generation(self) -> Population:
        if self._population is None:
            raise Exception('Population not initialized!')

        self._execute_actions()
        self._fit_population()
        return self._population

    def _fit_population(self) -> None:
        for creature in self._population._population:
            creature._fitness = self._fitness_function.fit(creature.phenotype())
            # if self._stats:
            #     self._stats.add_fit_stats({})

    def _execute_actions(self) -> None:
        # next_generation = self._selection(self._population)
        # next_generation = self._crossover(next_generation)
        # next_generation = self._mutation(next_generation)

        generation = self._population
        for action in self._actions:
            generation = action.do(generation)
            if self._stats:
                self._stats.add_action_stats(action.get_stats())

        self._population = generation

    # # actions
    # def _selection(self, population: Population) -> Population:
    #     return population
    #
    # def _crossover(self, population: Population) -> Population:
    #     return population
    #
    # def _mutation(self, population: Population) -> Population:
    #     return population
