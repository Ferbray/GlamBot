import json
import os
import shutil
import random
import re
import ssl
from time import ctime,time
from decimal import Decimal
from operator import itemgetter

from vkbottle import Bot, Message, keyboard_gen,VKError
from vkbottle.branch import ClsBranch, ExitBranch, rule_disposal, Branch
from vkbottle.rule import AbstractMessageRule
from vkbottle.keyboard import Keyboard, Text
from vbml import PatchedValidators
from aiohttp import ClientSession
import requests
import asyncio
import asyncpg

from database_wrapper import Database
from qiwi_wrapper import *

bot = Bot('9c6713c47ccc55cbbb5ba7b712c1a8a5e7c3c419da361d12f60dfd27ad3c882ed28c344b898193733989b', mobile=False)

conn = Database(user='glamuser', 
				password='GisMyVoron1974', 
				database='glamdata', 
				host='127.0.0.1')

async def get_info(upload_url: str, files: dict):
	async with ClientSession(json_serialize=json.dumps) as client:
		async with client.post(upload_url, ssl=ssl.SSLContext(), data=files) as r:
			response = await r.read()
	return json.loads(response)

async def UpPhoto(ans, img_name):
	upload_info = await bot.api.photos.get_messages_upload_server(peer_id=ans.from_id)
	upload_task = bot.loop.create_task(get_info(
		upload_info.upload_url, files={'photo': open(img_name, "rb")}
		))
	upload_result = await upload_task
	serv_xy_map = await bot.api.photos.save_messages_photo(photo=upload_result["photo"], 
														server=upload_result["server"], 
														hash=upload_result["hash"])

	xymap = "photo{}_{}".format(serv_xy_map[0].owner_id, serv_xy_map[0].id)
	return xymap

@bot.on.pre_process()
async def registration(ans: Message):
	if len(await conn.fetch(f"SELECT person_id FROM date_person WHERE person_id={ans.from_id}"))==0:
		await bot.branch.add(ans.from_id, 'registration_branch')

