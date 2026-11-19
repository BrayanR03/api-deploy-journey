
from typing import List

from app.db.models.evaluations import Evaluations

from datetime import datetime

def schema_evaluation(evaluation: Evaluations):

    return {
        "created_at": datetime.strftime(evaluation.created_at, "%Y-%m-%d") ,
        "uuid_evaluation": evaluation.uuid_evaluation,
        "result_evaluation": evaluation.result_evaluation,
        "risk factors": {
            "age" : evaluation.age,
            "sex" : evaluation.sex, 
            "bmi" : evaluation.bmi,
            "smoker" : evaluation.smoker,
            "physical_activity" : evaluation.physical_activity,
            "physical_health" : evaluation.physical_activity,
            "mental_health" : evaluation.mental_health,
            "high_cholesterol" : evaluation.high_cholesterol,
            "diabetes" : evaluation.diabetes,
            "high_blood_pressure" : evaluation.high_blood_pressure
        }
    }

def schema_list_evaluation(evaluations: Evaluations)->List[Evaluations]:

    return [
        schema_evaluation(evaluation=evaluation)
        for evaluation in evaluations
    ]
