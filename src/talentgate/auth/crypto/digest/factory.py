from src.talentgate.auth.crypto.digest.strategy import (
    Blake2sMessageDigestStrategy,
    Blake2bMessageDigestStrategy,
)


class MessageDigestStrategyFactory:
    @staticmethod
    def create(
        algorithm: str,
    ) -> Blake2bMessageDigestStrategy | Blake2sMessageDigestStrategy:
        strategies = {
            "blake2b": Blake2bMessageDigestStrategy(),
            "blake2s": Blake2sMessageDigestStrategy(),
        }
        return strategies.get(algorithm, strategies["blake2b"])
