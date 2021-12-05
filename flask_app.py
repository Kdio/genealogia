import os
import unidecode
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField("", validators=[DataRequired()])
    submit = SubmitField('Pesquisar')

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    results = []
    name = ''
    if form.validate_on_submit():
        name = form.name.data
        length = len(name)
        folder = os.getcwd() + "/www.genealogiabrasileira.com"
        for root, dirs, files in os.walk(folder):
            for file in files:
                string = open(os.path.join(root, file), 'r').read()
                position = unidecode.unidecode(string.lower()).find(unidecode.unidecode(name.lower()))
                if position > 0:
                    left, right = string[: position][-100:], string[position + length :][:100]
                    url = os.path.join(root, file).split('www.genealogiabrasileira.com')[1]
                    url = 'http://relei.tec.br/websites/www.genealogiabrasileira.com/' + url
                    results.append([url, left, right])
                    form.name.data = ""
        if results == []:
            message = "Texto não encontrado."
    return render_template('index.html', results=results, form=form, message=message, name=name)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
