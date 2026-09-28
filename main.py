from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import string
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# डेटा को याद रखने के लिए एक नकली डेटाबेस (Dictionary)
url_database = {}

# 5 अक्षरों का एक रैंडम कोड बनाने के लिए फ़ंक्शन (जैसे: aB3xD)
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(5))

# 1. मुख्य पेज लोड करने के लिए (Frontend Route)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "short_url": None})

# 2. बटन दबाने पर लंबा URL लेकर छोटा करने के लिए
@app.post("/shorten", response_class=HTMLResponse)
async def shorten_url(request: Request, url: str = Form(...)):
    # एक नया शॉर्ट कोड बनाएं
    code = generate_short_code()
    # डेटाबेस में सेव करें
    url_database[code] = url
    
    # लाइव होने पर यह खुद का URL दिखाएगा
    base_url = str(request.base_url)
    short_url = f"{base_url}{code}"
    
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})

# 3. शॉर्ट URL पर क्लिक करने पर असली वेबसाइट पर भेजने के लिए (Redirection)
@app.get("/{code}")
async def redirect_to_original(code: str):
    if code in url_database:
        return RedirectResponse(url=url_database[code])
    raise HTTPException(status_code=404, detail="Short URL not found")
