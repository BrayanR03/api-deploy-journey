
from datetime import date
from uuid import UUID, uuid4
from flask import json
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Uuid, text
from ..db import db

class Evaluations(db.Model):

    __tablename__ = "evaluations"

    evaluation_id: Mapped[int] = mapped_column(
        primary_key= True, nullable= False
    )

    age: Mapped[int] = mapped_column(
        nullable= False
    )

    sex: Mapped[bool] = mapped_column(
        nullable= False
    )

    smoker: Mapped[bool] = mapped_column(
        nullable= False
    )

    bmi: Mapped[float] = mapped_column(
        nullable= False
    )

    physical_activity: Mapped[bool] = mapped_column(
        nullable= False
    )

    physical_health: Mapped[int] = mapped_column(
        nullable= False
    )

    mental_health: Mapped[int] = mapped_column(
        nullable= False
    )

    high_cholesterol: Mapped[bool] = mapped_column(
        nullable= False
    )

    diabetes: Mapped[bool] = mapped_column(
        nullable= False
    )

    high_blood_pressure: Mapped[bool] = mapped_column(
        nullable= False
    )

    result_evaluation: Mapped[bool] = mapped_column(
        nullable= False
    )

    created_at: Mapped[date] = mapped_column(
        nullable= False, default= date.today, 
        server_default= text('CURRENT_DATE  ')
    )

    uuid_evaluation: Mapped[UUID] = mapped_column(
        Uuid(as_uuid= True), nullable= False, unique= True,
        default= uuid4, server_default= text('gen_random_uuid()')
    )