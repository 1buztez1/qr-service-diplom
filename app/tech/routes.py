from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.tech import bp
from app.models import Tech, QR_codes, Comment, TechGroup, Status
from app.tech.forms import AddDeviceForm
from app import db

from config import Config


@bp.route('/view_tech/<id>',  methods=['GET', 'POST'])
@login_required
def view_tech(id):
    tech = Tech.query.filter_by(id=id).first_or_404()
    qr_code = tech.qr_codes.filter_by(is_active=True).first()
    qr_code_base64 = qr_code.qr_data if qr_code else None
    comments_count = tech.comments.count()
    comments = tech.comments.order_by(Comment.created_at.desc()).all()
    return render_template('main/view_tech.html', tech=tech, qr_code_base64=qr_code_base64, comments_count=comments_count, comments=comments)


@bp.route('/generate_qr/<int:tech_id>', methods=['POST'])
@login_required
def generate_qr(tech_id):
    tech = Tech.query.get_or_404(tech_id)
    qr_code = QR_codes(tech_id=tech.id, qr_data='', created_by=current_user.id)
    qr_code.generate_and_store(Config.QR_URL + str(tech.id))
    from app import db
    db.session.add(qr_code)
    db.session.commit()
    flash('QR-код успешно создан!')
    return redirect(url_for('tech.view_tech', id=tech_id))


@bp.route('/add_comment/<int:tech_id>', methods=['POST'])
@login_required
def add_comment(tech_id):
    tech = Tech.query.get_or_404(tech_id)
    content = request.form.get('content')
    if content:
        comment = Comment(tech_id=tech.id, content=content, created_by=current_user.id)
        from app import db
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен!')
    return redirect(url_for('tech.view_tech', id=tech_id))

@bp.route('/change_status/<int:tech_id>/<int:status_id>', methods=['POST'])
@login_required
def change_status(tech_id, status_id):
    tech = Tech.query.get_or_404(tech_id)
    status = Status.query.get_or_404(status_id)
    
    tech.status_id = status_id
    db.session.commit()
    flash(f'Статус устройства изменен на "{status.status_name}"!')
    return redirect(url_for('tech.view_tech', id=tech_id))


@bp.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    # Проверяем, что пользователь имеет права администратора
    if current_user.group_id != 1:
        flash('У вас нет прав для добавления устройств.')
        return redirect(url_for('main.index'))
    
    form = AddDeviceForm()
    form.tech_group_id.choices = [(g.id, g.group_name) for g in TechGroup.query.all()]
    form.status_id.choices = [(s.id, s.status_name) for s in Status.query.all()]
    
    if form.validate_on_submit():
        tech = Tech(
            tech_name=form.tech_name.data,
            description=form.description.data,
            serial_number=form.serial_number.data,
            tech_group_id=form.tech_group_id.data,
            status_id=form.status_id.data
        )
        db.session.add(tech)
        db.session.commit()
        flash('Устройство успешно добавлено!')
        return redirect(url_for('main.index'))
    
    return render_template('tech/add_device.html', form=form)