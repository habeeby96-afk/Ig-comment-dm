from fastapi import APIRouter, Request, HTTPException
import os, hashlib, hmac, json
from instagram import handle_comment

router = APIRouter()
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

@router.get("/webhook/instagram")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhook/instagram")
async def receive_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256", "")
    expected = hmac.new(APP_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    data = json.loads(body)
    await handle_comment(data)
    return {"status": "ok"}
