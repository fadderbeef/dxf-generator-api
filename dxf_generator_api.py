import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import ezdxf

app = FastAPI()

OUTPUT_FOLDER = "output_dxfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class GenerateDXFRequest(BaseModel):
    part_name: str
    profile: List[List[float]]  # list of [x, y] coordinates

@app.post("/generate-dxf")
def generate_dxf(request: GenerateDXFRequest):
    try:
        filename = f"{request.part_name}.dxf"
        filepath = os.path.join(OUTPUT_FOLDER, filename)

        doc = ezdxf.new(dxfversion='R2018')
        msp = doc.modelspace()
        msp.add_lwpolyline(request.profile, close=True)
        doc.saveas(filepath)

        return {
            "message": f"{filename} generated",
            "download_url": f"/files/{filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
app.mount("/files", StaticFiles(directory=OUTPUT_FOLDER), name="files")
