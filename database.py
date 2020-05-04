import asyncio, asyncpg

async def connection():
	conn = await asyncpg.connect(user='glamuser', password='GisMyVoron1974', database='glamdata', host='127.0.0.1')
	await conn.execute("CREATE TABLE IF NOT EXISTS player_database ("
		"person_id integer,"
		"nickname VARCHAR,"
		"gender_player integer,"#Man - 0; Women - 1
		"date_registration integer,"
		"cordinat_x integer,"
		"cordinat_y integer,"
		"location_person integer,"#Where is the player
		"availability_in_mult integer,"#Now player in multipayer or not 0/1.If number 3, then multipayer forbidden
		"time_end_banned integer,"#Default - 0
		"type_step integer,"#Old step
		"strength_armor_head integer,"
		"strength_armor_breastplate integer,"
		"strength_armor_gloves integer,"
		"strength_armor_footwears integer,"
		"armor_protection integer,"
		"weapon_clogging integer,"
		"weapon_catridge_clip_now integer,"
		"weapon_reload_time integer,"
		"now_health integer,"
		"max_health integer,"
		"now_satiety integer,"
		"max_satiety integer,"
		"now_dehydration integer,"
		"max_dehydration integer,"
		"now_exp integer,"
		"max_exp integer,"
		"now_lvl integer,"
		"now_standart_balance integer,"
		"now_donate_balance integer,"
		"work integer,"
		"count_standart_bilets integer,"
		"count_gold_bilets integer,"
		"max_energy_player integer,"
		"now_energy_player integer,"
		"indicator_mailing integer,"#Defaul - 1/On
		"view_reaction_bot integer,"#Type view reaction bot - image/text - 1/0
		"status_player integer)")#Default - 0 / junior

	await conn.execute("CREATE TABLE IF NOT EXISTS player_rocket ("
		"...,"
		"...)")

	await conn.execute("CREATE TABLE IF NOT EXISTS building_base ("
		"id_building integer,"
		"id_building_person integer,"
		"id_place_building integer,"
		"id_type_building integer," #Type building - building/trigger
		"cordinat_first_x integer,"
		"cordinat_first_y integer,"
		"cordinat_second_x integer,"
		"cordinat_second_y integer)")

	await conn.execute("CREATE TABLE IF NOT EXISTS player_inventory ("
		"person_id integer,"
		"nickname VARCHAR,"
		"backpack_type integer,"
		"backpack_cells integer[][],"#1 - type object; 2 - count_object
		"weapon_type integer,"
		"armor_head integer,"
		"armor_breastplate integer,"
		"armor_gloves integer,"
		"armor_footwears integer)")

	await conn.execute("CREATE TABLE IF NOT EXISTS chat_multiplayer ("
		"player_id int,"
		"player_nickname VARCHAR,"
		"message_id int,"
		"message_text VARCHAR,"
		"message_date VARCHAR,"
		"message_post_time integer,"
		"message_type VARCHAR,"#Default - 0 GLOBAL/LOCAL/PRIVATE
		"whom_to_send integer)")#If message_type = 2 Then whom_to_send = recipient_id

	await conn.execute("CREATE TABLE IF NOT EXISTS settings ("
		"player_id int,"
		"nickname VARCHAR,"
		"accept_type_chat_mess integer,"#Def - 0/Mixed
		"type_show_chat integer,"
		"shrifts_all integer)")

	print("Executed")

	await conn.fetch("SELECT * FROM player_database")
	print("Fetched")

	await conn.close()

asyncio.get_event_loop().run_until_complete(connection())
