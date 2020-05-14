'''Need:
	
🔸Finish writing locations for using the tortoise module

'''

import json
import os
import shutil
import random
import re
import ssl
from time import ctime,time
from decimal import Decimal
from operator import itemgetter

from vkbottle import Bot, Message, keyboard_gen, VKError
from vkbottle.branch import ClsBranch, ExitBranch, rule_disposal, Branch
from vkbottle.rule import AbstractMessageRule, VBMLRule
from vkbottle.keyboard import Keyboard, Text
from vbml import PatchedValidators
from tortoise import Tortoise
from aiohttp import ClientSession
import asyncio
import aioqiwi

from qiwi_wrapper import qiwi_payment, qiwi_history
from tortoise_models import Main, Multiplayer, Rocket, Building, Inventory, MessChat, Settings, Session, MultiplayerBranch
from ImageEngine import ElipsAva, WritePersProfile, WriteTopPlayer

bot = Bot('9c6713c47ccc55cbbb5ba7b712c1a8a5e7c3c419da361d12f60dfd27ad3c882ed28c344b898193733989b', mobile=False)

async def get_info(upload_url: str, files: dict):
	async with ClientSession(json_serialize=json.dumps) as client:
		async with client.post(upload_url, ssl=ssl.SSLContext(), data=files) as r:
			response = await r.read()
	return json.loads(response)

async def UpPhoto(ans, img_name):
	upload_info = await bot.api.photos.get_messages_upload_server(peer_id=ans.from_id)
	upload_task = bot.loop.create_task(get_info(
		upload_info.upload_url, files={'photo': open(img_name, "rb")})
	)
	upload_result = await upload_task
	serv_xy_map = await bot.api.photos.save_messages_photo(photo=upload_result["photo"], 
														server=upload_result["server"], 
														hash=upload_result["hash"])

	xymap = "photo{}_{}".format(serv_xy_map[0].owner_id, serv_xy_map[0].id)
	return xymap

@bot.on.pre_process()
async def registration(ans: Message):
	if await StatePlayer.get_or_none(pers_id=ans.from_id) is None:
		reg_keyboard = keyboard_gen([
			[{'text':'Мужской','color':'positive'}],
			[{'text':'Женский', 'color':'primary'}]
		], inline=True)

		await ans("🔸Добро пожаловать в блок регистрации\n"
			"🔸Выберите род вашего персонажа!", 
			keyboard=reg_keyboard)#TODO ATTACHMENT
		await bot.branch.add(ans.peer_id, 'reg_branch')

