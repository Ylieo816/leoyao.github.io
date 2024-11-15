from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.infringement_check import check_infringement
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Define request model
class InfringementRequest(BaseModel):
    patent_id: str
    company_name: str

# Define endpoint for infringement check
@app.post("/check-infringement")
async def run_infringement_check(request: InfringementRequest = Body(...)):
    # Log received request
    print(f"Received request: patent_id={request.patent_id}, company_name={request.company_name}")
    
    # Perform infringement check
    result = check_infringement(request.patent_id, request.company_name)
    
    # Handle error cases
    if isinstance(result, dict) and 'error' in result:
        return JSONResponse(content=result, status_code=404)
    
    # Log analysis result
    print(f"Analysis result: {result}")
    
    # Return successful response
    return JSONResponse(content={"infringing_products": result})

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)