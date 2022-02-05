from fastapi import FastAPI

app = FASTAPI()

@app.get("/")
def home_view():
    return{"hello": "world"}
