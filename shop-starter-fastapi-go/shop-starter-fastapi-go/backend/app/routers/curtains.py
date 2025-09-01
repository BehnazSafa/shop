import httpx
from fastapi import APIRouter, HTTPException
from ..schemas import QuoteRequest, QuoteResponse

router = APIRouter(prefix="/curtains", tags=["curtains"])

PRICER_URL = "http://localhost:8080/quote"


@router.post("/quote", response_model=QuoteResponse)
async def quote(req: QuoteRequest):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(PRICER_URL, json=req.model_dump())
            r.raise_for_status()
            return QuoteResponse(**r.json())
    except httpx.HTTPError as e:
        raise HTTPException(502, f"Pricing service error: {e}")
