import requests

# Уязвимость: секретный API-ключ зашит прямо в исходный код
STRIPE_API_KEY = "sk_live_51P9xK2L9vM8nQ4wR7tY0zX3cV6bN1mA8sD5fG2hJ9kL0p"


def charge_user(amount: int, user_id: str):
    headers = {"Authorization": f"Bearer {STRIPE_API_KEY}"}
    response = requests.post(
        "https://api.stripe.com/v1/charges",
        json={"amount": amount, "currency": "usd", "customer": user_id},
        headers=headers,
    )
    return response.json()