@bot.branch.cls_branch("reg_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule(["Мужской","Женский"], lower=True))
	async def exit_branch(self, ans: Message):
		os.mkdir(f"PhotoDatePlayers/{ans.from_id}")
		try:
			vk = await bot.api.users.get(user_ids=ans.from_id, fields="photo_400_orig")
			async with ClientSession() as session:
				async with session.get(vk[0].photo_400_orig) as response:
					content = await response.read()

			cut_url = vk[0].photo_400_orig.split("/")[-1]
			name_ava = cut_url.split('.')[0]
			
			with open(f"PhotoDatePlayers/{ans.from_id}/{name_ava} orig_400.png", 'wb') as fh:
				fh.write(content)

		except:
			shutil.copy('materials_bot/NoPhoto orig_400.png', f"PhotoDatePlayers/{ans.from_id}")
			await ans("У вас нет аватарки, вам временно поставлена эта!", attachment="photo-191374726_457239031")
			name_ava = "NoPhoto"

		ElipsAva(ans.from_id, name_ava)
		vk_name = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name

		current_time = round(time())
		gender_player = (1 if ans.text=='Женский' else 0)

		WritePersProfile([
			vk_name, str(ans.from_id), "500",
			"0", "57", "76", "72", 
			"30", "56", "17"
		])

		await StatePlayer.create(
			pers_id=ans.from_id, 
			pers_nick=vk_name, 
			pers_gender=gender_player,
			date_reg=current_time
		)
		

		await PlayerRocket.create(
			pers_id=ans.from_id, 
			name_rocket='Тритон 8',
			place_builds = json.dumps([
				[0, 0],
				[1001, 1]
			])
		)

		await PlayerInventory.create(
			pers_id=ans.from_id, 
			pers_nick=reg_nick_id, 
			backpack_cells=json.dumps([
				[0, 7]
			])
		)

		await PlayerSettings.create(
			pers_id=ans.from_id, 
			pers_nick=reg_nick_id
		)

		end_reg_keyboard = keyboard_gen([
			[{'text':'Домой','color':'positive'}]
		], inline=True)

		await ans("🔸Поздравляю, вы успешно прошли регистрацию\n"
			"🔸Ваш персонаж - {ans.text[:-2]}ого рода\n"
			"🔸Вам открыта новая локация - Домой, нажмите на неё", 
			keyboard=end_reg_keyboard, attachment=f'PhotoDatePlayers/{ans.from_id}/{ans.from_id} profile.png')
		await bot.branch.exit(ans.peer_id)

	async def branch(self, ans: Message):
		replay_reg_keyboard = keyboard_gen([
			[{'text':'Мужской','color':'positive'}],
			[{'text':'Женский', 'color':'primary'}]
		], inline=True)
		await ans("🔸Добро пожаловать в блок регистрации\n🔸Выберите род вашего персонажа!", 
			keyboard=registration_keyboard)#TODO ATTACHMENT ABOUT REPLAY REGISTRATION

@bot.on.message(text=["домой", "!домой", "! домой", "/домой", "/ домой"], lower=True)
async def home(ans: Message):
	house_button = [
		[{'text':'Найти сервер','color':'positive'}],
		[{'text':'Топ игроков', 'color':'primary'}, {'text':'Магазин','color':'primary'}],
		[{'text':'Мои данные', 'color':'positive'}, {'text':'Помощь', 'color':'positive'}]
	]
	house_keyboard = keyboard_gen(house_button, inline=True)
	await ans("🔸Добро пожаловать в дом — это место для отдыха от мултьтиплеера\n\n"
		   "Здесь вы можете:\n"
		   "🔹Приобрести игровую валюту\n"
		   "🔹Узнать топ игроков\n"
		   "🔹Посмотреть свои данные\n"
		   "🔹Задать вопросы команде разработчиков", 
		   keyboard=house_keyboard, attachment="photo-191374726_457239029")

@bot.on.message(text=["топ игроков", "!топ игроков", "! топ игроков", 
					  "/топ игроков", "/ топ игроков"], lower=True)
async def top_player(ans: Message):
	'''Написать код для заполнения картинки'''
	list_player = [[pers.pers_nick, pers.pers_id, pers.now_common_balance] for pers in await StatePlayer.get()]
	await ans(list_player)
	list_player.sort(key=itemgetter(1), reverse=True)

	my_top = 0

	for _ in list_player:
		if _[1]==ans.from_id:
			list_player = list_player[0:9].append(_)
			break
		my_top+=1

	await WriteTopPlayer(list_player, str(my_top), ans.from_id)
	photo_top_player = await UpPhoto(ans, f'PhotoDatePlayers/{ans.from_id}/{ans.from_id} top_player.png')

	top_keyboard = keyboard_gen([
		[{'text':'Домой', 'color':'negative'}]
	], inline=True)
	await ans("🔸Вам показан топ игроков GlamBot-а\n🔸Здесь собраны самые величайшие бойцы", 
		   keyboard=top_keyboard, attachment=photo_top_player)

@bot.on.message(text=["найти сервер", "!найти сервер", "! найти сервер", 
					  "/найти сервер", "/ найти сервер"], lower=True)
async def find_server(ans: Message):
	sessions_button = []

	feature_sessions = [
	["Сессия — 1", 1],
	["Сессия — 2", 1],
	["Сессия — 3", 1],
	["Сессия — 4", 0],
	["Сессия — 5", 0]
	]

	urls_photos = [
		"photo-191374726_457239032",
		"photo-191374726_457239033",
		"photo-191374726_457239034",
		"photo-191374726_457239035",
		"photo-191374726_457239036",
		"photo-191374726_457239037",
		"photo-191374726_457239038"
	]

	load_sessions = ""

	for sess in feature_sessions:
		if await SessionDate.get_or_none(sess_name=sess[0]) is None:
			await SessionDate.create(
				sess_name=sess[0],
				battle_category=sess[1],
				list_player_id=json.dumps([])
			)

		status_player = await StatePlayer.get(pers_id=ans.from_id).status_player
		session_date = await SessionDate.get(sess_name=sess[0])
		light_bulb_load = ("💚" if session_date.now_seats_session<=40 else 
					 ("🧡" if session_date.now_seats_session<80 else "❤️"))
		load_sessions += f"{sess[0]}\n👥Игроков — [0/{session_player}]{light_bulb_load}\n"
		if session_date.now_seats_session < 80 or (status_player >= 2 
											   and session_date.now_seats_session < 100):
			sessions_button.append([
				[{'text':sess[0], 'color':'positive'}]
			])


	sessions_button.append([
		[{'text':'Домой', 'color':'negative'}]
	])
	session_keyboard = keyboard_gen(sessions_button, inline=True)
	await ans("🔸Это меню выбора сессии - благодаря им вы с другом можете играть вместе\n"
		   "Так же сессии нужны, чтобы снизить нагрузку в локациях\n"
		   "🔸Покупая статус — ..., вы сможете заходить на сессию с загрузкой до 120 человек\n\n"
		   f"🔹Сессии:\n{load_sessions}", 
		   keyboard=session_keyboard, attachment=urls_photos[random.randint(0,6)])

@bot.on.message(text=["сессия — 1", "сессия — 2", "сессия — 3", "сессия — 4", "сессия — 5"], lower=True)
async def connection_session(ans: Message):
	'''Заполнить форму входа в мультиплеер'''
	feature_session = [
	["Сессия — 1", 1],
	["Сессия — 2", 1],
	["Сессия — 3", 1],
	["Сессия — 4", 0],
	["Сессия — 5", 0]
	]
	for sess in feature_session:
		if await SessionDate.get_or_none(sess_name=sess[0]) is None:
			await SessionDate.create(
				sess_name=sess[0],
				battle_category=sess[1],
				list_player_id=json.dumps([0])
			)
		pers_state = await StatePlayer.get(pers_id=ans.from_id)
		session_date = await SessionDate.get(sess_name=sess[0])
		if sess[0] == ans.text and (session_date.now_seats_session<80 or 
							  (session_date.now_seats_session<100 and pers_state.status_player >= 2)):
			player_sess = json.loads(session_date.list_player_id)
			player_sess.append(ans.from_id)
			pers_state.status_player = int(sess[0][:-1])
			session_date.list_player_id = json.dumps(player_sess)
			session_date.now_seats_session += 1
			await session_date.save()
			await pers_state.save()
			await ans("🔸Вы зашли в мультиплеер")
			await bot.branch.add(ans.peer_id, "multiplayer_branch")
			break

		elif sess[0]==ans.text:
			house_keyboard=keyboard_gen([
				[{'text':'Домой', 'color':'negative'}]
			], inline=True)
			await ans("🔸Сессия загружена приходите позже", 
			 keyboard=house_keyboard)#TODO ATTACHMENT
			break

@bot.branch.cls_branch("market_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule("Выйти", lower=True))
	async def exit_branch(self, ans: Message):
		exit_market_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'positive'}]
		], inline=True)
		await ans("Окей, выходим!\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			keyboard=exit_market_keyboard)#TODO ATTACHMENT
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("<ammount_gold:int>", lower=True))
	async def buy_valuts_branch(self, ans: Message, ammount_gold):
		donate_time = round(time())
		count_ruble = (1 if ammount_gold<=10 else 
				 (ammount_gold/10 if ammount_gold<=900000 else 90000))

		link_payment = await qiwi_payment(donate_time, cost_ruble)

		player_state = await StatePlayer.get(pers_id=ans.from_id)
		player_state.comment_donate = donate_time
		await player_state.save()

		buy_valuts_button = [
			[{'text': 'НАЖИМАЙ СЮДА!', 'type': 'open_link', 'link': link_payment}], 
			[{'text':'Проверка оплаты', 'color':'positive'}],
			[{'text':'Отмена оплаты', 'color':'negative'}]
		]
		buy_valuts_keyboard = keyboard_gen(buy_valuts_button, inline=True)
		await ans("1️⃣Произведите оплату по ссылке\n"
			"🔸За вас может оплатить друг\n\n"
			"2️⃣Сделайте проверку или отмену\n"
			"🔸Если вы оплатили и нажмёте на отмену, то ваши средства пропадут❗\n"
			"🔸Нажимайте сразу после оплаты, иначе ваш запрос пропадет❗\n\n", 
			keyboard=buy_valuts_keyboard)#TODO ATTACHMENT

	@rule_disposal(VBMLRule("Проверка оплаты", lower=True))
	async def check_buy_valuts_branch(self, ans: Message):
		payment_state = await StatePlayer.get(pers_id=ans.from_id)
		if await qiwi_history(payment_state.comment_donate) is True:
			payment_state.now_donate_balance += payment_state.comment_donate*10
			payment_state.comment_donate = 0
			await payment_state.save()

			accept_val_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'positive'}]
			], inline=True)
			await ans("🔸Вы успешно приобрели валюту\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			 keyboard=accept_val_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.peer_id)

		else:
			check_buy_valuts_keyboard = keyboard_gen([
				[{'text':'Проверка оплаты', 'color':'positive'}],
				[{'text':'Отмена оплаты', 'color':'negative'}]
			], inline=True)
			await ans("Квитанция в обработке, повторите через 10 секунд!", 
			 keyboard=check_buy_valuts_keyboard)#TODO ATTACHMENT

	@rule_disposal(VBMLRule("Отмена оплаты", lower=True))
	async def cancel_buy_valuts_branch(self, ans: Message):
		payment_state = await StatePlayer.get(pers_id=ans.from_id)
		if await qiwi_history(payment_state.comment_donate) is True:
			payment_state.now_donate_balance += payment_state.comment_donate*10
			payment_state.comment_donate = 0
			await payment_state.save()

			accept_val_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'positive'}]
			], inline=True)
			await ans("🔸Оплата все таки прошла\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			 keyboard=accept_val_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.peer_id)

		else:
			payment_state.comment_donate = 0
			await payment_state.save()

			close_buy_valuts_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'negative'}]
			], inline=True)
			await ans("🔸Приходите снова", 
			 keyboard=close_buy_valuts_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.peer_id)

	async def branch(self, ans: Message):
		round_buy_valuts_button = [
			[{'text':'1000','color':'positive'}, {'text':'2500','color':'positive'}],
			[{'text':'5000','color':'positive'}, {'text':'10000','color':'positive'}],
			[{'text':'Выйти', 'color':'positive'}]
		]
		round_buy_valuts_keyboard = keyboard_gen(round_buy_valuts_button, inline=True)
		await ans("🔸Продавец - 'Я не понял, какое количество золота вы хотите приобрести?'\n"
			"🔸Напишите количество золота не больше 900к!\n"
			"Так же вы можете выбрать сумму, которую часто используют, нажатием на кнопку", 
			keyboard=round_buy_valuts_keyboard, attachment="photo-191374726_457239030")

