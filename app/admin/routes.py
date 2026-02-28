from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.admin import bp
from app.models import User, Group, db
from app.admin.forms import AddUserForm

@bp.route('/users')
@login_required
def users():
    # Проверяем, что пользователь имеет права администратора
    if current_user.group_id != 1:
        flash('У вас нет прав для просмотра пользователей.')
        return redirect(url_for('main.index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # Проверяем, что пользователь имеет права администратора (предполагаем, что group_id=1 - админ)
    if current_user.group_id != 1:
        flash('У вас нет прав для добавления пользователей.')
        return redirect(url_for('main.index'))
    
    form = AddUserForm()
    form.group_id.choices = [(g.id, g.g_name) for g in Group.query.all()]
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            l_name=form.l_name.data,
            f_name=form.f_name.data,
            m_name=form.m_name.data,
            group_id=form.group_id.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь успешно добавлен!')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/add_user.html', form=form)