@bot.branch.cls_branch("registration_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule(["Мужской","Женский"], lower=True))
	async def join_registration_branch(self, ans: Message):
		'''Планирование

		🔸Убрать requests
		🔸Написать парсинг через aiohttp
		🔸Переписать заполнение бд под Tortoise

		'''
		os.mkdir(f"PhotoDatePlayers/{ans.from_id}")
		try:
			vk = await bot.api.users.get(user_ids=ans.from_id, fields="photo_400_orig")
			r = requests.get(vk[0].photo_400_orig,stream=True)
			regfile = vk[0].photo_400_orig.split("/")[-1]
			regfile = regfile.split('.')[0]
			with open(f"PhotoDatePlayers/{ans.from_id}/{regfile}.png","bw") as file:
				for chunk in r.iter_content(4096):
					file.write(chunk)
		except:
			shutil.copy('materials_bot/NoPhoto.png', f"PhotoDatePlayers/{ans.from_id}")
			regfile = "NoPhoto"
			await ans("У вас нет аватарки, вам временно поставлена эта!", attachment=...)

		ElipsAva(ans.from_id,regfile)
		reg_nick_id = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
		date_reg = round(time())
		gender_player = (1 if ans.text=='Женский' else 0)

		# state_list=[ans.from_id,reg_nick_id,"1",race,"0","10",strength,hp,mind,agility,"","","",""]
		# WriteProfil(state_list)
		# inventory_list=[ans.from_id,"0","0","Без оружный","Отсутствует","Отсутствует","Отсутствует","Отсутствует","Отсутсвует","Отсутвует","Отсутствует","Отсутствует"]
		# WriteInventory(inventory_list)
		# skills_list=[ans.from_id,"1","[0/30]","1","[0/10]","1","[0/10]","1","[0/10]","1","[0/10]"]
		# WriteSkills(skills_list)

		await conn.execute("INSERT INTO player_database VALUES ("
		f"{ans.from_id}, '{reg_nick_id}', {gender_player}, {date_reg}, 0, 0, 0,"
		"0, 0, 0, 76, 32, 19, 89, ..., 61, 6, , 0, 57, 100, 72, 100, 30, 100,"
		"0, 100, 1, 500, 0, 0, 3, 0, 10, 6, 1, 1, 0)")

		await conn.execute("INSERT INTO player_inventory VALUES ("
		f"{ans.from_id}, '{reg_nick_id}',0,array[[1,5]],0,1,1,0,1)")

		await conn.execute("INSERT INTO settings VALUES ("
		f"{ans.from_id}, '{reg_nick_id}',0,0,0)")

		after_registration_button = [
			[{'text':'Домой','color':'positive'}]
		]
		after_registration_keyboard = keyboard_gen(after_registration_button, inline=True)

		await ans("🔸Поздравляю, вы успешно прошли регистрацию\n"
			"🔸Ваш персонаж - {ans.text[:-2]}ого рода\n"
			"🔸Вам открыта новая локация - Домой, нажмите на неё", 
			keyboard=after_registration_keyboard, attachment=...)

	async def round_registration_branch(self, ans: Message, *args):
		registration_button = [
			[{'text':'Мужской','color':'positive'}],
			[{'text':'Женский', 'color':'primary'}]
		]
		registration_keyboard = keyboard_gen(registration_button, inline=True)
		await ans("🔸Добро пожаловать в блок регистрации\n🔸Выберите род вашего персонажа!", 
			keyboard=registration_keyboard, attachment=...)


@bot.on.message(text=["домой", "!домой", "! домой", "/домой", "/ домой"], lower=True)
async def start_place(ans: Message):
	house_button = [
		[{'text':'Найти сервер','color':'positive'}],
		[{'text':'Топ игроков', 'color':'primary'}, {'text':'Магазин','color':'primary'}],
		[{'text':'Мои данные', 'color':'positive'}, {'text':'Помощь', 'color':'positive'}]
	]
	house_keyboard = keyboard_gen(house_button, inline=True)
	await ans("🔸Добро пожаловать на старт площадку — это место для отдыха от мултьтиплеера\n\n"
		   "Здесь вы можете:\n"
		   "🔹Приобрести игровую валюту\n"
		   "🔹Узнать топ игроков\n"
		   "🔹Посмотреть свои данные\n"
		   "🔹Задать вопросы команде разработчиков", 
		   keyboard=house_keyboard, attachment=...)

@bot.on.message(text=["топ игроков", "!топ игроков", "! топ игроков", 
					  "/топ игроков", "/ топ игроков"], lower=True)
async def top_player(ans: Message):
	'''Заполнить кодом топ игроков по валюте - рублям'''
	top_button = [
		[{'text':'Домой', 'color':'negative'}]
	]
	top_keyboard = keyboard_gen(top_button, inline=True)
	await ans("🔸Вам показан топ игроков GlamBot-а\n🔸Здесь собраны самые величайшие бойцы", 
		   keyboard=top_keyboard, attachment=...)

@bot.on.message(text=["найти сервер", "!найти сервер", "! найти сервер", 
					  "/найти сервер", "/ найти сервер"], lower=True)
async def find_server(ans: Message):
	sessions_button = []

	sessions_list = [
	["Сессия — 1","first_session"],
	["Сессия — 2","second_session"],
	["Сессия — 3","third_session"],
	["Сессия — 4","fourth_session"],
	["Сессия — 5","fiveth_session"]
	]

	load_sessions = ""

	for sess in sessions_list:
		session_player = await conn.fetch("SELECT %s,status_player FROM * WHERE id=%s" % (sess[1],ans.from_id))
		light_bulb_load = ("💚" if session_player<=70 else "🧡")
		light_bulb_load = ("❤️" if session_player>=100 else light_bulb_load)
		load_sessions += f"{sess[0]}\n👥Игроков — [0/{session_player}]{light_bulb_load}\n"
		if session_player[0][f"{sess[1]}"] < 100 or (session_player[0]["status_player"] >= ... 
											   and session_player[0][f"{sess[1]}"] < 110):
			sessions_button.append([
				[{'text':sess[0], 'color':'negative'}]
			])


	sessions_button.append([
		[{'text':'Домой', 'color':'negative'}]
	])
	session_keyboard = keyboard_gen(sessions_button, inline=True)
	await ans("🔸Это меню выбора сессии - благодаря им вы с другом можете играть вместе\n"
		   "Так же сессии нужны, чтобы снизить нагрузку в локациях\n"
		   "🔸Покупая статус — ..., вы сможете заходить на сессию с загрузкой до 120 человек\n\n"
		   f"🔹Сессии:\n{load_sessions}", 
		   keyboard=session_keyboard, attachment=...)

@bot.on.message(text=["сессия — 1", "сессия — 2", "сессия — 3", "сессия — 4", "сессия — 5"], lower=True)
async def connection_session(ans: Message):
	'''Заполнить форму входа в мультиплеер'''
	sessions_list = [
	["Сессия — 1","first_session"],
	["Сессия — 2","second_session"],
	["Сессия — 3","third_session"],
	["Сессия — 4","fourth_session"],
	["Сессия — 5","fiveth_session"]
	]
	for sess in sessions_list:
		session_player = await conn.fetch("SELECT %s,status_player FROM * WHERE id=%s" % (sess[1],ans.from_id))
		if sess[0] == ans.text and (session_player<100 or 
							  (session_player<120 and session_player[0]["status_player"] >= ...)):
			await ans("🔸Вы зашли в мультиплеер")
			await bot.branch.add(ans.peer_id, "multiplayer_branch")
			break
		elif sess[0]==ans.text:
			house_button = [
				[{'text':'Домой', 'color':'positive'}]
			]
			house_keyboard=keyboard_gen(house_button, inline=True)
			await ans("🔸Сессия загружена приходите позже", keyboard=house_keyboard, attachment=...)
			break

@bot.branch.cls_branch("market_branch")
class Branch(ClsBranch):
	'''Дописать код доната

	🔸Проверка по оплате
	🔸Отмена оплаты
	🔸Сама оплата на aiohttp + aioqiwi
	'''
	@rule_disposal(VBMLRule("Выйти", lower=True))
	async def exit_market_branch(self, ans: Message):
		exit_market_button = [
			[{'text':'Домой', 'color':'positive'}]
		]
		exit_market_keyboard = keyboard_gen(exit_market_button, inline=True)
		await ans("Окей, выходим!\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			keyboard=exit_market_keyboard, attachment=...)
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("<ammount_gold:int>", lower=True))
	async def buy_valuts_branch(self, ans: Message, ammount_gold):
		pass

	@rule_disposal(VBMLRule("Проверка оплаты", lower=True))
	async def check_buy_valuts_branch(self, ans: Message):
		check_buy_valuts_button = [
			[{'text':'Проверка оплаты', 'color':'positive'}],
			[{'text':'Отмена оплаты', 'color':'negative'}]
		]
		check_buy_valuts_keyboard = keyboard_gen(check_buy_valuts_button, inline=True)
		await ans("Квитанция в обработке, повторите через 10 секунд!", keyboard=check_buy_valuts_keyboard)

	@rule_disposal(VBMLRule("Отмена оплаты", lower=True))
	async def cancel_buy_valuts_branch(self, ans: Message):
		if ...:
			pass
		else:
			pass

	async def round_buy_valuts_branch(self, ans: Message, *args):
		round_buy_valuts_button = [
			[{'text':'1000','color':'positive'}, {'text':'2500','color':'positive'}],
			[{'text':'5000','color':'positive'}, {'text':'10000','color':'positive'}],
			[{'text':'Выйти', 'color':'positive'}]
		]
		round_buy_valuts_keyboard = keyboard_gen(round_buy_valuts_button, inline=True)
		await ans("🔸Продавец - 'Я не понял, какое количество золота вы хотите приобрести?'\n"
			"🔸Напишите количество золота не больше 900к!\n"
			"Так же вы можете выбрать сумму, которую часто используют, нажатием на кнопку", 
			keyboard=round_buy_valuts_keyboard, attachment=...)

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
		   keyboard=join_market_keyboard, attachment=...)
	await bot.branch.add(ans.peer_id, "market_branch")

