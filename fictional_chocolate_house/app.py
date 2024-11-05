from flask import render_template, request, redirect, url_for, flash
from app import create_app
from app.main import FictionalChocoHouse

# Create the Flask application using the factory
app = create_app()
db = FictionalChocoHouse()

# HOME route
@app.route('/')
def index():
    try:
        flavours = db.get_all_flavours()
        ingredients = db.get_all_ingredients()
        suggestions = db.get_all_suggestions()
        return render_template('index.html', 
                             flavours=flavours, 
                             ingredients=ingredients, 
                             suggestions=suggestions)
    except Exception as e:
        flash(f'Error loading data: {str(e)}', 'error')
        return render_template('index.html', 
                             flavours=[], 
                             ingredients=[], 
                             suggestions=[])

# Route to add new flavour
@app.route('/add_flavour', methods=['POST'])
def add_flavour():
    try:
        name = request.form['name']
        description = request.form['description']
        is_seasonal = request.form.get('is_seasonal', 'off') == 'on'
        season = request.form['season'] if is_seasonal else None
        db.add_flavour(name, description, is_seasonal, season)
        flash('Flavour added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding flavour: {str(e)}', 'error')
    return redirect(url_for('index'))

# Route to add new ingredient
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    try:
        name = request.form['name']
        quantity = int(request.form['quantity'])
        unit = request.form['unit']
        allergen_info = request.form.get('allergen_info')
        db.add_ingredient(name, quantity, unit, allergen_info)
        flash("Ingredient added successfully", 'success')
    except ValueError:
        flash("Invalid quantity value", 'error')
    except Exception as e:
        flash(f'Error adding ingredient: {str(e)}', 'error')
    return redirect(url_for('index'))

# Route to add a customer suggestion
@app.route('/add_suggestion', methods=['POST'])
def add_suggestion():
    try:
        flavour_name = request.form['flavour_name']
        description = request.form['description']
        allergen_concerns = request.form.get('allergen_concerns')
        db.add_suggestion(flavour_name, description, allergen_concerns)
        flash('Suggestion added successfully!!', 'success')
    except Exception as e:
        flash(f'Error adding suggestion: {str(e)}', 'error')
    return redirect(url_for('index'))

# Route to update suggestion status
@app.route('/update_suggestion/<int:suggestion_id>', methods=['POST'])
def update_suggestion(suggestion_id):
    try:
        new_status = request.form['status']
        db.update_suggestion_status(suggestion_id, new_status)
        flash('Suggestion status updated!!', 'success')
    except Exception as e:
        flash(f'Error updating suggestion: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    print("Starting the Flask application!")
    app.run(debug=True)

    