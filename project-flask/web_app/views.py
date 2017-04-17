from web_app import app
from logic import file#.pyfile name
from flask import render_template
from .forms import searchFlight

@app.route('/')
@app.route('/index')
def index():
    user = {}#"{'nickname': 'Juan'}  # fake user
    posts =[]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = searchFlight()
    if form.validate_on_submit():
        #print type(form.dest_date.data) #,form.dep_place,form.dest_date,form.dest_place
        dep_place=form.dep_place.data
        dest_place=form.dest_place.data
        dep_date=alg_exec.parse_date(form.dep_date.data)
        dest_date=alg_exec.parse_date(form.dest_date.data)
        names,min_itin,base_carrier_name=alg_exec.run_alg(dep_place,dest_place,dep_date,dest_date)
        return render_template('result.html',
        cities=names,
        min_itin=min_itin,
        carr_names=base_carrier_name)
    return render_template('search.html',form=form)


