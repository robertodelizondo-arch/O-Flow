from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(
    title="O-Flow API",
    description="API para el pronóstico de demanda basada en MLOps y Scikit-learn",
    version="1.0.0"
)

# Definir la estructura de los datos de entrada esperados mediante Pydantic
class DemandPredictionInput(BaseModel):
    store_id: str
    item_id: str
    historical_sales: list[float]
    promotional_flag: int
    temperature: float

# Ruta de verificación de salud (Health Check)
@app.get("/health", tags=["Sistema"])
def health_check():
    return {
        "status": "healthy",
        "message": "El servicio de O-Flow está operando correctamente."
    }

# Endpoint principal de predicción
@app.post("/predict", tags=["Predicción"])
def predict_demand(data: DemandPredictionInput):
    try:
        # Aquí puedes integrar la carga de tu modelo entrenado (.pkl o MLflow)
        # Ejemplo conceptual de procesamiento de datos:
        input_data = pd.DataFrame([{
            "promotional_flag": data.promotional_flag,
            "temperature": data.temperature,
            "avg_historical_sales": sum(data.historical_sales) / len(data.historical_sales) if data.historical_sales else 0
        }] )
        
        # Simulación de inferencia (reemplaza esto con tu modelo real cargado)
        # prediction = model.predict(input_data)[0]
        
        # Resultado simulado robusto para pruebas iniciales
        predicted_demand = round(input_data["avg_historical_sales"].iloc[0] * (1.15 if data.promotional_flag == 1 else 1.0), 2)

        return {
            "store_id": data.store_id,
            "item_id": data.item_id,
            "predicted_demand": predicted_demand,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))