# Ваш словарь
import json
import urllib.parse

data = [
    {"name": "название", "description": "описание", "price": 10, "image": "path"},
    {"name": "название2", "description": "описани2е", "price": 15, "image": "path"},
    {"name": "название32", "description": "опис2ани2е", "price": 100, "image": "path"},
]

# Преобразование в JSON и кодирование в URL
encoded_data = urllib.parse.quote(json.dumps(data))

# Получение URL
base_url = "http://localhost:63342/tg_rouse/static/templates/cart.html"
url = f"{base_url}?product={encoded_data}"

print(url)
