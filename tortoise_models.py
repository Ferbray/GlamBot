from tortoise import fields
from tortoise.models import Model

'''Explanation fields - 1

Location - Inventory/feature_armors;

Type - List of lists;

Index list: 
0 - head;
1 - vest; 
2 - gloves; 
3 - trousers; 
4 - shoes

Index lists:
0 - id;
1 - strength;
2 - protection;

Example:
[
    [1, 67, 23],
    [4, 32, 55],
    [0, 0, 0],
    [3, 90, 30],
    [10, 12, 230]
]

'''

'''Explanation fields - 2

Location - Rocket/places_free;

Type - List of lists;

Index list: 
It is created when a rocket is purchased, depending on its characteristics.

Index lists:
0 - cordinat x;
1 - cordinat y;
2 - size place - It's default sizes - .../.../...
3 - type of construction: Default - 0

Example:
[
    [100, 167, 23, 0],
    [532, 50, 15, 1],
    [907, 0, 5]
]

'''

'''Explanation fields - 3

Location - SendMessChat/feature_message;

Type - List;

Index list: 

0 - id;
1 - text; 
2 - date; 
3 - type: GLOBAL/LOCAL/PRIVATE; 
4 - whom: If type = 2 Then whom_to_send = recipient_id
5 - user_nick

Example:
[
    666,
    "Hello multiplayer",
    [14.05.2020:17:40],
    type: Global
    Whom: 0
]

'''

class Main(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    user_nick = fields.CharField(max_length=30)
    user_gender = fields.IntField() #Man - 0; Women - 1
    date_reg = fields.BigIntField()

    user_status = fields.IntField(default=0)
    user_progress = fields.JSONField() #Type list; Index: 0 - exp; 1 - lvl
    user_balance = fields.JSONField() #Type list; Index: 0 - common; 1 - donate
    user_location = fields.IntField(default=1) #1,2, ... - Loc Multiplayer; 0 - Multiplayer forbidden

    timeout_ban1 = fields.BigIntField(default=0) #Timeout of multiplayer ban
    timeout_ban2 = fields.BigIntField(default=0) #Timeout of report ban
    payment_state = fields.JSONField() #Type list; Index: 0 - ammount; 1 - id
    
    class Meta:
        database = "main"

class Multiplayer(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    session_num = fields.IntField(default=0)
    cordinat_x = fields.IntField(default=2112)
    cordinat_y = fields.IntField(default=2048)
    last_step = fields.IntField(default=0) #Need to change legs when walking

    user_protection = fields.IntField(default=17)
    user_health = fields.JSONField() #Type list; Index: 0 - now health; 1 - max health
    user_satiety = fields.JSONField()
    user_dehydration = fields.JSONField()
    user_cheerfulness = fields.JSONField()
    user_radioactivity = fields.JSONField()
    user_energy = fields.JSONField()
    user_tickets = fields.JSONField() #Type list; Index: 0 - common; 1 - gold

    class Meta:
        database = "multiplayer"

class Rocket(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    rocket_id = fields.IntField(default=0)
    rocket_name = fields.CharField(max_length=30)
    rocket_fuel = fields.BigIntField(default=3000)
    places_free = fields.JSONField() #Explanations above

    class Meta:
        database = "rocket"

class Building(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    build_id = fields.IntField()
    building_place = fields.IntField()
    building_type = fields.IntField() #Building/trigger
    building_cordinats = fields.JSONField() #Type list; Index: 0 - x1; 1 - y1; 2 - x2; 3 - y2

    class Meta:
        database = "building"

class Inventory(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    
    gun_type = fields.IntField(default=1)
    gun_clogging = fields.IntField(default=61)
    gun_magazine = fields.IntField(default=6)
    timeout_reload = fields.BigIntField(default=0) #Timeout of reload gun
    feature_armors = fields.JSONField() #Explanations above

    backpack_type = fields.IntField(default=1)
    backpack_cells = fields.JSONField() #Type list of lists; Index lists 0 - type object; 1 - count_object

    class Meta:
        database = "inventory"

class MessChat(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()
    feature_message = fields.JSONField() #Explanations above

    class Meta:
        database = "mess_chat"

class Settings(Model):
    id = fields.IntField(pk=True)

    user_id = fields.IntField()

    mailing_permission = fields.IntField(default=1) #On - 1; Off - 0
    study_permission = fields.IntField(default=1)
    answer_options = fields.IntField(default=1) #Type view reaction bot - image/text - 1/0

    show_chat = fields.IntField(default=0)
    permission_tips = fields.IntField(default=1)
    chat_type = fields.IntField(default=0)
    installed_font = fields.IntField(default=0)

    class Meta:
        database = "settings"

class Session(Model):
    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=30)
    category = fields.IntField(default=0)#0 - PVE or 1 - PVP
    players_id = fields.JSONField() #Type list

    class Meta:
        database = "session"

class MultiplayerBranch(Model):
    id = fields.IntField(pk=True)

    pers_id = fields.IntField()
    branch = fields.CharField(20)
    context = fields.CharField(255)

    class Meta:
        database = "branch_database"