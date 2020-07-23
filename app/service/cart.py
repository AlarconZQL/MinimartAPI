from app import db
from app.models import Cart, Store, ProductStoreLink, CartProductLink


class CartService:
    @staticmethod
    def create_store_cart(store_id):
        store = Store.query.get(store_id)
        if store != None:
            new_cart = Cart(store_id=store_id)
            db.session.add(new_cart)
            db.session.commit()
            return new_cart
        else:
            return None

    @staticmethod
    def add_product_to_cart(cart_id, product_id):
        cart = Cart.query.get(cart_id)
        # Check if the cart exists
        if cart != None:
            # Check if the store has stock of the product
            store_product = ProductStoreLink.query.filter_by(
                store_id=cart_id, product_id=product_id).first()
            if store_product != None and store_product.stock > 0:
                store_product.stock = store_product.stock - 1
                # Add product to the cart
                cart_product = CartProductLink.query.filter_by(
                    cart_id=cart.id, product_id=product_id).first()
                if cart_product != None:
                    cart_product.units = cart_product.units + 1
                else:
                    cart.products.append(CartProductLink(
                        cart_id=cart.id, product_id=product_id, units=1))
                db.session.add(cart)
                db.session.commit()
                return cart
            else:
                raise Exception('No stock for that product')
        raise Exception('Cart not found')

    @staticmethod
    def remove_product_from_cart(cart_id, product_id):
        cart = Cart.query.get(cart_id)
        # Check if the cart exists
        if cart != None:
            # Check if any unit of the product is in the cart
            cart_product = CartProductLink.query.filter_by(
                cart_id=cart.id, product_id=product_id).first()
            if cart_product != None:
                # Remove product from cart and delete the relation if units reach zero
                cart_product.units = cart_product.units - 1
                if cart_product.units == 0:
                    db.session.delete(cart_product)
                # Increase the product's stock on the store
                store_product = ProductStoreLink.query.filter_by(
                    store_id=cart_id, product_id=product_id).first()
                if store_product != None:
                    store_product.stock = store_product.stock + 1
                db.session.add(cart)
                db.session.commit()
                return cart
            else:
                raise Exception(
                    'This cart does not have any unit of this product')
        else:
            raise Exception('Cart not found')
