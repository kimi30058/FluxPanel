from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from module_admin.entity.do.user_do import SysUser, SysUserRole
from module_admin.entity.do.role_do import SysRole
from module_admin.entity.do.dept_do import SysDept
from utils.pwd_util import PwdUtil
from datetime import datetime

engine = create_engine('sqlite:///test_database.db')
Session = sessionmaker(bind=engine)
session = Session()

admin = session.query(SysUser).filter(SysUser.user_name == 'admin').first()
if not admin:
    dept = session.query(SysDept).filter(SysDept.dept_id == 100).first()
    if not dept:
        dept = SysDept(
            dept_id=100,
            parent_id=0,
            ancestors='0',
            dept_name='测试部门',
            order_num=1,
            leader='admin',
            phone='',
            email='',
            status='0',
            del_flag='0',
            create_by='admin',
            create_time=datetime.now()
        )
        session.add(dept)
    
    admin = SysUser(
        user_id=1,
        dept_id=100,
        user_name='admin',
        nick_name='管理员',
        password=PwdUtil.get_password_hash('admin123'),
        status='0',
        del_flag='0',
        create_by='admin',
        create_time=datetime.now()
    )
    session.add(admin)
    
    role = session.query(SysRole).filter(SysRole.role_id == 1).first()
    if not role:
        role = SysRole(
            role_id=1,
            role_name='超级管理员',
            role_key='admin',
            role_sort=1,
            status='0',
            del_flag='0',
            create_by='admin',
            create_time=datetime.now()
        )
        session.add(role)
    
    user_role = SysUserRole(
        user_id=1,
        role_id=1
    )
    session.add(user_role)
    
    session.commit()
    print('Admin user created successfully')
else:
    print('Admin user already exists')

session.close()
