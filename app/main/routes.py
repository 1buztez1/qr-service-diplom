from flask import render_template
from flask_login import login_required

from app.main import bp
from app.models import Tech

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    tech = Tech.query.all()
    filtered_tech_1 = [t for t in tech if t.status_id == 1] 
    filtered_tech_2 = [t for t in tech if t.status_id == 2] 
    filtered_tech_3 = [t for t in tech if t.status_id == 3] 

    return render_template('main/index.html', count_tech = len(tech),
                           count_tech_1=len(filtered_tech_1),
                           count_tech_2=len(filtered_tech_2),
                           count_tech_3=len(filtered_tech_3),
                           tech=tech)