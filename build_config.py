#################################
# Reference Prompts
#################################
pro0 = '''
beautiful detailed CG unity 8k wallpaper of loli :3 girl wearing kitchen maid uniform and pleated skirt, blue long hairstyle, perfect symmetrical face, jewely eyes with with elegant eyelashes, glowing skin, cleavage breasts, by ilya kuvshinov and alphonse mucha, luminus particles, golden hour lighting, strong rim light, intense shadows, by Canon EOS SIGMA Art Lens
'''
pro1 = '''
fantastic 8k book cover art of cute girl, silk dress, baroque lace frills, white skin, blonde wavy long hairstyle, perfect symmetrical face, cleavage breasts, by krenz cushart and stanley lau and artem demura and alphonse mucha and peter mohrbacher, beautiful snow palace with glitter many particles, soft focus, artgerm, strong rim light, golden hour, by Canon EOS, SIGMA Art Lens 35mm F1.4, ISO 200 Shutter Speed 2000.
'''
pro2 = '''detailed wallpaper like pencil drawing of pretty girl wearing school swimsuite in splash and summer sky, brunette long hairstyle, white glowing skin, jewelry eyes, perfect symmetrical face with blush cheeks, cleavage breasts and thigh, by ilya kuvshinov and alphonse mucha, golden hour lighting, strong rim light, splash particles, intense shadows, by Canon EOS, SIGMA Art Lens'''
pro3 = '''detailed wallpaper like pencil drawing of loli
girl wearing swimsuite in splash and summer sky, brunette bob hairstyle, glowing white skin, jewelry eyes, perfect symmetrical face with blush cheeks, cleavage breasts and thigh, by ilya kuvshinov and alphonse mucha, soft focus golden hour lighting, strong rim light, splash particles, intense shadows, by Canon EOS SIGMA Art Lens
Negative prompt: nipples, mutated hands, mutated fingers'''
pro4 = '''detailed wallpaper like pencil drawing of loli girl wearing swimsuite in splash and summer sky, brunette bob hairstyle, glowing white skin, jewelry eyes, perfect symmetrical face with blush cheeks, cleavage breasts and thigh, by ilya kuvshinov and alphonse mucha, soft focus golden hour lighting, strong rim light, splash particles, intense shadows, by Canon EOS SIGMA Art Lens
Negative prompt: nipples, mutated hands, mutated fingers'''
pro5 = '''fantastic book cover art of cute little princess, Platinum blonde wavy long hairstyle, white skin, blue eyes, perfect symmetrical face, beautiful long dress with many frills, by krenz cushart and alphonse mucha and stanley lau and artem demura and peter mohrbacher, soft focus, artstation, artgerm, vibrant colors, strong rim light, golden hour, splash.'''
pro6 = '''fantasitic CG unity wallpaper of beautiful elf like Cleopatra, perfect symmetrical face ruby eyes with elegant eyelashes pale pink short hairstyle glowing skin, gothic corset with frills cleavage breasts, by alphonse mucha and krenz cushart, artgerm strong rim light flower particles golden hour soft focus by Canon EOS, SIGMA Art Lens 35mm.'''
pro7 = '''extremely detailed 8k wallpaper of a beautiful lovely sweet cute loli girl like granblue_fantasy and azur_lane with frilled lace thighhighs many frills ( lovely sweet loli moe face) thighs glowing skin orange eyes like (topaz) fluttery dress with jewelry long silver wavy hair blush cheeks cinematic lighting bokeh highlight cinematicpostprocessing
Negative prompt: 2girls 3girls anatomy disconnected_limbs floating_limbs huge_breasts large_breasts late_teen long_body long_neck malformed_hands medium_breasts missing_limb mutation nipples octane_renderer pablo_picasso poorly_drawn portrait portrait_face pussy snuggled'''
pro8 = '''1girl, beautiful princess in light blue dress with wavy hair sitting on the sofa in greenhouse, intricate human hands fingers, perfect symmetrical pretty face with pretty lively eyes, flowers, perfect pupil of the anime eyes, portrait, many jewelry accessories, wide shot , blush, anime concept art, perfect shadow, sharp contrast, dramatic lighting, vivid color, highly colorful'''

