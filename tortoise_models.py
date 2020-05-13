from tortoise import fields
from tortoise.models import Model



class StatePlayer(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    pers_nick = fields.CharField(max_length=30)
    pers_gender = fields.IntField() #Man - 0; Women - 1
    date_reg = fields.BigIntField()
    cordinat_x = fields.IntField(Default=2112)
    cordinat_y = fields.IntField(Default=2048)
    pers_loc = fields.IntField(Default=0) #Where is the player
    located_in_mult = fields.IntField(Default=0) #Now player in multipayer or not 0/1.If number 3, then multipayer forbidden
    time_end_bann = fields.BigIntField(Default=0)
    type_step = fields.IntField(Default=0) #Old step
    strength_arm_head = fields.IntField(Default=130)
    strength_arm_vest = fields.IntField(Default=40)
    strength_arm_gloves = fields.IntField(Default=20)
    strength_arm_pant = fields.IntField(Default=25)
    strength_arm_footwears = fields.IntField(Default=24)
    protect_arm = fields.IntField(Defaul=17)
    weapon_clogging = fields.IntField(Default=61)
    weapon_catridge = fields.IntField(Default=6)
    time_reload_weapon = fields.BigIntField(Default=0)
    now_health = fields.IntField(Default=57)
    max_health = fields.IntField(Default=100)
    now_satiety = fields.IntField(Default=72)
    max_satiety = fields.IntField(Default=100)
    now_dehydration = fields.IntField(Default=30)
    max_dehydration = fields.IntField(Default=100)
    now_cheerfulness = fields.IntField(Default=56)
    max_cheerfulness = fields.IntField(Default=100)
    now_radioactivity = fields.IntField(Default=76)
    max_radioactivity = fields.IntField(Default=100)
    now_exp = fields.IntField(Default=0)
    now_lvl = fields.IntField(Default=1)
    now_common_balance = fields.IntField(Default=500)
    now_donate_balance = fields.IntField(Default=0)
    work = fields.IntField(Default=0)
    count_common_bilets = fields.IntField(Default=3)
    count_gold_bilets = fields.IntField(Default=1)
    max_energy_player = fields.IntField(Default=10)
    now_energy_player = fields.IntField(Default=3)
    indicator_mailing = fields.IntField(Default=1)
    view_react_bot = fields.IntField(Default=1) #Type view reaction bot - image/text - 1/0
    status_player = fields.IntField(Default=0)
    status_learning = fields.IntField(Default=0)
    conn_type_sess = fields.IntField(Default=0)
    ban_report = fields.IntField(Default=0)
    ban_mult = fields.IntField(Default=0)
    comment_donate = fields.IntField(Default=0)

    class Meta:
        database = "player_database"

class PlayerRocket(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    type_rocket = fields.IntField(Default=0)
    name_rocket = fields.CharField(max_length=30)
    now_fuel = fields.BigIntField(Default=3000)
    now_build = fields.IntField(Default=2)
    max_build = fields.IntField(Default=2)
    place_builds = fields.JSONField() #1 - num place object; 2 - type object

    class Meta:
        database = "player_rocket"

class BuildingBase(Model):
    id = fields.IntField(pk=True)
    person_id = fields.IntField()
    id_building = fields.IntField()
    id_place_building = fields.IntField()
    id_type_building = fields.IntField() #Type building - building/trigger
    cordinat_x1 = fields.IntField()
    cordinat_y1 = fields.IntField()
    cordinat_x2 = fields.IntField()
    cordinat_y2 = fields.IntField()

    class Meta:
        database = "building_base"

class PlayerInventory(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    pers_nick = fields.CharField(max_length=30)
    backpack_type = fields.IntField(Default=0)
    backpack_cells = fields.JSONField()#1 - type object; 2 - count_object
    weapon_type = fields.IntField(Default=1)
    armor_head = fields.IntField(Default=1)
    armor_vest = fields.IntField(Default=1)
    armor_gloves = fields.IntField(Default=1)
    armor_pant = fields.IntField(Default=1)
    armor_footwears = fields.IntField(Default=1)

    class Meta:
        database = "player_inventory"

class SendMessChat(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    pers_nick = fields.CharField(max_length=30)
    message_id = fields.IntField()
    message_text = fields.IntField()
    message_date = fields.IntField()
    message_post_time = fields.IntField()
    message_type = fields.IntField(Default=0) #GLOBAL/LOCAL/PRIVATE
    whom_to_send = fields.IntField() #If message_type = 2 Then whom_to_send = recipient_id

    class Meta:
        database = "chat_multiplayer"

class PlayerSettings(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    pers_nick = fields.CharField(max_length=30)
    view_type_mess = fields.IntField(Default=0)
    view_quests = fields.IntField(Default=1)
    type_show_chat = fields.IntField(Default=0)
    shrifts_all = fields.IntField(Default=0)

    class Meta:
        database = "player_settings"

class SessionDate(Model):
    id = fields.IntField(pk=True)
    sess_name = fields.CharField(max_length=30)
    battle_category = fields.IntField(Default=0)#0 - PVE or 1 - PVP
    list_player_id = fields.JSONField()
    max_seats_session = fields.IntField(Default=100)
    now_seats_session = fields.IntField(Default=0)

    class Meta:
        database = "player_settings"

class PlayerBranch(Model):
    id = fields.IntField(pk=True)
    pers_id = fields.IntField()
    branch = fields.CharField(20)
    context = fields.CharField(255)

    class Meta:
        database = "branch_database"