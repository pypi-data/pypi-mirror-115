from alge.genotype.phenotype import Phenotype
from alge.genotype.phenotyped.error.phenotype_factory_error import PhenotypeFactoryError


CHAR_0 = '0'
CHAR_1 = '1'


class Factory:

    @staticmethod
    def create_from_string(input: str) -> Phenotype:
        phenotype = []
        for char in input:
            if char == CHAR_0:
                phenotype.append(False)
            elif char == CHAR_1:
                phenotype.append(True)
            else:
                raise PhenotypeFactoryError(char)
        return Phenotype(phenotype)
