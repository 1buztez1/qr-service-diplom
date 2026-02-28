from app import create_app, db
from app.models import User, Group, TechGroup, Tech, Status
import sys
from flask_migrate import upgrade

sys.dont_write_bytecode = True
app = create_app()

def first_insert():
    with app.app_context():
        upgrade()
        selectGroup = Group.query.all()
        if len(selectGroup) == 0:
            try:
                print('Starting insertion process...')
                print('Inserting default groups and admin user...')
                group1 = Group(id=1, g_name="Администратор")
                group2 = Group(id=2, g_name="Пользователь")
                db.session.add(group1)
                db.session.add(group2)
                db.session.commit()
                user = User(username='admin', email='admin@qr-service.ru', l_name='root', f_name='root', m_name='root', group_id=1)
                user.set_password('admin')
                db.session.add(user)
                db.session.commit()
                print('Inserting default tech groups and statuses...')
                tg1 = TechGroup(group_name="Принтер")
                tg2 = TechGroup(group_name="Картридж")
                tg3 = TechGroup(group_name="Ноутбук")
                tg4 = TechGroup(group_name="Монитор")
                tg5 = TechGroup(group_name="ПК")
                db.session.add(tg1)
                db.session.add(tg2)
                db.session.add(tg3)
                db.session.add(tg4)
                db.session.add(tg5)
                db.session.commit()

                # t1 = Tech(tech_group_id=1, tech_name='HP laserjet', description='null', serial_number='123123123', status_id=1)
                # t2 = Tech(tech_group_id=1, tech_name='Kyocera laserjet', description='null', serial_number='32321231234', status_id=1)
                # t3 = Tech(tech_group_id=2, tech_name='A85-kx', description='null', serial_number='8754367514', status_id=1)
                # db.session.add(t1)
                # db.session.add(t2)
                # db.session.add(t3)
                # db.session.commit()
                s1 = Status(status_name='Работает')
                s2 = Status(status_name='Требует внимания')
                s3 = Status(status_name='Неисправен')
                s4 = Status(status_name='В ремонте')
                db.session.add(s1)
                db.session.add(s2)
                db.session.add(s3)
                db.session.add(s4)
                db.session.commit()
            except Exception as e:
                print(f'Error occurred: {e}')
            finally:
                print('Insertion process completed.')

if __name__ == "__main__":
    first_insert()