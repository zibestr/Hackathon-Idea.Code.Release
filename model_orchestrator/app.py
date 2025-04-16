"""
Сервер оркестрации запросов к моделям на Triton Inference Server
author: <danila.yashin23@gmial.com>
"""
#  TODO: придумать фичи для модели ранжирования
#  TODO: обучить модель ранжирования на синтетических данных
#  TODO: прописать API для обращения к модели ранжирования
import os

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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
triton_client = tritonhttpclient.InferenceServerClient(
    url="triton-server:8000"
)


class TextRequest(BaseModel):
    """Запрос к модели классификации токсичности текста.
    Fields:
        - text: str - Текст для классификации, максимальная длина 1000.
    """
    text: str = Field(example="Пример текста", max_length=1000)


class ToxicityReponse(BaseModel):
    """Ответ от модели классификации токсичности текста.
    Fields:
        - non_toxicity: float - Вероятность нетоксичности текста, от 0 до 1.
        - insult: float - Вероятность оскорбления в тексте, от 0 до 1.
        - obscenity: float - Вероятность непристойности текста, от 0 до 1.
        - threat: float - Вероятность угрозы в тексте, от 0 до 1.
        - dangerous: float - Вероятность текста нанести вред репутации
        говорящего, от 0 до 1.
    """
    non_toxicity: float = Field(ge=0, le=1)
    insult: float = Field(ge=0, le=1)
    obscenity: float = Field(ge=0, le=1)
    threat: float = Field(ge=0, le=1)
    dangerous: float = Field(ge=0, le=1)


class RankingPairRequest(BaseModel):
    """Запрос к моделе ранжирования пар пользователей.
    Fields:
        TODO: придумать фичи
    """
    pass


class RankingResponse(BaseModel):
    """Ответ модели ранжирования пар пользователей.
    Fields:
        - coincidence: float - Вероятность совпадения пользователей, от 0 до 1.
    """
    coincidence: float = Field(default=0.0, ge=0, le=1)


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
        TODO: вот тут все к свиням заменить
    Returns:
        dict[str, float]: словарь с вероятностью сходства двух пользователей.
    """
    from random import random
    return {"coincidence": random()}


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


@app.get("/check_model_toxicity")
async def check_toxicity_model():
    """API проверки доступности модели для опеределения токсичности текста."""
    try:
        is_ready = triton_client.is_model_ready("toxicity_classifier")
        return {"status": "ready" if is_ready else "not ready"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    """API проверки доступности сервиса оркестрации моделей."""
    return {"status": "ok"}