@bot.on.message(text=["магазин", "!магазин", "! магазин", "/магазин", "/ магазин"], lower=True)
async def join_market(ans: Message):
	join_market_button = [
		[{'text':'1000','color':'positive'}, {'text':'2500','color':'positive'}],
		[{'text':'5000','color':'positive'}, {'text':'10000','color':'positive'}],
		[{'text':'Выйти', 'color':'negative'}]
	]
	join_market_keyboard = keyboard_gen(join_market_button, inline=True)
	await ans("🔸Вы пришли в магазин бота, здесь вы можете приобрести золотые монеты\n"
		   "🔸Выберите подходящий вариант или введите свою сумму\n\n"
		   "🔹Отношение валют 1:10 (рубль:голде)\n\n"
		   "100₽ — 1000🔶\n"
		   "250₽ — 2500🔶\n"
		   "500₽ — 5000🔶\n"
		   "1000₽ — 10000🔶\n\n"
		   "🔸Макс покупка голды — 900000🔶", 
		   keyboard=join_market_keyboard, attachment="photo-191374726_457239030")
	await bot.branch.add(ans.peer_id, "market_branch")

@bot.on.message(text="ответить <id_player:int>", lower=True)
async def my_date(ans: Message, id_player):
	if ans.text == 185031237:
		allowed_keyboard = keyboard_gen([
			[{'text':'Выйти', 'color':'negative'}]
		], inline=True)
		await ans("🔸Введите текст для ответа\n"
			"🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять ответ",
			keyboard=allowed_keyboard)#TODO ATTACHMENT
		await bot.branch.add(ans.peer_id, "root_branch", id_mail_player=id_player)

	else:
		access_denied_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'negative'}]
		], inline=True)
		await ans("❌Отказано в доступе", keyboard=access_denied_keyboard)

