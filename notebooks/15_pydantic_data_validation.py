from sympy import field_isomorphism
from openpyxl.comments import comments
from os import listdrives
from attr.validators import min_len
class user():
    name = ""
    email = ""
    age = 0

user = user()
user.name = "Ajith Kumar"
user.email = "ajithkumar@gmail.com"
user.age = "my age is 23"

print(user)



### Using Pydantic for data validation 
from pydantic import BaseModel , Field
from typing import List

class user(BaseModel):
    name : str 
    age : int
    email : str

user = user(
    name = "ajith kumar", 
    age = 23, 
    email = "ajithkumar@gmail.com")

print(user.name)

### Field Validation
class Product(BaseModel):
    product_name: str = Field(max_length=50)
    product_description: str = Field(min_length=20)
    product_price: int = Field(gt=0, le=100)


product = Product(
    product_name="Iphone 16 Pro Max",
    product_description="This is the latest phone from apple with the best camera quality and the best processor.",
    product_price=10
)
product2 = Product(
    product_name="Iphone 17 Pro",
    product_description="This is the latest phone from apple with the best camera quality and the best processor.",
    product_price=50
)

class Order(BaseModel):
    order_id: str = Field(min_length=5, max_length=12)
    product: Product


order = Order(
    order_id="nvj32n3n3n",
    product=product
)

print(order.product.product_description)


class Carts(BaseModel):
    id : str = Field(min_length=5 , max_length=12)
    items : list[Product]
    comments : str = Field(default="No Comments")

cart = Carts(id= "dbhde32", items=[product , product2], comments= "This is my Cart")

for product in cart.items:
    print(product.product_name)

