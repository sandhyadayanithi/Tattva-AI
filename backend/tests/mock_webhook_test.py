import httpx
import asyncio

async def test_webhook_verification():
    """Tests the GET /webhook verification logic."""
    url = "http://localhost:8000/webhook"
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "hackathon123",
        "hub.challenge": "12345678"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            print(f"GET /webhook Status: {response.status_code}")
            print(f"GET /webhook Response: {response.text}")
            if response.text == "12345678":
                print("✅ Webhook verification PASSED")
            else:
                print("❌ Webhook verification FAILED")
        except Exception as e:
            print(f"Error testing verification: {e}")

async def test_webhook_post_text():
    """Tests the POST /webhook with a text message payload."""
    url = "http://localhost:8000/webhook"
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "12345", "phone_number_id": "1088612030996309"},
                    "messages": [{
                        "from": "919999999999",
                        "id": "msg_001",
                        "timestamp": "1671234567",
                        "text": {"body": "Hello fact checker"},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            print(f"POST /webhook (Text) Status: {response.status_code}")
            print(f"POST /webhook (Text) Response: {response.text}")
        except Exception as e:
            print(f"Error testing POST text: {e}")

if __name__ == "__main__":
    print("Ensure the FastAPI server is running (python -m uvicorn main:app --reload)")
    print("-" * 40)
    asyncio.run(test_webhook_verification())
    print("-" * 40)
    asyncio.run(test_webhook_post_text())
