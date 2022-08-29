url_path = 'http://127.0.0.1:5000'
mcskill_url_staff = 'https://mcskill.net/api/v2/?section=admin&action=get_crew'
permissions = {
    'Access to private logs': 'Доступ к приватным логам Ультимы',
    'Access to adminPanel': 'Доступ к админ панели',
    'Access edit roles': 'Доступ к созданию/Редактированию/Удалению ролей',
    'Access create user': 'Доступ создавать пользователей',
    'Access edit users roles': 'Доступ к изменению ролей у пользователей'
}
private_routes = {
    'admin_panel': {
        'name': 'Админ панель',
        'perm': 'Access to adminPanel'
    },
    'private_logs': {
        'name': 'Приватные логи',
        'perm': 'Access to private logs'
    }
}
public_routes = {
    'public_logs': 'Публичные логи',
    'activity_check': 'Игровая активность'
}
admin_panel_routes = {
    'edit_roles': {
        'name': 'Редактирование ролей',
        'perm': 'Access edit roles'
    },
    'create_user': {
        'name': 'Создание пользователя',
        'perm': 'Access create user'
    },
    'edit_user_roles': {
        'name': 'Редактирование ролей у пользователей',
        'perm': 'Access edit users roles'
    }
}
public_logs_servers_list = [
    'UltimaTech',
    'HitechCraft_Titan',
    'HitechCraft_Phobos',
    'HitechCraft_Elara'
]
route_data = {
    'public_routes': public_routes,
    'private_routes': private_routes,
    'admin_panel': admin_panel_routes,
    'url_path': url_path,
    'permissions': permissions
}
private_logs_servers_list = [
    'UltimaTech'
]
download_logs_url = {
    'HitechCraft_Titan': 'https://logs12.mcskill.net/Hitechcraft_public_logs/',
    'HitechCraft_Phobos': 'https://logs12.mcskill.net/Hitechcraft2_public_logs/',
    'HitechCraft_Elara': 'https://logs12.mcskill.net/Hitechcraft3_public_logs/'
}
colors_codes = {
    '[30;22m': '<span style="color: #000000;">',  # §0 - Black
    '[34;22m': '<span style="color: #0000AA;">',  # §1 - Dark_Blue
    '[32;22m': '<span style="color: #00AA00;">',  # §2 - Dark_Green
    '[36;22m': '<span style="color: #00AAAA;">',  # §3 - Dark_Aqua
    '[31;22m': '<span style="color: #AA0000;">',  # §4 - Dark_Red
    '[35;22m': '<span style="color: #AA00AA;">',  # §5 - Purple
    '[33;22m': '<span style="color: #FFAA00;">',  # §6 - Gold
    '[37;22m': '<span style="color: #AAAAAA;">',  # §7 - Gray
    '[30;1m': '<span style="color: #555555;">',  # §8 - Dakr_Gray
    '[34;1m': '<span style="color: #5555FF;">',  # §9 - Blue
    '[32;1m': '<span style="color: #55FF55;">',  # §a - Green
    '[36;1m': '<span style="color: #55FFFF;">',  # §b - Aqua
    '[31;1m': '<span style="color: #FF5555;">',  # §c - Red
    '[35;1m': '<span style="color: #FF55FF;">',  # §d - Light_Purple
    '[33;1m': '<span style="color: #FFFF55;">',  # §e - Yellow
    '[37;1m': '<span style="color: #FFFFFF;">',  # §f - White
    '[0;30;22m': '<span style="color: #000000;">',  # §0 - Black
    '[0;34;22m': '<span style="color: #0000AA;">',  # §1 - Dark_Blue
    '[0;32;22m': '<span style="color: #00AA00;">',  # §2 - Dark_Green
    '[0;36;22m': '<span style="color: #00AAAA;">',  # §3 - Dark_Aqua
    '[0;31;22m': '<span style="color: #AA0000;">',  # §4 - Dark_Red
    '[0;35;22m': '<span style="color: #AA00AA;">',  # §5 - Purple
    '[0;33;22m': '<span style="color: #FFAA00;">',  # §6 - Gold
    '[0;37;22m': '<span style="color: #AAAAAA;">',  # §7 - Gray
    '[0;30;1m': '<span style="color: #555555;">',  # §8 - Dakr_Gray
    '[0;34;1m': '<span style="color: #5555FF;">',  # §9 - Blue
    '[0;32;1m': '<span style="color: #55FF55;">',  # §a - Green
    '[0;36;1m': '<span style="color: #55FFFF;">',  # §b - Aqua
    '[0;31;1m': '<span style="color: #FF5555;">',  # §c - Red
    '[0;35;1m': '<span style="color: #FF55FF;">',  # §d - Light_Purple
    '[0;33;1m': '<span style="color: #FFFF55;">',  # §e - Yellow
    '[0;37;1m': '<span style="color: #FFFFFF;">',  # §f - White
    '[5m': '',  # Obfuscated
    '[21m': '<b>',  # Bold
    '[9m': '<s>',  # Strikethrough
    '[4m': '<u>',  # Underline
    '[3m': '<i>',  # Italic
    '[0;39m': '</b></s></u></i></span>',  # Reset
    '[0m': '</b></s></u></i></span>',  # Reset
    '[m': '</b></s></u></i></span>'  # End
}
staff_settings = {
    'helper1': {
        'view': True,
        'color': '#51cf89'
    },
    'helper2': {
        'view': True,
        'color': '#26a65b'
    },
    'moder': {
        'view': True,
        'color': '#9400d3'
    },
    'stmoder': {
        'view': False,
        'color': '#446CB3'
    },
    'gm': {
        'view': False,
        'color': '#0183D7'
    },
    'gd': {
        'view': False,
        'color': '#0183D7'
    },
    'curator': {
        'view': False,
        'color': 'red'
    },
    'admin': {
        'view': False,
        'color': 'red'
    },
    'techadmin': {
        'view': False,
        'color': '#00CCFF'
    }
}
invalids = {
    'HiTech #1 1.7.10 - Titan': 'HitechCraft_Titan',
    'HiTech #2 1.7.10 - Phobos': 'HitechCraft_Phobos',
    'HiTech #3 1.7.10 - Elara': 'HitechCraft_Elara'
}
