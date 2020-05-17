from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance

def ElipsAva(id, linc):
	photo_ava_400 = Image.open(f'PhotoDatePlayers/{id}/{linc} orig_400.png')

	elips_sizes = [
		(264, 264), 
		(144, 144), 
		(112,112)
	]

	for size in elips_sizes:
		elips_mask = Image.new('L', size, 0)
		elips_draw = ImageDraw.Draw(elips_mask)
		elips_draw.ellipse((0, 0) + size, fill=255)

		photo_x_size = photo_ava_400.resize(size)

		elips_output = ImageOps.fit(photo_x_size, elips_mask.size, centering=(0.5, 0.5))
		elips_output.putalpha(elips_mask)
		elips_output.thumbnail(size, Image.ANTIALIAS)
		elips_output.save(f'PhotoDatePlayers/{id}/{id} elips_{size[0]}.png')


def WritePersProfile(pers_date):
	elips_mask = Image.new('L', (264, 264), 0)
	pattern_pers_date = Image.open('materials_bot/PersDate.png')
	elips_ava_264 = Image.open(f'PhotoDatePlayers/{pers_date[1]}/{pers_date[1]} elips_264.png')
	pattern_pers_date.paste(elips_ava_264.convert('RGB'), (44, 4), elips_ava_264)

	standart_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=60, index=0, encoding='', layout_engine=None)
	small_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=35, index=0, encoding='', layout_engine=None)
	text_color = (32, 0, 38)

	cordinat_list = [
		[(520, 42), standart_font],
		[(550, 152), small_font],
		[(550, 233), small_font],
		[(550, 310), small_font],
		[(250, 470), standart_font],
		[(630, 470), standart_font],
		[(250, 656), standart_font],
		[(630, 656), standart_font],
		[(250, 840), standart_font],
		[(630, 840), standart_font]
	]

	draw = ImageDraw.Draw(pattern_pers_date)

	for pencil in cordinat_list:
		draw.text(pencil[0], str(pers_date[cordinat_list.index(pencil)]), text_color, pencil[1])

	pattern_pers_date.save(f'PhotoDatePlayers/{pers_date[1]}/{pers_date[1]} profile.png')

def WriteTopPlayer(players_data, person_top, person_id):
	pattern_top_player = Image.open('materials_bot/TopPlayer.png')
	standart_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=60, index=0, encoding='', layout_engine=None)
	small_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=30, index=0, encoding='', layout_engine=None)

	text_color = (32, 0, 38)
	cordinat_writing = [
		[(144, 144), (7, 99), (180, 140), (310, 105), (200, 205), (200, 105)],
		[(144, 144), (848, 99), (540, 140), (668, 105), (560, 205), (560, 105)],
		[(112, 112), (284, 260), (424, 284), (548, 250), (437, 348), (440, 252)],
		[(112, 112), (25, 425), (150, 455), (280, 420), (160, 505), (160, 420)],
		[(112, 112), (900, 425), (555, 455), (700, 420), (580, 505), (580, 420)],
		[(112, 112), (25, 570), (150, 590), (280, 555), (160, 640), (160, 560)],
		[(112, 112), (900, 565), (555, 590), (700, 560), (580, 640), (580, 560)],
		[(112, 112), (25, 710), (150, 730), (280, 700), (160, 785), (160, 700)],
		[(112,112), (900, 705), (555, 730), (700, 700), (585, 785), (585, 700)],
		[(144, 144), (115, 855), (255, 885), (540, 860), (380, 955), (280, 855)]
	]

	draw = ImageDraw.Draw(pattern_top_player)

	for data in players_data:
		num_player = players_data.index(data)
		elips_mask = Image.new('L', cordinat_writing[num_player][0], 0)
		elips_x_size = Image.open(f'PhotoDatePlayers/{data[1]}/{data[1]} elips_{cordinat_writing[num_player][0][0]}.png')
		pattern_top_player.paste(elips_x_size.convert('RGB'), 
						  cordinat_writing[num_player][1], 
						  elips_x_size)

		for pen in cordinat_writing[num_player][2:]:
			num_cordinat = cordinat_writing[num_player]
			num_cordinat = num_cordinat.index(pen)-2

			type_shrift = (small_font if num_cordinat>0 else standart_font)

			what_writed = (person_top if num_player==9 else 
				  (num_player+1 if num_cordinat==3 else data[num_cordinat]))
			draw.text(pen, str(what_writed), text_color, type_shrift)
	pattern_top_player.save(f'PhotoDatePlayers/{person_id}/{person_id} top_player.png')