from ..db.models.evaluations import Evaluations
from .base_repository import BaseRepository


class EvaluationsRepository(BaseRepository[Evaluations]):
    """Repositorio de evaluaciones (PK: evaluation_id)."""

    def __init__(self) -> None:
        super().__init__(Evaluations)


evaluations_repository = EvaluationsRepository()