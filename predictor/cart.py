# cart.py in your 'shop' app
class Cart:

    def __init__(self, request):
        self.request = request
        self.cart = request.session.get('cart', {})  # Get the cart from the session

    def add(self, vegetable):
        vegetable_data = {
            'id': vegetable.id,
            'name': vegetable.name,
            'price': float(vegetable.price)
        }
        if vegetable.id not in self.cart:
            self.cart[vegetable.id] = {'quantity': 1, 'vegetable': vegetable_data}
        else:
            self.cart[vegetable.id]['quantity'] += 1
        self.save()
        print("Cart after adding:", self.cart)  # Debug line


    def remove(self, vegetable):
        print("Current cart before removal:", self.cart)  # Debug line
        if vegetable.id in self.cart:
            del self.cart[vegetable.id]
            print(f'Vegetable {vegetable.id} removed from cart.')
        else:
            print(f'Vegetable {vegetable.id} not found in cart.')
        self.save()



    def get_items(self):
        # Return a list of cart items
        return self.cart.values()

    def get_total(self):
        # Calculate total amount
        return sum(item['quantity'] * item['vegetable']['price'] for item in self.cart.values())

    def save(self):
        self.request.session['cart'] = self.cart
        print("Cart saved to session:", self.request.session['cart'])  # Debug line
