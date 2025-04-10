from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from module_admin.entity.do.menu_do import SysMenu
from datetime import datetime

engine = create_engine('sqlite:///test_database.db')
Session = sessionmaker(bind=engine)
session = Session()

ai_menu = session.query(SysMenu).filter(SysMenu.path == '/ai').first()
if not ai_menu:
    ai_menu = SysMenu(
        menu_name='AI管理',
        parent_id=0,
        order_num=5,
        path='/ai',
        component=None,
        is_frame=1,
        is_cache=0,
        menu_type='M',
        visible='0',
        status='0',
        perms='',
        icon='robot',
        create_by='admin',
        create_time=datetime.now(),
        remark='AI模块'
    )
    session.add(ai_menu)
    session.flush()  # Flush to get the menu_id
    
    provider_menu = SysMenu(
        menu_name='AI提供商',
        parent_id=ai_menu.menu_id,
        order_num=1,
        path='provider',
        component='ai/provider/index',
        route_name='Provider',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='ai:provider:list',
        icon='cloud',
        create_by='admin',
        create_time=datetime.now(),
        remark='AI提供商管理'
    )
    session.add(provider_menu)
    
    model_menu = SysMenu(
        menu_name='AI模型',
        parent_id=ai_menu.menu_id,
        order_num=2,
        path='model',
        component='ai/model/index',
        route_name='Model',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='ai:model:list',
        icon='component',
        create_by='admin',
        create_time=datetime.now(),
        remark='AI模型管理'
    )
    session.add(model_menu)
    
    assistant_menu = SysMenu(
        menu_name='AI助手',
        parent_id=ai_menu.menu_id,
        order_num=3,
        path='assistant',
        component='ai/assistant/index',
        route_name='Assistant',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='ai:assistant:list',
        icon='people',
        create_by='admin',
        create_time=datetime.now(),
        remark='AI助手管理'
    )
    session.add(assistant_menu)
    
    chat_menu = SysMenu(
        menu_name='对话',
        parent_id=ai_menu.menu_id,
        order_num=4,
        path='chat',
        component='ai/chat/index',
        route_name='Chat',
        is_frame=1,
        is_cache=0,
        menu_type='C',
        visible='0',
        status='0',
        perms='ai:chat:list',
        icon='message',
        create_by='admin',
        create_time=datetime.now(),
        remark='AI对话'
    )
    session.add(chat_menu)
    
    provider_query = SysMenu(
        menu_name='提供商查询',
        parent_id=provider_menu.menu_id,
        order_num=1,
        path='',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='ai:provider:query',
        icon='#',
        create_by='admin',
        create_time=datetime.now()
    )
    session.add(provider_query)
    
    provider_add = SysMenu(
        menu_name='提供商新增',
        parent_id=provider_menu.menu_id,
        order_num=2,
        path='',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='ai:provider:add',
        icon='#',
        create_by='admin',
        create_time=datetime.now()
    )
    session.add(provider_add)
    
    provider_edit = SysMenu(
        menu_name='提供商修改',
        parent_id=provider_menu.menu_id,
        order_num=3,
        path='',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='ai:provider:edit',
        icon='#',
        create_by='admin',
        create_time=datetime.now()
    )
    session.add(provider_edit)
    
    provider_remove = SysMenu(
        menu_name='提供商删除',
        parent_id=provider_menu.menu_id,
        order_num=4,
        path='',
        component='',
        is_frame=1,
        is_cache=0,
        menu_type='F',
        visible='0',
        status='0',
        perms='ai:provider:remove',
        icon='#',
        create_by='admin',
        create_time=datetime.now()
    )
    session.add(provider_remove)
    
    for menu, prefix in [(model_menu, 'model'), (assistant_menu, 'assistant'), (chat_menu, 'chat')]:
        for action, name, order in [
            ('query', '查询', 1),
            ('add', '新增', 2),
            ('edit', '修改', 3),
            ('remove', '删除', 4)
        ]:
            button = SysMenu(
                menu_name=f'{menu.menu_name}{name}',
                parent_id=menu.menu_id,
                order_num=order,
                path='',
                component='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'ai:{prefix}:{action}',
                icon='#',
                create_by='admin',
                create_time=datetime.now()
            )
            session.add(button)
    
    session.commit()
    print("AI menu items created successfully")
else:
    print("AI menu already exists")

from module_admin.entity.do.role_do import SysRoleMenu

admin_role_id = 1

ai_menu_ids = [menu.menu_id for menu in session.query(SysMenu).filter(
    SysMenu.path.like('/ai%') | 
    SysMenu.parent_id.in_([m.menu_id for m in session.query(SysMenu).filter(SysMenu.path == '/ai')])
).all()]

existing_perms = session.query(SysRoleMenu).filter(
    SysRoleMenu.role_id == admin_role_id,
    SysRoleMenu.menu_id.in_(ai_menu_ids)
).all()

existing_menu_ids = [perm.menu_id for perm in existing_perms]

for menu_id in ai_menu_ids:
    if menu_id not in existing_menu_ids:
        role_menu = SysRoleMenu(
            role_id=admin_role_id,
            menu_id=menu_id
        )
        session.add(role_menu)

session.commit()
print("AI menu permissions added to admin role")

session.close()
