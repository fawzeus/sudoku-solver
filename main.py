from fastapi import FastAPI,UploadFile,File,Request,Body
from solver import solve
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


@app.post("/")
async def root(image:UploadFile = File(...)):
    buffer= open("./temp/to_solve.jpg", "wb")
    shutil.copyfileobj(image.file, buffer)
    buffer.close()
    #image=cv2.imread("./temp/to_solve.jpg")
    #cv2.imshow("Original Image",image)
    #cv2.waitKey(0)
    im =  solve("./temp/to_solve.jpg")
    res, im_png = cv2.imencode(".png", im)
    return StreamingResponse(StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png"))