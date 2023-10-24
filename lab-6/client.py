import requests

response = requests.post('http://localhost:5000/api/electro-scooters', json={'name': 'Scooter 1', 'battery_level': 80})
print(response.json())