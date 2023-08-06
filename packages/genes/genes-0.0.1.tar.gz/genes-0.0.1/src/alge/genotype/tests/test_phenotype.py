import pytest
from typing import Tuple
from alge.genotype.phenotype import Phenotype
from alge.genotype.phenotyped.error.phenotype_factory_error import PhenotypeFactoryError
from alge.genotype.phenotyped.factory import  Factory as PhenotypeFactory


def phenotypes_to_create() -> Tuple:
    data = [
        ('',),
        ('0',),
        ('1',),
        ('00000000',),
        ('10101010001111010001101000101111100101010101010100001110001010001',),
    ]
    for row in data:
        yield row


def wrong_phenotypes() -> Tuple:
    data = [
        (' ',),
        ('a',),
        ('0110 ',),
        ('11x',),
    ]
    for row in data:
        yield row


@pytest.mark.parametrize(['phenotype_as_string'], phenotypes_to_create())
def test_phenotype_from_string_creation(phenotype_as_string: str):
    phenotype = PhenotypeFactory.create_from_string(phenotype_as_string)
    assert isinstance(phenotype, Phenotype)
    assert len(phenotype_as_string) == len(phenotype._data)


@pytest.mark.parametrize(['phenotype_as_string'], wrong_phenotypes())
def test_phenotype_from_string_error(phenotype_as_string: str):
    with pytest.raises(PhenotypeFactoryError):
        PhenotypeFactory.create_from_string(phenotype_as_string)
