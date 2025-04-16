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
triton_client = tritonhttpclient.InferenceServerClient(url="triton-server:8000")


class TextRequest(BaseModel):
    text: str = Field(example="Пример текста", max_length=1000)


class ToxicityReponse(BaseModel):
    non_toxicity: float = Field(ge=0, le=1)
    insult: float = Field(ge=0, le=1)
    obscenity: float = Field(ge=0, le=1)
    threat: float = Field(ge=0, le=1)
    dangerous: float = Field(ge=0, le=1)


def predict_toxicity(text: str) -> dict[str, float]:
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


@app.post("/predict_toxicity", response_model=ToxicityReponse)
def endpoint(request: TextRequest):
    try:
        response = predict_toxicity(request.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/check_model_toxicity")
async def check_model():
    try:
        is_ready = triton_client.is_model_ready("toxicity_classifier")
        return {"status": "ready" if is_ready else "not ready"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}
