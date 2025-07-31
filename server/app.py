from flask import Flask, render_template_string
from flask_migrate import Migrate
from server.models import db, Animal, Zookeeper, Enclosure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/animal/<int:id>")
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    html = f"""
<ul>Name: {animal.name}</ul>
<ul>Species: {animal.species}</ul>
<ul>ID: {animal.id}</ul>
<ul>Zookeeper: {animal.zookeeper.name if animal.zookeeper else "None"}</ul>
<ul>Enclosure: {animal.enclosure.environment if animal.enclosure else "None"}</ul>
"""
    return render_template_string(html)


@app.route("/zookeeper/<int:id>")
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id) 
    animals_list = "".join(
        [f"<ul>{animal.name} ({animal.species})</ul>" for animal in zookeeper.animals]
    ) or "<ul>None (None)</ul>"

    html = f"""
<ul>Name: {zookeeper.name}</ul>
<ul>Birthday: {zookeeper.birthday}</ul>
<ul>ID: {zookeeper.id}</ul>
<ul>Animals:</ul>
{animals_list}
"""
    return render_template_string(html)


@app.route("/enclosure/<int:id>")
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    animals_list = "".join(
        [f"<ul>{animal.name} ({animal.species})</ul>" for animal in enclosure.animals]
    ) or "<ul>None (None)</ul>"
    html = f"""
<ul>Environment: {enclosure.environment}</ul>
<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
<ul>ID: {enclosure.id}</ul>
<ul>Animals:</ul>
{animals_list}
"""
    return render_template_string(html)


if __name__ == "__main__":
    app.run(debug=True)