@bot.on.message(text="забанить реп <id_player:int>", lower=True)
async def my_date(ans: Message, id_player):
	if ans.text == 185031237:
		accept_ban_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'negative'}]
		], inline=True)
		pers_state = await StatePlayer.get(pers_id=ans.from_id)
		pers_state.ban_report = 1
		await pers_state.save()
		await ans("🔸Репорт игрока успешно забанен\n",
			keyboard=accept_ban_keyboard)#TODO ATTACHMENT

	else:
		access_denied_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'negative'}]
		], inline=True)
		await ans("❌Отказано в доступе", keyboard=access_denied_keyboard)

@bot.branch.cls_branch("root_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule("Выйти", lower=True))
	async def exit_branch(self, ans: Message):
		exit_root_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'positive'}]
		], inline=True)
		await ans("Окей, выходим!\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			keyboard=exit_root_keyboard)#TODO ATTACHMENT
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("<root_text>", lower=True))
	async def send_root_branch(self, ans: Message, id_mail_player, root_text):
		if len(root_text)>=2 and len(root_text)<=100:
			accept_root_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'negative'}]
			], inline=True)
			
			root_keyboard = keyboard_gen([
				[{'text': f'Отправить репорт', 'color':'positive'}]
			], inline=True)
			nick_player_report = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
			rand_report = random.randint(-2e9,2e9)
			await bot.api.messages.send(user_id=id_mail_player, 
							   random_id=rand_report, 
							   message=(f"Вам пришел ответ на репорт от админа @id{ans.from_id}({nick_player_report})\n\n\n"
										"Его ид:{ans.from_id}\n\n"
										"Он ответил:\n"
										"<<{root_text}>>"),
							   keyboard=root_keyboard)#TODO ATTACHMENT
			await ans(f'🎉Ваш ответ отправлен:\n\n\n <<{root_text}>> !', 
						keyboard=accept_root_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.from_id)

		else:
			error_send_keyboard = keyboard_gen([
				[{'text':'Выйти', 'color':'negative'}]
			], inline=True)
			await ans("❌Текст не прошел проверку\n"
			 "🏷️Длина - от 2 до 100 символов!\n\n"
			 "🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять ответ", 
			 keyboard=error_send_keyboard)#TODO ATTACHMENT

