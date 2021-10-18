from fastapi import FastAPI,UploadFile,File,Request,Body
from solver import solve
import uvicorn
import shutil
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
import io
import cv2


app = FastAPI()
templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})
"""@app.get("/image/{image_path}")
def read_item(image_path: str):
   solve(image_path)"""

@app.post("/")
async def root(image:UploadFile = File(...)):
    buffer= open("./images/to_solve.jpg", "wb")
    shutil.copyfileobj(image.file, buffer)
    buffer.close()
    im =  solve("./images/to_solve.jpg")
    res, im_png = cv2.imencode(".png", im)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")