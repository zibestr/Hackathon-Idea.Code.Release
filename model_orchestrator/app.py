"""
Сервер оркестрации запросов к моделям на Triton Inference Server
author: <danila.yashin23@gmial.com>
"""
import json
# TODO: обучить модель ранжирования на синтетических данных
import os

import numpy as np
from fastapi import FastAPI, HTTPException
from schemas import (ModelReadiness, RankingPairRequest, RankingResponse,
                     TextRequest, ToxicityReponse)
from transformers import AutoTokenizer
from tritonclient import http as tritonhttpclient

app = FastAPI()
tokenizer_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rubert-tiny-toxicity/tokenizer"
)
tokenizer = AutoTokenizer.from_pretrained(
    tokenizer_path,
    local_files_only=True
)

minmax_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "user-ranking/config.json"
)
with open(minmax_path, "r", encoding="UTF-8") as file:
    min_max_values = json.load(file)
VEC_DIM = 50

triton_client = tritonhttpclient.InferenceServerClient(
    url="triton-server:8000"
)


def _min_max_scale(value, min_, max_) -> float:
    return (value - min_) / (max_ - min_)


def decoder2vector(ids: list[int]) -> np.ndarray:
    """Кодирует перечень интересов или вредных привычек в вектор

    Args:
        ids (list[int]): id интересов или вредных привычек

    Returns:
        np.ndarray: закодированная фича
    """
    vec = np.zeros(shape=(1, VEC_DIM), dtype=np.int64)
    for id_ in ids:
        vec[0, id_ - 1] = 1
    return vec


def predict_toxicity(text: str) -> dict[str, float]:
    """
    Функция обращения к Triton Inference Server модели toxicity_classifier
    по HTTP протоколу.
    Args:
        - text: str - текст для классификации.
    Returns:
        dict[str, float]: словарь с классами и их вероятностями.
    """
    inputs = tokenizer(
        text,
        max_length=64,
        padding="max_length",
        truncation=True,
        return_tensors="np"
    )

    input_ids = tritonhttpclient.InferInput(
        "input_ids",
        inputs["input_ids"].shape,
        "INT64"
    )
    attention_mask = tritonhttpclient.InferInput(
        "attention_mask",
        inputs["attention_mask"].shape,
        "INT64"
    )

    input_ids.set_data_from_numpy(inputs["input_ids"].astype(np.int64))
    attention_mask.set_data_from_numpy(
        inputs["attention_mask"].astype(np.int64)
    )

    response = triton_client.infer(
        model_name="toxicity_classifier",
        inputs=[input_ids, attention_mask]
    )

    output = response.as_numpy("output")
    return {
        "non_toxicity": float(output[0, 0]),
        "insult": float(output[0, 1]),
        "obscenity": float(output[0, 2]),
        "threat": float(output[0, 3]),
        "dangerous": float(output[0, 4])
    }


def predict_coincidence(request: RankingPairRequest) -> dict[str, float]:
    """
    Функция обращения к Triton Inference Server модели user_ranking
    по HTTP протоколу.
    Args:
        request: RankingPairRequest - запрос с данными двух пользователей.
    Returns:
        dict[str, float]: словарь с вероятностью сходства двух пользователей.
    """
    request = request.model_dump()
    for feature in ("age", "year_created_at", "budget", "rating"):
        request[feature + "_main"] = _min_max_scale(
            request[feature + "_main"],
            min_max_values[feature + "_min"],
            min_max_values[feature + "_max"]
        )
        request[feature + "_candidate"] = _min_max_scale(
            request[feature + "_candidate"],
            min_max_values[feature + "_min"],
            min_max_values[feature + "_max"]
        )
    numerical_features = ["age_main", "year_created_at_main",
                          "budget_main", "rating_main",
                          "age_candidate", "year_created_at_candidate",
                          "budget_candidate", "rating_candidate",
                          "gender_main", "gender_candidate"]
    cat_features = ["ei_id_main",
                    "education_direction_main",
                    "ei_id_candidate",
                    "education_direction_candidate"]
    habit_features = ["habit_ids_main", "habit_ids_candidate"]
    interest_features = ["interest_ids_main", "interest_ids_candidate"]

    input_numerical = np.array([request[col]
                                for col in numerical_features]).reshape(1, -1)
    input_categorical = np.array([request[col]
                                  for col in cat_features]).reshape(1, -1)
    input_habit = np.expand_dims(np.concatenate(
        [decoder2vector(request[col])
         for col in habit_features]
    ), axis=0)
    input_interest = np.expand_dims(np.concatenate(
        [decoder2vector(request[col])
         for col in interest_features]
    ), axis=0)

    num_input = tritonhttpclient.InferInput(
        "num_input",
        input_numerical.shape,
        "FP32"
    )
    cat_input = tritonhttpclient.InferInput(
        "cat_input",
        input_categorical.shape,
        "INT64"
    )
    habits_input = tritonhttpclient.InferInput(
        "habits_input",
        input_habit.shape,
        "INT64"
    )
    interest_input = tritonhttpclient.InferInput(
        "interest_input",
        input_interest.shape,
        "INT64"
    )

    num_input.set_data_from_numpy(input_numerical.astype(np.float32))
    cat_input.set_data_from_numpy(
        input_categorical.astype(np.int64)
    )
    habits_input.set_data_from_numpy(input_habit.astype(np.int64))
    interest_input.set_data_from_numpy(input_interest.astype(np.int64))

    response = triton_client.infer(
        model_name="user_ranking",
        inputs=[num_input, cat_input, habits_input, interest_input]
    )

    output = response.as_numpy("output")
    return {"coincidence": float(output[0])}


@app.post("/ranking_pair", response_model=RankingResponse)
def compare_pair(request: RankingPairRequest):
    """Endpoint API модели ранжирования пользователей

    Args:
        request (RankingPairRequest): Запрос к модели.

    Raises:
        HTTPException: 500 ошибка, если есть проблемы на стороне Triton
        Inference Server

    Returns:
        RankingResponse: Ответ модели.
    """
    try:
        response = predict_coincidence(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_toxicity", response_model=ToxicityReponse)
def toxicity_endpoint(request: TextRequest):
    """Endpoint API модели классификации токсичности

    Args:
        request (TextRequest): Запрос к модели.

    Raises:
        HTTPException: 500 ошибка, если есть проблемы на стороне Triton
        Inference Server

    Returns:
        ToxicityReponse: Ответ модели.
    """
    try:
        response = predict_toxicity(request.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check_model_toxicity", response_model=ModelReadiness)
async def check_toxicity_model():
    """API проверки доступности модели для опеределения токсичности текста."""
    try:
        is_ready = triton_client.is_model_ready("toxicity_classifier")
        return {"ready": is_ready}
    except Exception as e:
        return {"error": str(e)}


@app.get("/check_model_ranking", response_model=ModelReadiness)
async def check_ranking_model():
    """API проверки доступности модели для опеределения токсичности текста."""
    try:
        is_ready = triton_client.is_model_ready("user_ranking")
        return {"ready": is_ready}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    """API проверки доступности сервиса оркестрации моделей."""
    return {"status": "ok"}
