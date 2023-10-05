import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .image_processor import ImageProcessor
from .scraper import Scraper

app = FastAPI()

class RequestModel(BaseModel):
    prompt: str
    channel_url: str

@app.post("/process_image/", response_model=dict)
async def process_image_endpoint(request: RequestModel):
    try:
        print("Received request: ", request)
        processor = ImageProcessor()
        print("Created processor instance: ", processor)
        scraper_instance = Scraper()
        print("Created scraper instance: ", scraper_instance)
        json_obj = processor.process_image(request.prompt, request.channel_url, scraper_instance)
        print("Returning response: ", json_obj)
        return json.loads(json_obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