@bot.on.message(text=["мои данные", "!мои данные", "! мои данные", "/мои данные", "/ мои данные"], lower=True)
async def my_date(ans: Message):
	'''Написать заполнения профиля

	🔸Попробовать использовать разные модули
	🔸OpenGL + Pillow + Pillow-SMID

	'''
	
	my_date_button = [
		[{'text':'Домой', 'color':'negative'}]
	]
	my_date_keyboard = keyboard_gen(my_date_button, inline=True)
	await ans("🔸Ваши данные представлены на картинке", keyboard=my_date_keyboard, attachment=...)

@bot.branch.cls_branch("report_branch")
class Branch(ClsBranch):
	@rule_disposal(VBMLRule("Выйти", lower=True))
	async def exit_report_branch(self, ans: Message):
		exit_report_button = [
			[{'text':'Домой', 'color':'positive'}]
		]
		exit_report_keyboard = keyboard_gen(exit_report_button, inline=True)
		await ans("Окей, выходим!\nНажмите на кнопку <<Домой>>, чтобы вернуться", 
			keyboard=exit_report_keyboard, attachment=...)
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("реп <report_text>", lower=True))
	async def exit_report_branch(self, ans: Message, report_text):
		if len(report_text)>=10 and len(report_text)<=50:
			accept_report_button = [
				[{'text':'Домой', 'color':'negative'}]
			]
			accept_report_keyboard = keyboard_gen(accept_report_button, inline=True)
			root_button = [
				[{'text':'Ответить', 'color':'positive'}]
			]
			
			root_keyboard = keyboard_gen(root_button, inline=True)
			nick_player_report = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
			rand_report = random.randint(-2e9,2e9)
			await bot.api.messages.send(user_id=185031237, 
							   random_id=rand_report, 
							   message=(f"Вам пришел репорт от игрока @id{ans.from_id}({nick_player_report})\n\n\n"
										"Его ид:{ans.from_id}\n\n"
										"Он хочет спросить:\n"
										"<<{ans.text}>>"),
							   keyboard=root_keyboard,
							   attachment=...)
			await ans(f'🎉Ваш текст отправлен, ждите ответа:\n\n\n <<{ans.text}>> !', 
						keyboard=stop_report_keyboard, attachment=...)
			await bot.branch.exit(ans.from_id)

		else:
			error_send_button = [
				[{'text':'Выйти', 'color':'negative'}]
			]
			error_send_keyboard = keyboard_gen(error_send_button, inline=True)
			await ans("❌Текст не прошел проверку\n"
			 "🏷️Длина - от 10 до 50 символов!\n\n"
			 "🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять репорт", 
			 keyboard=error_send_keyboard, attachment=...)

	async def send_report_branch(self, ans: Message):
		round_send_report_button = [
		[{'text':'Выйти', 'color':'negative'}]
	]
		round_send_report_keyboard = keyboard_gen(round_send_report_button, inline=True)
		await ans("❌Вы не указали в начале 'реп'\n\n"
			"Шаблон\n"
			"реп Админы, у вас не работает чат в мультиплеере, зайдите посмотрите\n\n"
			"Длина сообщения должна быть больше 10 символов и меньше 50",
			keyboard=round_send_report_keyboard, attachment=...)

