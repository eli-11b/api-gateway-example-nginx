# service_b/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/products/")
def read_products():
    return {"message": "List of products as a response from product service"}

@app.get("/products/docs")
async def show_documentation():
    """
        SUMMARY: Show Swagger documentation
        ARGS: NONE
        RETURNS: redirect to swagger docs        
    """
    return RedirectResponse("http://localhost:8001/docs")


@app.get("/products/{product_id}")
def read_product(product_id: int):
    return {"message": f"Product with ID {product_id}"}
