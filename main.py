
import oracledb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="E-Commerce API")

# బ్రౌజర్ కనెక్షన్ కోసం తప్పనిసరి
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conn_params = {
    "user": "system",
    "password": "ruksana",
    "dsn": "localhost:1521/xe",
    "mode": oracledb.AUTH_MODE_SYSDBA
}

@app.get("/get-products")
def get_all_products():
    try:
        conn = oracledb.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT Product_ID, Name, Price, Category FROM Products")
        rows = cursor.fetchall()
        
        products = []
        for r in rows:
            products.append({
                "id": r[0],
                "name": r[1],
                "price": r[2],
                "category": r[3]
            })
        conn.close()
        return products
    except Exception as e:
        return {"error": str(e)}
        @app.post("/add-to-cart")
def add_to_cart(name: str, price: float):
    try:
        conn = oracledb.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Cart (Product_Name, Price) VALUES (:1, :2)", [name, price])
        conn.commit()
        conn.close()
        return {"message": f"{name} added to database cart!"}
    except Exception as e:
        return {"error": str(e)}