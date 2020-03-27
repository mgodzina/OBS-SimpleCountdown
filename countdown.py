#countdown V0.1
import obspython as obs
import time

time_input         = ""
source_name = ""

# ------------------------------------------------------------

def update_text():
	global time_input
	global source_name

	source = obs.obs_get_source_by_name(source_name)

	if time_input.count(':') > 1:
		final=time_input.split(':')
	else:
		print('Zły format. Użyj HH:MM:SS')
		final='00:00:00'.split(':')

	if final[0].isdigit() and final[1].isdigit() and final[2].isdigit():
		godzina = int(final[0]) -1
		minuty = int(final[1])
		sekundy = int(final[2])
	else:
		print('Zły format. Użyj HH:MM:SS')
		godzina = 0
		minuty = 0
		sekundy = 0

	czas1 = list(time.localtime())
	czas1[3] = godzina
	czas1[4] = minuty
	czas1[5] = sekundy
	czas1 = time.struct_time(tuple(czas1))
	timestamp =  time.mktime(czas1) - time.mktime(time.gmtime())
	h = int(((timestamp / 60) / 60) % 60 )
	s= int(timestamp % 60)
	m= int((timestamp / 60) % 60)

	if timestamp > 0:
		text = '{}:{:02}:{:02}'.format(h, m, s)
	else:
		text = 'START!'

	settings = obs.obs_data_create()
	obs.obs_data_set_string(settings, "text", text)
	obs.obs_source_update(source, settings)
	obs.obs_data_release(settings)
			
				
			
	obs.obs_source_release(source)

def refresh_pressed(props, prop):
	update_text()

# ------------------------------------------------------------

def script_description():
	return "Simple Countdown to HH:MM::SS. Does not support day skip.\n\nBy Marcin Godzina\nhttps://github.com/mgodzina"

def script_update(settings):
	global time_input
	global source_name

	time_input         = obs.obs_data_get_string(settings, "time_input")
	source_name = obs.obs_data_get_string(settings, "source")

	obs.timer_remove(update_text)

	if time_input != "" and source_name != "":
		obs.timer_add(update_text, 1000)

def script_defaults(settings):
	obs.obs_data_set_default_string(settings, "time_input", "12:00:00")

def script_properties():
	props = obs.obs_properties_create()

	obs.obs_properties_add_text(props, "time_input", "Time", obs.OBS_TEXT_DEFAULT)

	p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)

	obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
	return props
