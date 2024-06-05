from flask import Flask, request, jsonify, render_template
from collections import Counter

app = Flask(__name__)

orders = []
completed_orders = []
drinks = []
ingredients = {
    'Avocado Toast': {
        'Avocado': 0.5, 'Cucumber': 0.5, 'Cherry Tomato': 2, 'Bell Pepper': 1,
        'Fresh Baked Bread': 4, 'Sesame Seeds': 1, 'Olive Oil': 1,
        'Salt': 1, 'Pepper': 1
    },
    'Honey Banana Bowl': {
        'Banana': 1, 'Seasonal Fruit': 1, 'Honey': 2, 'Sesame Seeds': 1
    },
    'French Toast': {
        'Fresh Baked Bread': 4, 'Eggs': 2, 'Milk or Cream': 0.75,
        'Vanilla Extract': 1, 'Ground Cinnamon': 1, 'Butter': 2,
        'Banana': 1, 'Honey': 2, 'Seasonal Fruit': 1
    }
}

drink_ingredients = {
    'Brown Sugar Latte': {
        'Espresso': 1, 'Milk': 1, 'Brown Sugar': 2
    },
    'Lemonade Coffee': {
        'Espresso': 1, 'Lemonade': 1
    },
    'Espresso': {
        'Espresso': 1
    },
    'Latte': {
        'Espresso': 1, 'Milk': 1
    },
    'Cappuccino': {
        'Espresso': 1, 'Milk': 0.5, 'Foam': 0.5
    },
    'Americano': {
        'Espresso': 1, 'Water': 1
    },
    'Mocha': {
        'Espresso': 1, 'Milk': 1, 'Chocolate Syrup': 1
    }
}

@app.route('/')
def index():
    return render_template('order.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.get_json()
    name = data.get('name')
    food = data.get('food')
    drink = data.get('drink')
    note = data.get('note')

    if name and food and drink:
        orders.append({'name': name, 'food': food, 'drink': drink, 'note': note})
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/orders')
def view_orders():
    return render_template('orders.html', orders=orders)

@app.route('/complete_order', methods=['POST'])
def complete_order():
    index = int(request.form.get('index'))
    if 0 <= index < len(orders):
        completed_orders.append(orders.pop(index))
    return '', 204

@app.route('/ingredients')
def view_ingredients():
    total_ingredients = Counter()
    total_drink_ingredients = Counter()

    for order in orders:
        for ingredient, amount in ingredients[order['food']].items():
            total_ingredients[ingredient] += amount
        if order['drink'] != 'None':
            for ingredient, amount in drink_ingredients[order['drink']].items():
                total_drink_ingredients[ingredient] += amount

    return render_template('ingredients.html', ingredients=total_ingredients, drink_ingredients=total_drink_ingredients)

if __name__ == '__main__':
    app.run(debug=True)
