from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageEnhance

pattern_pers_date = Image.open('materials_bot/PersDate.png')

def ElipsAva(id, linc):
	photo_ava_400 = Image.open(f'PhotoDatePlayers/{id}/{linc} orig_400.png')

	elips_size = (264, 264)  # размер итогового портрета
	elips_mask = Image.new('L', elips_size, 0)
	elips_draw = ImageDraw.Draw(elips_mask)
	elips_draw.ellipse((0, 0) + elips_size, fill=255)

	photo_ava_320 = photo_ava_400.resize(elips_size)

	elips_output = ImageOps.fit(photo_ava_320, elips_mask.size, centering=(0.5, 0.5))
	elips_output.putalpha(elips_mask)
	elips_output.thumbnail(elips_size, Image.ANTIALIAS)
	elips_output.save(f'PhotoDatePlayers/{id}/{id} elips_320.png')


def WritePersProfile(pers_date):
	elips_mask = Image.new('L', (264, 264), 0)
	elips_ava_320 = Image.open(f'PhotoDatePlayers/{pers_date[1]}/{pers_date[1]} elips_320.png')
	pattern_pers_date.paste(elips_ava_320.convert('RGB'), (44, 4), elips_ava_320)

	standart_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=60, index=0, encoding='', layout_engine=None)
	small_font = ImageFont.truetype(font="shrifts/Ubuntu-Medium.ttf", size=35, index=0, encoding='', layout_engine=None)
	text_color = (32, 0, 38)

	cordinat_list = [
		[520, 42, standart_font],
		[550, 152, small_font],
		[550, 233, small_font],
		[550, 310, small_font],
		[250, 470, standart_font],
		[630, 470, standart_font],
		[250, 656, standart_font],
		[630, 656, standart_font],
		[250, 840, standart_font],
		[630, 840, standart_font]
	]

	draw = ImageDraw.Draw(pattern_pers_date)

	for pencil in cordinat_list:
		draw.text((pencil[0], pencil[1]), pers_date[cordinat_list.index(pencil)], text_color, pencil[2])

	pattern_pers_date.save(f'PhotoDatePlayers/{pers_date[1]}/{pers_date[1]} profile.png')
