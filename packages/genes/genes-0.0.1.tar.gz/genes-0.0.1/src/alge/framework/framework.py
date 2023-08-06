
from alge.genalg.api import GeneticAlgorithmApi

class GeneticAlgorithmFramework():

    _api: GeneticAlgorithmApi

    def __init__(self, api: GeneticAlgorithmApi):
        self._api = api