# , golden hour lighting 
general="1girl, artgerm, portraiture, beautiful detailed CG unity 8k wallpaper of cute girl" # , 
effect="halo, intense shadows, strong rim light"
hair="aqua long hair"
face="perfect symmetrical face, jewely eyes with with elegant eyelashes"
body="white skin, loli" # , cleavage breasts, thighs, steaming body 
cloth="school uniform, silver maid dress" # "lace frill dress, lolita, veil" # , skirt, school uniform
emotion="closed mouth" # , flooded tears
pose=""
environment = "white background, summer" # "autumn, gold time"
authors_1 = "by ilya kuvshinov and alphonse mucha" 
authors_2 = "by dysoor and fataaa and namaonpa and yuyupiko01"
authors_3 = "by krenz cushart and stanley lau and artem demura and alphonse mucha and peter mohrbacher"
authors = authors_2
# camera = "by Canon EOS SIGMA Art Lens, SIGMA Art Lens 35mm F1.4, ISO 200 Shutter Speed 2000"
camera = "by Canon EOS SIGMA Art Lens"
description = "water drop skin, silky hair, childlike features" # , moon iris
makeup = "Pink eyeshadow, peach blush"
jewerly = "crystal glitter silver jewelry, slender hairpin"
misc = "pencil"
# misc = "pencil, novel"

# esic = "heart"
# environment = "summer, blue sky"
# prompt = ",".join([general, effect, hair, face, body, cloth, emotion, pose, environment, authors, camera, description, makeup, jewerly, misc])



#################################
# Prompt & Config
#################################
# close-up portrait
prompts = [
	###### Style ######
	# "detailed CG wallpaper like pencil drawing",
	# "fanart, lineart",
	# "detailed CG wallpaper",
	"anime",
	# "manga",
	# "artgerm",
	# "solo",
	# "portraiture",
	# "full body",

	###### Abstract #######
	# ???????????????????????????????????????_???????????????
	# "jk",
	"black iris",
	# "iris",
	# magnolia flowers, 
	"granblue fantasy", # 4, ??????????????????
	# "genshin impact",
	# "blue archive", # 5
	# "azur lane", # 4
	"moe",
	"summer",

	###### Character ########
	"shy",
	"pure",
	"bishojo",
	"cute", # !!!
	"loli",
	# "young lovely teenager girl",
	"princess",
	# "beautiful princess in pale pink lace dress",
	# , glowing skin, 
	"white",
	"glowing", # !!!
	"skin",
	"jewelry eyes", # !!!
	"elegant eyelashes",
	# "silky hair",
	"pink eyeshadow",
	"peach blush cheeks",
	"perfect symmetrical face",
	# , pale pink hair
	# "green hair",
	# "frilled lace stockings",
	# "translucent lolita dress",
	"school uniform",
	"skirt",
	# "thighhighs"
	# "lace frill",
	"shoulders",
	# "wedding veil",
	# "long braid hair",
	# "cleavage",
	# "huge breasts",
	# "thighs",
	# "legs",
	# "many jewelry accessories",
	# "standing",
	# "standing with hands behind waist",
	# "closed mouths",
	# "intricate human hands fingers",

	###### Environment/Light ########
	# "aqua background",
	# "The warm and warm sunshine in the spring shines on the girl"
	# "gold hour",
	# "golden sunlight"
	# "icy blue moonlight",
	"moonlight",

	###### Effect ########
	# "cinematic",
	# "strong rim light",
	# "highlight, cinematicpostprocessing",

	###### Camera/Authors #######
	# "by ilya kuvshinov", # 7
	"by alphonse mucha",
	# "by Justin Gerard", # 4
	# "by Canon EOS SIGMA Art Lens 35mm",
]
prompts = [
	"cute", ###
	"bishojo", ###
	"pink", ###
	"lolita", #

	"white", ###
	"glowing", # 
	"skin", ###

	"jewelry eyes", ###
	"elegant eyelashes", #
	"violet",
	"eyeshadow", ###
	"blush cheeks", ###
	"silky silver hair",

	"shy", #
	"pure", #
	"cute",

	"holy",
	"lace", #
	"dress", #
	"thighhighs", #

	# "full body",
	"black iris", ###

	"thighs", ###
	"shoulders",
	"beauty",
	"legs", ###

	# "moe", #
	"anime", ###

	###### Environment/Light ########
	# "icy",
	"detailed fantasitic CG wallpaper",
	"translucent", #
	"moonlight", #

	###### Effect ########
	# "artgerm", ###

	###### Camera/Authors #######
	"sweet",
	"loli", ###
	"beautiful",
	"princess", #
	"lovely", #
	"maiden", #
	", granblue fantasy", # 4, ??????????????????
	# ", by alphonse mucha",
	", by Justin Gerard", # 4
	", by Canon EOS SIGMA Art Lens",
]
check_prompt_len = True

