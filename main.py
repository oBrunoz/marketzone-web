from src import app
import uvicorn

if '__main__' == __name__:
    uvicorn.run(app, reload=True, port="8000")