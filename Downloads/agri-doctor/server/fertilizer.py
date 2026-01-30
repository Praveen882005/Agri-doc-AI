from fastapi import APIRouter

router = APIRouter(prefix="/fertilizer", tags=["Fertilizer"])

@router.get("/shops")
async def get_shops(city: str):
    shops = {
        "chennai": ["GreenGrow Fertilizers", "AgroMart", "Farmer’s Hub"],
        "madurai": ["Madurai Agro Depot", "GrowWell Traders"],
        "vellore": ["Vellore Fertilizer Center", "AgriNeeds"],
    }
    return {"shops": shops.get(city.lower(), ["No shops found in this city."])}
