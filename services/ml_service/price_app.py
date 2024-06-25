"""FastAPI-приложение для модели предсказания цены."""

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_client import Histogram
from fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator

# создаём приложение FastAPI
app = FastAPI()

# создаём обработчик запросов для API
app.handler = FastApiHandler()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

main_app_predictions = Histogram(
    # имя метрики
    "main_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets = (0.5e7, 1e7, 1.5e7, 2e7, 2.5e7, 3e7, 3.5e7, 4e7, 4.5e7, 5e7)
)
main_app_counter_errors = Counter(
    # имя метрики
    "main_app_counter_errors", 
    # описание метрики
    "Count of errors caused by wrong requests"
)

@app.post("/api/price/") 
def get_prediction_for_estate(model_params: dict):
    """Функция для получения предсказания цены.

    Args:
        model_params (dict): Параметры объекта недвижимости, которые нужно передать в модель.

    Returns:
        dict: Предсказание цены для объекта недвижимости.
    """
    all_params = {
        "model_params": model_params
    }
    response = app.handler.handle(all_params)
    if "score" in response:
        main_app_predictions.observe(response["score"])
    else:
        main_app_counter_errors.inc()
    return response
