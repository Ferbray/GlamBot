from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance

def ElipsAva(id, linc):
	photo_ava_400 = Image.open(f'PhotoDatePlayers/{id}/{linc} orig_400.png')

	list_elips_sizes = [
		(264, 264), 
		(144, 144), 
		(112,112)
	]

	for elips_size in list_elips_sizes:
		elips_mask = Image.new('L', elips_size, 0)
		elips_draw = ImageDraw.Draw(elips_mask)
		elips_draw.ellipse((0, 0) + elips_size, fill=255)

		photo_x_size = photo_ava_400.resize(elips_size)

		elips_output = ImageOps.fit(photo_x_size, elips_mask.size, centering=(0.5, 0.5))
		elips_output.putalpha(elips_mask)
		elips_output.thumbnail(elips_size, Image.ANTIALIAS)
		elips_output.save(f'PhotoDatePlayers/{id}/{id} elips_{elips_size[0]}.png')


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
		draw.text(pencil[0], pers_date[cordinat_list.index(pencil)], text_color, pencil[1])

	pattern_pers_date.save(f'PhotoDatePlayers/{pers_date[1]}/{pers_date[1]} profile.png')

def WriteTopPlayer(list_player, person_top, person_id):
	pattern_top_player = Image.open('materials_bot/TopPlayer.png')
	standart_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=60, index=0, encoding='', layout_engine=None)
	small_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=35, index=0, encoding='', layout_engine=None)

	text_color = (32, 0, 38)
	cordinat_writing = [
		[(144, 144), (78, 169), ..., ..., ...],
		[(144, 144), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112, 112), ..., ..., ..., ...],
		[(112,112), ..., ..., ..., ...],
		[(144, 144), ..., ..., ..., ...]
	]

	draw = ImageDraw.Draw(pattern_top_player)

	for player_date in list_player:
		num_player = list_player.index(player_date)
		elips_mask = Image.new('L', cordinat_writing[num_player][0], 0)
		elips_x_size = Image.open(f'PhotoDatePlayers/{player_date[1]}/{player_date[1]} elips_{cordinat_writing[num_player][0]}.png')
		pattern_pers_date.paste(elips_x_size.convert('RGB'), 
						  cordinat_writing[num_player][1], 
						  elips_x_size)

		for pen in cordinat_writing[num_player][2:]:
			num_cordinat = cordinat_writing[num_player].index(pen)-2
			type_shrift = (small_font if num_cordinat>0 else standart_font)
			what_writed = (person_top if num_player==9 else 
				  (player_date[num_cordinat] if num_cordinat<5 else str(num_player+1)))
			draw.text(pen, what_writed, text_color, type_shrift)

	pattern_pers_date.save(f'PhotoDatePlayers/{person_id}/{person_id} top_player.png')