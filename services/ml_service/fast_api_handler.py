"""Класс FastApiHandler, который обрабатывает запросы API."""

import pickle
import pandas as pd


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "model_params": dict
        }

        self.model_path = "../models/model.pkl"
        self.load_price_model(model_path=self.model_path)
        
        # необходимые параметры для предсказаний модели оттока
        self.required_model_params = [
            "floor", "is_apartment", "kitchen_area", "living_area", "rooms", "studio",
            "total_area", "build_year", "building_type_int", "latitude", "longitude",
            "ceiling_height", "flats_count", "floors_total", "has_elevator"
        ]

    def load_price_model(self, model_path: str):
        """Загружаем обученную модель предсказания цены.
        
        Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = pickle.load(open(model_path, 'rb'))
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        """Предсказываем цену.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float — предсказание цены
        """
        param_dataframe = pd.DataFrame(model_params, index=[0])
        
        return self.model.predict(param_dataframe)[0]
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.

        Args:
            query_params (dict): Параметры запроса.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if "model_params" not in query_params:
            return False
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры объекта недвижимости на наличие обязательного набора.

        Args:
            model_params (dict): Параметры объекта недвижимости для предсказания.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            bool: True — если запрос корректный, False — иначе
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
        
    def handle(self, params):
        """Функция для обработки входящих запросов по API. Запрос состоит из параметров.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                print(f"Predicting for model_params:\n{model_params}")
                # получаем предсказания модели
                prediction = self.price_predict(model_params)
                response = {
                    "score": int(round(prediction))
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            response = {"Error": "Problem with request"}
        finally:
            return response
