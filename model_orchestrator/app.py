"""
Сервер оркестрации запросов к моделям на Triton Inference Server
author: <danila.yashin23@gmial.com>
"""
import asyncio
import base64
import io
import json
import os

import numpy as np
from fastapi import FastAPI, HTTPException
from PIL import Image
from schemas import (ModelReadiness, NSFWRequest, NSFWResponse,
                     RankingPairRequest, RankingResponse, TextRequest,
                     ToxicityResponse)
from transformers import AutoTokenizer, ViTImageProcessor
from tritonclient import http as tritonhttpclient

app = FastAPI()

# Инициализация синхронных компонентов
tokenizer = AutoTokenizer.from_pretrained(
    os.path.join(os.path.dirname(__file__), "rubert-tiny-toxicity/tokenizer"),
    local_files_only=True
)

image_preprocessor = ViTImageProcessor.from_pretrained(
    os.path.join(os.path.dirname(__file__), "nsfw-detector/preprocessor"),
    local_files_only=True
)

with open(os.path.join(os.path.dirname(__file__), "user-ranking/config.json"), 
          "r", encoding="UTF-8") as file:
    min_max_values = json.load(file)

VEC_DIM = 50
triton_client = tritonhttpclient.InferenceServerClient(url="triton-server:8000")


def _min_max_scale(value, min_, max_) -> float:
    return (value - min_) / (max_ - min_)


def decoder2vector(ids: list[int]) -> np.ndarray:
    vec = np.zeros((1, VEC_DIM), dtype=np.int64)
    for id_ in ids:
        vec[0, id_ - 1] = 1
    return vec


async def triton_infer(model_name: str, inputs: list):
    def sync_infer():
        return triton_client.infer(model_name, inputs)
    return await asyncio.to_thread(sync_infer)


async def predict_toxicity(text: str) -> dict[str, float]:
    inputs = tokenizer(
        text,
        max_length=64,
        padding="max_length",
        truncation=True,
        return_tensors="np"
    )

    input_ids = tritonhttpclient.InferInput(
        "input_ids", inputs["input_ids"].shape, "INT64"
    )
    attention_mask = tritonhttpclient.InferInput(
        "attention_mask", inputs["attention_mask"].shape, "INT64"
    )

    input_ids.set_data_from_numpy(inputs["input_ids"].astype(np.int64))
    attention_mask.set_data_from_numpy(
        inputs["attention_mask"].astype(np.int64)
    )

    response = await triton_infer(
        "toxicity_classifier",
        [input_ids, attention_mask]
    )

    output = response.as_numpy("output")
    return {k: float(v) for k, v in zip(
        ["non_toxicity", "insult", "obscenity", "threat", "dangerous"],
        output[0]
    )}


async def predict_coincidence(request: RankingPairRequest) -> dict[str, float]:
    request_data = request.model_dump()

    for feature in ("age", "year_created_at", "budget", "rating"):
        for suffix in ("_main", "_candidate"):
            key = feature + suffix
            request_data[key] = _min_max_scale(
                request_data[key],
                min_max_values[f"{feature}_min"],
                min_max_values[f"{feature}_max"]
            )

    numerical = np.array([request_data[col] for col in [
        "age_main", "year_created_at_main", "budget_main", "rating_main",
        "age_candidate", "year_created_at_candidate",
        "budget_candidate", "rating_candidate",
        "gender_main", "gender_candidate"
    ]]).reshape(1, -1).astype(np.float32)

    categorical = np.array([request_data[col] for col in [
        "ei_id_main", "education_direction_main",
        "ei_id_candidate", "education_direction_candidate"
    ]]).reshape(1, -1).astype(np.int64)

    habits = np.expand_dims(np.concatenate([
        decoder2vector(request_data[col])
        for col in ["habit_ids_main", "habit_ids_candidate"]
    ]), axis=0).astype(np.int64)

    interests = np.expand_dims(np.concatenate([
        decoder2vector(request_data[col])
        for col in ["interest_ids_main", "interest_ids_candidate"]
    ]), axis=0).astype(np.int64)

    inputs = [
        tritonhttpclient.InferInput("num_input", numerical.shape, "FP32")
        .set_data_from_numpy(numerical),
        tritonhttpclient.InferInput("cat_input", categorical.shape, "INT64")
        .set_data_from_numpy(categorical),
        tritonhttpclient.InferInput("habits_input", habits.shape, "INT64")
        .set_data_from_numpy(habits),
        tritonhttpclient.InferInput("interest_input", interests.shape, "INT64")
        .set_data_from_numpy(interests)
    ]

    response = await triton_infer("user_ranking", inputs)
    return {"coincidence": float(response.as_numpy("output")[0])}


async def predict_nsfw(image: Image.Image) -> dict[str, float]:
    inputs = np.asarray(
        image_preprocessor(image)["pixel_values"],
        dtype=np.float32
    )

    infer_input = tritonhttpclient.InferInput(
        "image",
        inputs.shape,
        "FP32"
    ).set_data_from_numpy(inputs.astype(np.float32))

    response = await triton_infer("nsfw_detector", [infer_input])
    output = response.as_numpy("output")
    return {"normal": float(output[0, 0]), "nsfw": float(output[0, 1])}


@app.post("/ranking_pair", response_model=RankingResponse)
async def compare_pair(request: RankingPairRequest):
    try:
        return await predict_coincidence(request)
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.post("/predict_toxicity", response_model=ToxicityResponse)
async def toxicity_endpoint(request: TextRequest):
    try:
        return await predict_toxicity(request.text)
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.post("/predict_nsfw", response_model=NSFWResponse)
async def nsfw_endpoint(request: NSFWRequest):
    try:
        image = (Image.open(io.BytesIO(base64.b64decode(request.image)))
                 .convert("RGB"))
        return await predict_nsfw(image)
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.get("/check_model_{model_name}", response_model=ModelReadiness)
async def check_model(model_name: str):
    try:
        is_ready = await asyncio.to_thread(
            triton_client.is_model_ready,
            f"{model_name}_classifier" if model_name == "toxicity" else
            "user_ranking" if model_name == "ranking" else
            "nsfw_detector"
        )
        return {"ready": is_ready}
    except Exception as e:
        return {"error": str(e)}