@bot.on.message(text=["мои данные", "!мои данные", "! мои данные", "/мои данные", "/ мои данные"], lower=True)
async def my_date(ans: Message):
	'''Написать заполнения профиля

	🔸Попробовать использовать разные модули
	🔸OpenGL + Pillow + Pillow-SMID/numpy

	'''
	
	my_date_keyboard = keyboard_gen([
		[{'text':'Домой', 'color':'negative'}]
	], inline=True)
	await ans("🔸Ваши данные представлены на картинке", keyboard=my_date_keyboard)#TODO ATTACHMENT

@bot.branch.cls_branch("report_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule("Выйти", lower=True))
	async def exit_branch(self, ans: Message):
		exit_report_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'positive'}]
		], inline=True)
		await ans("Окей, выходим!\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			keyboard=exit_report_keyboard)#TODO ATTACHMENT
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("<report_text>", lower=True))
	async def send_report_branch(self, ans: Message, report_text):
		if len(report_text)>=10 and len(report_text)<=50:

			accept_report_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'negative'}]
			], inline=True)
			
			root_keyboard = keyboard_gen([
				[{'text': f'Ответить {ans.from_id}', 'color':'positive'}],
				[{'text': f'Забанить реп {ans.from_id}', 'color':'negative'}]
			], inline=True)
			nick_player_report = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
			rand_report = random.randint(-2e9,2e9)
			await bot.api.messages.send(user_id=185031237, 
							   random_id=rand_report, 
							   message=(f"Вам пришел репорт от игрока @id{ans.from_id}({nick_player_report})\n\n\n"
										"Его ид:{ans.from_id}\n\n"
										"Он хочет спросить:\n"
										"<<{report_text}>>"),
							   keyboard=root_keyboard)#TODO ATTACHMENT
			await ans(f'🎉Ваш текст отправлен, ждите ответа:\n\n\n <<{report_text}>> !', 
						keyboard=accept_report_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.from_id)

		else:
			error_send_keyboard = keyboard_gen([
				[{'text':'Выйти', 'color':'negative'}]
			], inline=True)
			await ans("❌Текст не прошел проверку\n"
			 "🏷️Длина - от 10 до 50 символов!\n\n"
			 "🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять репорт", 
			 keyboard=error_send_keyboard)#TODO ATTACHMENT

