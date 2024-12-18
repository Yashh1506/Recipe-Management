from flask import Flask, render_template, request, url_for,send_file, redirect, Response
from flask_sqlalchemy import SQLAlchemy
import base64


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Recipe.db'
db = SQLAlchemy(app)

class Recipe(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    country=db.Column(db.String(100), nullable=False)
    cuisine=db.Column(db.String(100), nullable=False)
    prep_time=db.Column(db.Integer, nullable=False)
    cook_time=db.Column(db.Integer, nullable=False)
    serving=db.Column(db.Integer, nullable=False)
    ingredients=db.Column(db.String(1000), nullable=False)
    instructions=db.Column(db.String(1000), nullable=False)
    notes=db.Column(db.String(500), nullable=True)
    image=db.Column(db.LargeBinary, nullable=True)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'


@app.route('/')
def index():
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    return render_template('home.html',cuisine=cuisine)

@app.route('/login', methods=['GET','POST'])
def login():
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()

    return render_template('login.html',cuisine=cuisine)

@app.route('/signup')
def signup():
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    return render_template('signup.html',cuisine=cuisine)

@app.route('/new_recipe', methods=['GET','POST'])
def new_recipe():
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    if request.method=="POST":
        title=request.form['title']
        cuisine=request.form['cuisine']
        prep_time=request.form['prep_time']
        cook_time=request.form['cook_time']
        serving=request.form['serving_size']
        ingredients=request.form['ingredients']
        instructions=request.form['instructions']
        notes=request.form['notes']
        image_file = request.files['image']
        image_data = image_file.read() if image_file else None
        country=request.form['country']
        recipe=Recipe(title=title,cuisine=cuisine,prep_time=prep_time,cook_time=cook_time,serving=serving,ingredients=ingredients,instructions=instructions,notes=notes,image=image_data,country=country)
        db.session.add(recipe)
        db.session.commit()
        return redirect('/all_recipe')
    return render_template('new_recipe.html',cuisine=cuisine)



@app.route('/all_recipe')
def all_recipe():
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    all_recipe = Recipe.query.all()
    recipe_with_images=[]
    for recipe in all_recipe:
        if recipe.image:
        # Convert binary data to base64
            image_base64 = base64.b64encode(recipe.image).decode('utf-8')
            image_src = f"data:image/jpg;base64,{image_base64}"  # Replace png with the actual image type if necessary
        else:
            image_src = None
        recipe_with_images.append({'sno':recipe.sno,'image_src':image_src})
    return render_template('all_recipe.html', all_recipe=all_recipe,recipe_with_images=recipe_with_images, cuisine=cuisine)

@app.route('/recipe/<int:sno>')
def recipe(sno):
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    recipe = Recipe.query.filter_by(sno=sno).first()
    if recipe.image:
        # Convert binary data to base64
        image_base64 = base64.b64encode(recipe.image).decode('utf-8')
        image_src = f"data:image/jpg;base64,{image_base64}"  # Replace png with the actual image type if necessary
    else:
        image_src = None
    return render_template('recipe.html', recipe=recipe,image_src=image_src,cuisine=cuisine)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        cuisine=request.form['cuisine']
        prep_time=request.form['prep_time']
        cook_time=request.form['cook_time']
        serving=request.form['serving_size']
        ingredients=request.form['ingredients']
        instructions=request.form['instructions']
        notes=request.form['notes']
        image_file = request.files['image']
        image_data = image_file.read() if image_file else None
        country=request.form['country']
        updated = Recipe.query.filter_by(sno=sno).first()
        updated.title=title
        updated.cuisine=cuisine
        updated.prep_time=prep_time
        updated.cook_time=cook_time
        updated.serving=serving
        updated.ingredients=ingredients
        updated.instructions=instructions
        updated.notes=notes
        updated.image_data=image_data
        updated.country=country
        db.session.add(updated)
        db.session.commit()
        return redirect('/all_recipe')

    recipe = Recipe.query.filter_by(sno=sno).first()
    return render_template('update.html', recipe=recipe)

@app.route('/delete/<int:sno>')
def delete(sno):
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    recipe = Recipe.query.filter_by(sno=sno).first()
    db.session.delete(recipe)
    db.session.commit()
    return redirect('/all_recipe', cuisine=cuisine)

    
@app.route('/cuisine/<string:cuisine>')
def cuisine(cuisine):
    name=Recipe.query.filter_by(cuisine=cuisine)
    cuisine=db.session.query(Recipe.cuisine).order_by(Recipe.cuisine).distinct()
    recipe_with_images=[]
    for recipe in name:
        if recipe.image:
        # Convert binary data to base64
            image_base64 = base64.b64encode(recipe.image).decode('utf-8')
            image_src = f"data:image/jpg;base64,{image_base64}"  # Replace png with the actual image type if necessary
        else:
            image_src = None
        recipe_with_images.append({'sno':recipe.sno,'image_src':image_src})
    return render_template('cuisine.html', name=name,recipe_with_images=recipe_with_images,cuisine=cuisine)

if __name__=="__main__":
    app.run(debug=True)