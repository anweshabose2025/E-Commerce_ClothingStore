"""Shopping cart routes for adding and retrieving items"""

from fastapi import APIRouter
from ..database import cart_collection
from ..pydanticmodel import CartItem

router = APIRouter(prefix="/cart", tags=["Cart"])
# This is mainly for documentation.
# FastAPI automatically creates Swagger UI docs.
# All APIs with tag "Cart" will appear grouped under a section called:Cart

@router.post("/add") # This is a decorator in FastAPI. This function will run when a user sends a POST request. POST /cart/add
def add_to_cart(item:CartItem):
    """Add an item to the user's shopping cart"""
    item_data = item.model_dump() if hasattr(item,"model_dump") else item.dict() # Converting Pydantic Object to Dictionary
    cart_collection.insert_one(item_data)
    return {"message":"Item added to the cart"}

@router.get("/{user_email}")
def get_cart(user_email:str):
    """Get all shoping cart items for a specific user"""
    items = list(cart_collection.find({"user_email":user_email}, {"_id": 0}))
    return items

@router.delete("/{user_email}")
def delete_cart(user_email:str):
    """Delete all shoping cart items for a specific user"""
    cart_collection.delete_many({"user_email":user_email})
    return {"message":"Cart cleared successfully"}

# item = CartItem(
#     item="Phone",
#     quantity=1,
#     price=25000
# )
# 
# item_data = {
#     "item": "Phone",
#     "quantity": 1,
#     "price": 25000
# }