config_filepath = "./config/loli_princess_blackiris.json"
config = {
	# prompt: ??????????????????????????????????????????????????????danbooru??????tag
	#    ??????????????????????????????????????????
	"prompts": prompts,
	# seed: ?????????????????????????????????None??????????????????????????????????????????????????????????????????????????????
	#    ?????????eta??????0???????????????????????????????????????????????????????????????????????????
	"seed": None,
	# n: ?????????????????????
	"n": 50,
	# height, width: ??????????????????512x512???6G??????????????????
	# 512  x 512
	# 640  x 384
	# 768  x 256
	# 896  x 256
	# 1024 x 256
	"height": 640,
	"width": 384,
	# keep_origin: ?????????????????????inpaint??????????????????True??????????????????????????????????????????mask???????????????100%???????????????????????????????????????????????????inpaint???????????????????????????guidance_scale?????????????????????
	"keep_origin": True,
	# strength: ??????inpaint???img2img????????????????????????AI???????????????????????????0~1?????????????????????0.8
	"strength": 0.8,
	# num_inference_steps: ??????????????????????????????30~100?????????????????????50
	"num_inference_steps": 30,
	# guidance_scale: ????????????????????????????????????????????????????????????????????????????????????????????????7.5
	"guidance_scale": 5.5,
	# eta: ?????????????????????????????????0??????????????????????????????1???????????????????????????
	#    This includes an original DDPM generative process when ?? = 1 and DDIM when ?? = 0.
	"eta": 0.0,
	# name: ?????????????????????????????????????????????????????????None?????????????????????????????????
	"name": None,
}



#################################
# Join prompts
#################################
def JoinPrompt(prompts) -> str:
	return " ".join(prompts)
# promptr = prompt.replace(",", " ")
config["prompt"]: str = JoinPrompt(config["prompts"])



#################################
# Check prompt length
#################################
def check_prompt_length(prompt):
	from transformers import CLIPTokenizer

	tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14") 
	tokens = tokenizer(prompt, truncation=False, return_tensors="pt")
	tokens_len = tokens.input_ids.shape[-1]

	if tokens_len > tokenizer.model_max_length:
		print(f"Too many tokens of length {tokens_len}, while max_length is {tokenizer.model_max_length}.")
	else:
		print(f"tokens_len: {tokens_len}.")

if check_prompt_len:
	check_prompt_length(config["prompt"])




#################################
# Build configs
#################################
def TestEachKeyword(config):
	import copy
	template_config = config
	configs = []
	for prompt_del in config["prompts"]:
		config = copy.copy(template_config)
		config["prompts"]: list[str] = copy.copy(config["prompts"])
		config["prompts"].remove(prompt_del)
		config["prompt"] = JoinPrompt(config["prompts"])
		config["name"] = prompt_del
		configs.append(config)
	return configs
	

configs = [config]
# configs = TestEachKeyword(config)



#################################
# Save the config file
#################################
print(">>> " + config_filepath)

with open(config_filepath, mode="w", encoding="utf8") as f:
	import json
	json.dump(configs, f, indent=4)