@bot.on.message(text=["отправить репорт", "!отправить репорт", "! отправить репорт", 
					  "/отправить репорт", "/ отправить репорт"], lower=True)
async def send_report(ans: Message):
	send_report_keyboard = keyboard_gen([
		[{'text':'Выйти', 'color':'negative'}]
	], inline=True)
	await ans("🔸Вы зашли в блок отправки репорта,\n"
			"🔸Его необходимость в том, чтобы связаться с администрацией\n\n"
			"Шаблон отправки сообщения\n"
			"В чате мультиплеера проблема с отправкой сообщений\n\n"
			"🔸Текст репорта должен быть больше 10 символов и меньше 50!\n"
			"!!!Предупреждение, если сообщения будут не адекватными или содержать спам/флуд, то администрация в праве заблокировать вам репорт!!!", 
		   keyboard=send_report_keyboard)#TODO ATTACHMENT
	await bot.branch.add(ans.peer_id, "report_branch")

@bot.on.message(text=["админ рассылка", "!админ рассылка", "! админ рассылка", 
					  "/админ рассылка", "/ админ рассылка"], lower=True)
async def admin_mailing(ans: Message):
	if ans.from_id == 185031237:
		admin_mail_keyboard = keyboard_gen([
			[{'text':'Отменить', 'color':'negative'}]
		], inline=True)
		await ans("🔸Введите текст рассылки\n\n"
			"Шаблон\n"
			"Подписчики, у нас акция на статусы!\n\n"
			"🔹Больше 5 символов и меньше 500 символов",
			keyboard=ad_mail_keyboard)#TODO ATTACHMENT
		await bot.branch.add(ans.from_id, 'admin_mailing_branch')

	else:
		refusal_adm_mail_but = [
			[{'text':'Домой', 'color':'negative'}]
		]
		refusal_adm_mail_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'negative'}]
		], inline=True)
		await ans("❌Отказано в доступе", keyboard=refusal_adm_mail_keyboard)#TODO ATTACHMENT

@bot.branch.cls_branch('admin_mailing_branch')
class Branch(ClsBranch):
	@rule_disposal(VBMLRule("Отменить", lower=True))
	async def exit_branch(self, ans: Message):
		stop_adm_keyboard = keyboard_gen([
			[{'text':'Домой', 'color':'negative'}]
		], inline=True)
		await ans("🔸Отмена отправки рассылки\n"
			"🔸Выберите дальнейший путь", keyboard=stop_adm_keyboard)#TODO ATTACHMENT
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("<mailing_text>", lower=True))
	async def send_mailing_branch(self, ans: Message, mailing_text):
		if len(mailing_text)>=5 and len(mailing_text)<=500:
			allowed_mailing_player = await StatePlayer.get(indicator_mailing=1)

			accept_mailinig_keyboard = keyboard_gen([
				[{'text':'Домой', 'color':'negative'}]
			], inline=True)
			disconn_mailinig_keyboard = keyboard_gen([
				[{'text':'Рассылка откл', 'color':'negative'}]
			], inline=True)

			nick_admin_mailing = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
			await ans('🎉Рассылка началась')#TODO ATTACHMENT

			for person_date in allowed_mailing_player:
				rand_num_mailing = random.randint(-2e9,2e9)
				await bot.api.messages.send(user_id=person_date.pers_id,
								random_id=rand_num_mailing,
								message=(f"📢Вам пришла рассылка\n\n"
				 "🔸Вы можете ее отменить в разделе помощь\n\n<<{mailing_text}>>", ans.fwd_messages[0].text),
								keyboard=disconn_mailinig_keyboard)#TODO ATTACHMENT

			await ans("🎉Рассылка закончилась\n\n"
			f"📢Отправлено — {len(allowed_mailing_player)}👤", 
			keyboard=accept_mailinig_keyboard)#TODO ATTACHMENT
			await bot.branch.exit(ans.peer_id)

		else:
			error_adm_mailing_keyboard = keyboard_gen([
				[{'text':'Отменить', 'color':'negative'}]
			], inline=True)
			await ans("❌Текст не прошел проверку\n"
			 "🏷️Длина - от 5 до 500 символов!\n\n"
			 "🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять репорт", 
			 keyboard=error_adm_mailing_keyboard)#TODO ATTACHMENT