@bot.on.message(text=["отправить репорт", "!отправить репорт", "! отправить репорт", 
					  "/отправить репорт", "/ отправить репорт"], lower=True)
async def send_report(ans: Message):
	send_report_button = [
		[{'text':'Выйти', 'color':'negative'}]
	]
	send_report_keyboard = keyboard_gen(send_report_button, inline=True)
	await ans("🔸Вы зашли в блок отправки репорта,\n"
			"🔸Его необходимость в том, чтобы связаться с администрацией\n\n"
			"Шаблон отправки сообщения\n"
			"реп В чате мультиплеера проблема с отправкой сообщений\n\n"
			"🔸Текст репорта должен быть больше 10 символов и меньше 50!\n"
			"🔸Не забывайте командное слово 'реп' в начале\n"
			"!!!Предупреждение, если сообщения будут не адекватными или содержать спам/флуд, то администрация в праве заблокировать вам репорт!!!", 
		   keyboard=send_report_keyboard, attachment=...)
	await bot.branch.add(ans.peer_id, "report_branch")

@bot.on.message(text=["админ рассылка", "!админ рассылка", "! админ рассылка", 
					  "/админ рассылка", "/ админ рассылка"], lower=True)
async def admin_mailing(ans: Message):
	if ans.from_id == 185031237:
		admin_mail_button = [
			[{'text':'Отменить', 'color':'negative'}]
		]
		admin_mail_keyboard = keyboard_gen(admin_mail_button, inline=True)
		await ans("🔸Введите текст рассылки\n\n"
			"Шаблон\n"
			"адм Подписчики, у нас акция на статусы!\n\n"
			"🔹Больше 5 символов и меньше 500 символов",
			keyboard=ad_mail_keyboard, attachment=...)
		await bot.branch.add(ans.from_id, 'admin_mailing_branch')
	else:
		refusal_adm_mail_but = [
			[{'text':'Домой', 'color':'negative'}]
		]
		refusal_adm_mail_keyboard = keyboard_gen(refusal_adm_mail_but, inline=True)
		await ans("❌Отказано в доступе", keyboard=refusal_adm_mail_keyboard, attachment=...)


