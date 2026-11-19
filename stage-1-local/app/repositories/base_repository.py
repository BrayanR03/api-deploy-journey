from typing import Any, Generic, TypeVar

from sqlalchemy import inspect, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """CRUD para modelos con PK entera; heredan los repositorios.

    Trabaja con dict (por ejemplo, lo que devuelve request.get_json() o
    schema.load()). Cada operación de escritura hace commit y, si falla,
    rollback para no dejar la sesión inválida.
    """

    # Campos que nunca se actualizan desde datos externos.
    # Los repositorios hijos pueden ampliarlo (p. ej. {"id", "role"}).
    protected_fields: frozenset[str] = frozenset({"id"})

    def __init__(self, model: type[ModelType]):
        self.model = model
        self._columns = {c.key for c in inspect(model).mapper.column_attrs}

    def _clean(self, data: dict[str, Any]) -> dict[str, Any]:

        """Descarta claves que no son columnas del modelo."""
        return {k: v for k, v in data.items() if k in self._columns}

    def _commit(self, db: Session) -> None:
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

    def get(self, db: Session, id: int) -> ModelType | None:
        return db.get(self.model, id)

    def get_by_uuid(self, db: Session, uuid_evaluation: str) -> ModelType | None:
        result = select(self.model).where(self.model.uuid_evaluation==uuid_evaluation)
        return db.scalars(result).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, obj_in: dict[str, Any]) -> ModelType:
        db_obj = self.model(**self._clean(obj_in))
        db.add(db_obj)
        self._commit(db)
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: dict[str, Any]
    ) -> ModelType:
        for field, value in self._clean(obj_in).items():
            if field not in self.protected_fields:
                setattr(db_obj, field, value)
        self._commit(db)
        db.refresh(db_obj)
        return db_obj


    def delete_by_uuid(self, db: Session, uuid_evaluation: str) -> bool:
        result = select(self.model).where(self.model.uuid_evaluation==uuid_evaluation)
        obj = db.scalars(result).first()
        if obj is None:
            return False
        db.delete(obj)
        self._commit(db)
        return True


    def delete(self, db: Session, id: int) -> bool:
        obj = self.get(db, id)
        if obj is None:
            return False
        db.delete(obj)
        self._commit(db)
        return True