@bot.on.message(text=["рассылка", "!рассылка", "! рассылка", "/рассылка", 
					  "/ рассылка","рассылка откл"], lower=True)
async def panel_mailing(ans: Message):
	check_indicator_mailing = await StatePlayer.get(pers_id=ans.from_id).indicator_mailing
	panel_mailing_keyboard = keyboard_gen([
		[{'text':'Домой', 'color':'negative'}]
	], inline=True)
	message_answer = ("📢Рассылка успешно отменена\n\n" 
				 "🔸Если захотите быть снова в кругу событий и новостей, тогда нажмите еще раз на эту кнопку" 
				 if check_indicator_mailing==1 else 
				 "📢Свежие новости снова с вами, не скучали?\n" 
				 "🔹Если захотите отключить оповещения, тогда нажмите еще раз на кнопку")
	diff_indicator_mailing = (1 if check_indicator_mailing==0 else 0)
	await conn.execute(f"UPDATE player_database SET check_indicator_mailing={diff_indicator_mailing} WHERE person_id={ans.from_id}")#FIXED ME
	await ans(message_answer, keyboard=panel_mailing_button)#TODO ATTACHMENT

@bot.on.message(text=["quiet", "!quiet", "! quiet", "/quiet", "/ quiet"], lower=True)
async def help(ans: Message):
	await ans(await StatePlayer.get(pers_id=ans.from_id))
	await ans(await PlayerRocket.get(pers_id=ans.from_id))
	await ans(await PlayerInventory.get(pers_id=ans.from_id))
	await ans(await PlayerSettings.get(pers_id=ans.from_id))

@bot.on.message(text=["помощь", "!помощь", "! помощь", "/помощь", "/ помощь"], lower=True)
async def help(ans: Message):
	help_button = [
		[{'text':'Отправить репорт', 'color':'positive'}],
		[
			{'text':'Статья', 'type':'open_link',
				'link':'https://vk.com/@glambot-o-glambot-i-dalneishem-razvitii-new'},
			{'text':'Офёрта', 'type':'open_link',
				'link':'https://docs.google.com/document/d/1E2RNytuavppM3eXA76AIxAWBbKhSCCEnbUaTf85QgjI/edit?usp=drivesdk'}
		],
		[{'text':'Рассылка', 'color':'positive'}, {'text':'Админ рассылка', 'color':'positive'}],
		[{'text':'Домой', 'color':'negative'}]
	]
	help_keyboard = keyboard_gen(help_button, inline=True)
	await ans("🔸Вам нужна помощь?\n"
		   "🔸Посмотрите статью\n"
		   "🔸Если вы нашли баги,читеров и т.п - отправляйте репорт\n"
		   "🔸Вы можете отключить/включить рассылку\n"
		   "🔸Можете открыть офёрту и соглашение", 
		   keyboard=help_keyboard)#TODO ATTACHMENT

async def init_tortoise():
	await Tortoise.init(
		db_url="postgres://glamuser:GisMyVoron1974@127.0.0.1:5432/glamdata", 
		modules={"models": ["tortoise_models"]}
	)
	await Tortoise.generate_schemas()

bot.run_polling(on_startup=init_tortoise)