@bot.branch.cls_branch('admin_mailing_branch')
class Branch(ClsBranch):
	'''Необходимо добавить, чтобы Админ мог отправить при рассылке

	🔸Клавиатуру
	🔸Фотографию
	🔸Пересланное письмо

	'''
	@rule_disposal(VBMLRule("Отменить", lower=True))
	async def exit_ad_mailing_branch(self, ans: Message):
		stop_adm_button = [
			[{'text':'Домой', 'color':'negative'}]
		]
		stop_adm_keyboard = keyboard_gen(stop_adm_button, inline=True)
		await ans("🔸Отмена отправки рассылки\n"
			"🔸Выберите дальнейший путь", keyboard=stop_adm_keyboard, attachment=...)
		await bot.branch.exit(ans.peer_id)

	@rule_disposal(VBMLRule("адм <mailing_text>", lower=True))
	async def exit_ad_mailing_branch(self, ans: Message, mailing_text):
		if len(mailing_text)>=5 and len(mailing_text)<=500:
			allowed_mailing_player = await conn.fetch("SELECT person_id FROM date_person WHERE indicator_mailing=1")
			accept_mailinig_button = [
				[{'text':'Домой', 'color':'negative'}]
			]
			accept_mailinig_keyboard = keyboard_gen(accept_mailinig_button, inline=True)
			disconn_mailinig_button = [
				[{'text':'Помощь', 'color':'negative'}]
			]
			disconn_mailinig_keyboard = keyboard_gen(disconn_mailinig_button, inline=True)
			nick_admin_mailing = (await bot.api.users.get(user_ids=ans.from_id))[0].first_name
			await ans('🎉Рассылка началась', attachment=...)
			for person_id in allowed_mailing_player:
				rand_num_mailing = random.randint(-2e9,2e9)
				await bot.api.messages.send(user_id=person_id["person_id"],
								random_id=rand_num_mailing,
								message=(f"📢Вам пришла рассылка\n\n"
				 "🔸Вы можете ее отменить в разделе помощь\n\n<<{ans.text}>>"),
								keyboard=disconn_mailinig_keyboard,
								attachment=...)

			await ans("🎉Рассылка закончилась\n\n"
			f"📢Отправлено — {len(all_person_id)}👤", 
			keyboard=accept_mailinig_keyboard, attachment=...)
			await bot.branch.exit(ans.peer_id)

		else:
			error_adm_mailing_button = [
				[{'text':'Отменить', 'color':'negative'}]
			]
			error_adm_mailing_keyboard = keyboard_gen(error_adm_mailing_button, inline=True)
			await ans("❌Текст не прошел проверку\n"
			 "🏷️Длина - от 5 до 500 символов!\n\n"
			 "🔸Вы можете нажать на кнопку - отмены, если не хотите отправлять репорт", 
			 keyboard=error_adm_mailing_keyboard, attachment=...)

	async def round_ad_mailing_branch(self, ans: Message):
		round_ad_mailing_button = [
			[{'text':'Выйти', 'color':'negative'}]
		]
		round_ad_mailing_keyboard = keyboard_gen(round_ad_mailing_button, inline=True)
		await ans("❌Вы не указали в начале 'адм'\n\n"
			"Шаблон\n"
			"адм Подписчики, у нас акция на статусы!\n\n"
			"Длина сообщения должна быть больше 5 символов и меньше 500",
			keyboard=round_ad_mailing_keyboard, attachment=...)

@bot.on.message(text=["рассылка", "!рассылка", "! рассылка", "/рассылка", "/ рассылка"], lower=True)
async def panel_mailing(ans: Message):
	check_indicator_mailing = (await conn.fetch(f"SELECT indicator_mailing FROM player_database WHERE person_id={ans.from_id}"))[0]["indicator_mailing"]
	panel_mailing_button = [
		[{'text':'Домой', 'color':'negative'}]
	]
	panel_mailing_keyboard = keyboard_gen(panel_mailing_button,inline=True)
	message_answer = ("📢Рассылка успешно отменена\n\n" 
				 "🔸Если захотите быть снова в кругу событий и новостей, тогда нажмите еще раз на эту кнопку" 
				 if check_indicator_mailing==1 else 
				 "📢Свежие новости снова с вами, не скучали?\n" 
				 "🔹Если захотите отключить оповещения, тогда нажмите еще раз на кнопку")
	diff_indicator_mailing = (1 if check_indicator_mailing==0 else 0)
	await conn.execute(f"UPDATE player_database SET check_indicator_mailing={diff_indicator_mailing} WHERE person_id={ans.from_id}")
	await ans(message_answer, keyboard=panel_mailing_button, attachment=...)

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
		   keyboard=help_keyboard, attachment=...)
