import time
import tqdm
import random
import requests

url = 'http://127.0.0.1:8081/api/price/'

init_example = {
    "floor": 11,
    "is_apartment": False,
    "kitchen_area": 10.0,
    "living_area": 46.0,
    "rooms": 3,
    "studio": False,
    "total_area": 75.0,
    "build_year": 2008,
    "building_type_int": 4,
    "latitude": 55.87521743774414,
    "longitude": 37.59069442749024,
    "ceiling_height": 2.700000047683716,
    "flats_count": 315,
    "floors_total": 25,
    "has_elevator": True
}

for i in tqdm.tqdm(range(1, 101)):
    cur_example = init_example.copy()

    # Меняем площади, чтобы получать разные предсказания
    cur_example['total_area'] = random.randint(40, 150)
    cur_example["living_area"] = cur_example['total_area'] - cur_example["kitchen_area"]
    
    # Добавляем проблемные запросы, на которых сервис точно упадет
    if random.random() < 0.2:
        param_to_pop = random.choice(list(init_example.keys()))
        cur_example.pop(param_to_pop)

    # Добавляем несколько длинных пауз между запросами
    if i % 30 == 0:
        time.sleep(10)
        
    response = requests.post(url, json=cur_example)
    
    # Добавляем разную задержку между запросами
    sleep_time = random.randint(0, 3)
    time.sleep(sleep_time)
