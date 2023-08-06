from __future__ import annotations


class PhenotypeFactoryError(RuntimeError):
    @classmethod
    def character_not_allowed(cls, char: str) -> PhenotypeFactoryError:
        return cls(f'Character not allowed: {char}')
