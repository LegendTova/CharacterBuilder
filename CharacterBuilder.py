import sys
import socket
import ssl
import re
import random
def main():
	classes = ["artificer", "barbarian", "bard", "blood hunter", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"]
	racialFeats = []
	feats = []
	#stats = getBaseStats()
	stats = [10, 10, 10, 10, 10, 10]
	
	backgroundData = getBackground()

	race = input("What is your characters race?")
	race = race.lower()
	
	racialFeats, subraceFeats = raceProcessing(race, stats)
	
	racialFeats = racialCleanUp(racialFeats)
	
	subraceFeats = racialCleanUp(subraceFeats)
	
	classStart = choice(classes)[0]
	
	while True:
		try:
			classLevel = input("how many levels are you taking in this class: ")
			classLevel = int(classLevel)
			if classLevel < 1 or classLevel > 20:
				print("\nERROR: number not in range 1 to 20")
				continue
		except:
			print("\nERROR: invalid entry! Enter a number from 1 to 20")
			continue
		
		break
		
	classFeats, subclassFeats, equipment, absoluteProfs, stats, feats = classProcessing(classStart, classLevel, stats);
	
	backgroundData[3] = re.sub(r"Value:\d+\w+ Weight:\d+\w+", r"", backgroundData[3])
	backgroundData[3] = backgroundData[3].split(", ")
	backgroundData[3][len(backgroundData[3]) - 1] = backgroundData[3][len(backgroundData[3]) - 1][4:]
	
	equipment.extend(backgroundData[3]) 
	
	absoluteProfs[2] = absoluteProfs[2].extend(backgroundData[2])
	st = absoluteProfs[3] 
	absoluteProfs[4].extend(backgroundData[1])
	skills = absoluteProfs[4]
	absoluteProfs = absoluteProfs[:2] 
	absoluteProfs.extend(backgroundData[4].split(", "))
	backgroundData = backgroundData[0]	
	
	speed = getSpeed(racialFeats, subraceFeats, classStart, classFeats)
	
	ac = getAC(equipment, classFeats, stats)
	
def getBaseStats():
	stats = [10, 10, 10, 10, 10, 10]
	
	stats[0] = input("Whats you Strength ability score: ")
	stats[1] = input("Whats you Dexterity ability score: ")
	stats[2] = input("Whats you Constitution ability score: ")
	stats[3] = input("Whats you Intelligence ability score: ")
	stats[4] = input("Whats you Wisdom ability score: ")
	stats[5] = input("Whats you Charisma ability score: ")

def getSpeed(racialFeats, subraceFeats, c, classFeats):

	speed = []

	if c in ["barbarian", "monk"]:
		print()
		# get page and dial down to table(like spell)
	
	for i in subraceFeats:
		if "base walking speed" in i[1]:
			temp = i[1].split(" ")
			speed.append(int(temp[len(temp) - 2]))
			
	for i in racialFeats:
		if "base walking speed" in i[1]:
			temp = i[1].split(" ")
			speed.append(int(temp[len(temp) - 2]))
	
	return findMax(speed)
	
def getAC(equipment, classFeats, stats):
	ac = [10]

	if c in ["barbarian", "monk"]:
		for i in classFeats:
			if "Unarmored Defense" in i[0]:
				str = re.search(r'\b10 + your \w+ modifier + your \w+ modifier.\b', i[1])
				
				if "Constitution" in str:
					ac = 10 + (stats[2] - 10) / 2)
				elif "Wisdom" in str
					ac = 10 + (stats[4] - 10) / 2)
	
	armor = []
	shield = False
	
	for i in equipment:
		if "armor" in i:
			armor.append(i)
		elif "shield" in i:
			shield = True

	page = connection("http://dnd5e.wikidot.com/armor", "Light")
	
	armorStats = []
	
	for i in armor:
		j = 0
		while removeTags(i) not in page[j].lower():
			j = j + 1
			
		armorStats.append(removeTags(page[j+1]))
	
	for i in range(0, len(armorStats)):
		base = int(armorStats[i].split(" + ")[0])
		if "Dex" in armorStats[i]:
			dex = int((stats[2] - 10)/2)
			
			if "max 2" in armorStats[i]:
				if dex > 2:
					armorStats[i] = base + 2
				else:
					armorStats[i] = base + dex
			else:
				armorStats[i] = base + dex
				
		else:
			armorStats[i] = base
	
	return findMax(armorStats)
		
def getInitiative(classFeats, stats, feats):
	initiative = stats[1]
	
	for i in feats:
		if "alert" in i[0].lower():
			initiative = initiative + 5
	
	for i in classFeats:
		if "You can give yourself a bonus to your initiative rolls equal to your " in i[1]:
			temp = i[i].split("You can give yourself a bonus to your initiative rolls equal to your ")[1].split(" ")[0].lower()
			if "charisma" in temp:
				initiative = initiative + stats[5]
			elif "wisdom" in temp:
				initiative = initiative + stats[4]
			elif "intelligence" in temp:
				initiative = initiative + stats[3]
				
	return initiative
	
def raceProcessing(r, stats):
	print("-----RACE-----")
	useTashas = ""
	useUA = ""
	error = ""
	
	while useTashas.lower() not in ["y", "n", "yes", "no"]:
		print(error)
		useTashas = input("are you using tashas racial ability score increase? (y/n)")
		
		error = "Invalid reponse! Please use enter y for yes or n for no"
	
	error = ""	
	while useUA.lower() not in ["y", "n", "yes", "no"]:
		print(error)
		useUA = input("are you including UA(unearthed arcana)? (y/n)")
		
		error = "Invalid reponse! Please use enter y for yes or n for no"
		
	
	url = "dnd5e.wikidot.com/lineage:" + r
	
	page = connection(url, "Size")
	
	while r not in page[0].lower():
		page = page[1:]		
	
	
	page = removeUnneededRace(page)
	
	
	#subrace stuff----------------------------------
	subraces = []
	baseFeats = []
	count = -1
	for i in range(0, len(page)):
		countAb = 0
		temp = "<li"
		isBase = True
		
		if "<h1" in page[i] and "id=\"to" in page[i] and (useUA in ["y", "yes"] or "Unearthed Arcana" not in page[i]):
			subraces.append([page[i]])
			baseFeats.append([page[i]])
			count = count + 1
			for j in range(i+1, len(page)):
				if "<h1" in page[j] and "id=\"to" in page[j]:
					i = j-1
					break
				elif "<h2" in page[j] and "id=\"to" in page[j]:
					subraces[count].append([page[j]])
					countAb = countAb + 1
				
					temp = page[j]
					
					for k in range(j+1, len(page)):
						if "<h2" in page[k] and "id=\"to" in page[k]:
							j = k-1
							break
						elif "<li" in page[k]:
							subraces[count][countAb].append(page[k])
				elif "<li" in page[j] and ("<li" in temp or "Features" in temp):
					
					if isBase:
						baseFeats[count].append(page[j])
				
				if "<li" not in temp and "Features" not in temp:
						temp = page[j]
						isBase = False
					
	x = 0
	while True:
		if x == len(baseFeats):
			break
		
		if len(baseFeats[x]) < 2:
			baseFeats.remove(baseFeats[x])
			continue
			
		x = x + 1
	
	for i in range(0, len(baseFeats)):
		baseFeats[i].append([])
	
	for j in range(0, len(subraces)):
		PBH = True
	
		for i in range(1, len(baseFeats)):
			if baseFeats[i][0] == subraces[j][0]:
				for k in range(1, len(subraces[j])):
					if "Features" not in subraces[j][k][0]:
						baseFeats[i][len(baseFeats[i]) - 1].append(subraces[j][k])
						PBH = False

		if PBH:
			for k in range(1, len(subraces[j])):
				if "Features" not in subraces[j][k]:
					baseFeats[0][len(baseFeats[i]) - 1].append(subraces[j][k])
	
	baseStats = []
	
	for i in range(0, len(baseFeats)):
		baseStats.append(removeTags(baseFeats[i][0]))
	
	baseChoice = choice(baseStats)[0]				
	
	racialFeats = getBaseRacialFeatures(baseChoice, baseFeats)
	
	return racialFeats[0], racialFeats[1]

def racialCleanUp(features):

	r = []

	for i in features:
		temp = i.split(".</strong> ")
		for j in range(0, len(temp)):
			temp[j] = removeTags(temp[j])
	
		r.append(temp)
	
	return r
	
def getBackground():	
	background = ""
	page = ""
	background = input("enter background: ")
	background = background.lower()
	backgroundSearch = background
	background = background.replace(" ", "-") # use regex
	
	page = connection("dnd5e.wikidot.com/background:" + background, "Features")
	
	while ("<span>background: " + backgroundSearch) not in page[0].lower():
		page = page[1:]
	
	index = findStart(["Skill Proficiencies:"], page)
	skills = page[index][41:]
	skills = removeTags(skills)
	skills = skills.split(", ")

	tools = page[index + 1][37:]
	tools = removeTags(tools)
	tools = toolChoice(tools)
	
	language = page[index + 2][28:]
	language = removeTags(language)
	if language.lower() == "None":
		language = "";
	
	equipment = page[index + 3][28:]
	equipment = removeTags(equipment) # need to remove value from string
	
	#need features
	while "</table>" not in page[0].lower():
		page = page[1:]
	
	page = page[1:]
	
	feat = [removeTags(page[0]), removeTags(page[1])]
	
	return [feat, skills, tools, equipment, language]
	
def getBaseRacialFeatures(baseChoice, baseFeats):
	indexOfChoice = -1
	
	feats = []
	
	for i in range(0, len(baseFeats)):
		if baseChoice in baseFeats[i][0]:
			indexOfChoice = i
	
	for i in range(1, len(baseFeats[indexOfChoice]) - 1):
		feats.append(baseFeats[indexOfChoice][i])
	
	subraces = []
	
	for i in baseFeats[indexOfChoice][len(baseFeats[indexOfChoice]) - 1]:
		subraces.append(removeTags(i[0]))
	
	
	srFeats = (subraceFeats(baseFeats, subraces, indexOfChoice))
	
	return feats, srFeats
	
def subraceFeats(baseFeats, subraces, index):
	if subraces == []:
		return []

	sr = choice(subraces)[0] 
	
	for i in range(0, len(baseFeats[index][len(baseFeats[index]) - 1])):
		if sr in baseFeats[index][len(baseFeats[index]) - 1][i][0]:
			return baseFeats[index][len(baseFeats[index]) - 1][i][1:]
		
	
def classProcessing(c, classLevel, stats):
	c = c.replace(" ", "-")
	url = "dnd5e.wikidot.com/" + c
	
	page = connection(url)
	
	while c not in page[0].lower():
		page = page[1:]
	
	absoluteProfs = getProficency(page)
	
	equipment = equipmentChoice(page)
	
	classFeats = isolateAbilities(page)
	
	
	subclassLevel = findSubclassLvl(c)
	
	subclassFeats = []
	sc = ""
	
	if classLevel >= subclassLevel:
		subclassFeats, sc = getSubclass(page, c)
	
	
	for i in range(0, len(classFeats)):
		classFeats[i][1] = removeTags(classFeats[i][1])
		classFeats[i][0] = removeTags(classFeats[i][0])
	
	
	for i in range(0, len(subclassFeats)):
		subclassFeats[i][0] = removeTags(subclassFeats[i][0])
		subclassFeats[i][1] = removeTags(subclassFeats[i][1])
	
	classFeats = removeUnobtainedAbilities(classFeats, classLevel)	
	
	isMainFeat = isFeature("Spellcasting", classFeats)
	isSubFeat = isFeature("Spellcasting", subclassFeats)
	
	spellList = []
	
	if isMainFeat or isSubFeat:
		spellLvl, knownSpells, cantripSpells = 0, 0, 0
		
		if isMainFeat:
			spellLvl, knownSpells, cantripSpells = spellProcessing(c, sc, classFeats, classLevel, stats, page)
		else:
			subUrl = "dnd5e.wikidot.com/" + sc
			subPage = connection(subUrl)
			spellLvl, knownSpells, cantripSpells = spellProcessing(c, sc, classFeats, classLevel, stats, subPage)
		knownSpells = int(removeTags(knownSpells))
		
		requiredCantrips = []
		if " + " in cantripSpells:
			requiredCantrips = cantripSpells.split(" + ")
			cantripSpells = requiredCantrips[len(requiredCantrips) - 1]
			requiredCantrips = requiredCantrips[:len(requiredCantrips) - 1]
		
		cantripSpells = int(removeTags(cantripSpells))
		
		if isMainFeat:
			spellList = pickSpells(cantripSpells, knownSpells, c, spellLvl)
		else:
			spellList = pickSpells(cantripSpells, knownSpells, c, spellLvl, subclassFeats[findFeature("Spellcasting", subclassFeats)][1])

		if len(requiredCantrips) > 0:
			for i in range(0, len(requiredCantrips)):
				requiredCantrips[i] = removeTags(requiredCantrips[i])
			spellList[0].extend(requiredCantrips)
	
	#stats, feats = getAbiFeats(stats, classFeats, classLevel)
	
	feats = []
	
	return classFeats, subclassFeats, equipment, absoluteProfs, stats, feats
		
def findSubclassLvl(c):
	if c in ["sorceror", "warlock", "cleric"]:
		return 1
	elif c in ["paladin", "druid", "wizard"]:
		return 2
	else:
		return 3
	

def connection(url, search="1st"):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	extension = "/";
	
	try:
		s.connect((url, 80))
	except:
		extension = url[url.find("/"):]
		url = url[:url.find("/")]
		s.connect((url, 80))
	
	
	sendAdd = "GET " + extension + " HTTP/1.1\r\nHost: " + url + "\r\n\r\n"
	
	s.send(sendAdd.encode())
	
	r = s.recv(10485760000).decode()

	while search not in r:
		r = s.recv(10485760000).decode()
	
	s.close()
	
	r = r.split("\n")
	
	return r
def getProficency(page):
	index = findStart(["Proficiencies", "h5"], page)
	
	armor = page[index + 1][27:]
	armor = armor[:(len(armor) - 6)]
		
	weapons = page[index + 2][26:]
	weapons = weapons[:(len(weapons) - 6)]
	
	tools = page[index + 3][24:]
	tools = tools[:(len(tools) - 6)]
	tools = toolChoice(tools)

	st = page[index + 4][32:]
	st = st[:(len(st) - 6)]
	st = st.split(", ")
	
	skills = page[index + 5][25:]
	skills = skills[:(len(skills) - 4)]
	skills = skillChoice(skills)
	
	return [armor, weapons, tools, st, skills]

	
def toolChoice(tools):
	tools = tools.split(", ")
	r = []
	for i in range(0, len(tools)):
		choices = []
		num = 1
		
		
		if "artisan" in tools[i]:
			choices.extend(readTxt('./data/artisan.txt'))
		if "musical" in tools[i]:
			choices.extend(readTxt('./data/instrument.txt'))
		if "gaming" in tools[i]:
			choices.extend(readTxt('./data/gaming.txt'))
		
		if len(choices) == 0:
			continue
		
		if "three" in tools[i].lower():
			num = 3
		elif "two" in tools[i].lower():
			num = 2
		
		chosen = choice(choices, num)
		str = ""
		
		r.extend(chosen)

	for i in tools:
		iLow = i.lower()
		if "one" not in iLow and "two" not in iLow and "three" not in iLow:
			r.append(i)
	
	return r

def hitpoints(c, stats, lvl):
	
	dice = -1
	hp = 0
	
	if "barbarian" in c:
		dice = 12
	elif c in ["fighter", "paladin"]:
		dice = 10
	elif c in ["wizard", "sorcerer"]:
		dice = 6
	else:
		dice = 8
		
	for i in range(0, dice):
		hp = hp + random.randrange(1, dice)
		
	hp = hp + int((stats[2] - 10) / 2) * lvl

	return hp
	
def spellProcessing(c, sc, classFeats, classLevel, stats, page):
	
	isMainCaster = c in ["artificer", "bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
	
	if isMainCaster:
		while ("the " + c + "</th>") not in page[0].lower():
			page = page[1:]
	else:
		temp = sc.split(":")[1].split("-")
		str = ""
		for i in temp:
			str = str + i + " "
		str = str[:len(str)-1]

		while (str + " spellcasting</th>") not in page[0].lower():
			page = page[1:]
	
	cut = 0
	while ("</table>") not in page[cut].lower():
		cut = cut + 1
		
	page = page[:cut]
	
	headerSave = []
	
	rowCount = 0
	addNum = 2
	if not isMainCaster:
		addNum = 0
	
	while rowCount < classLevel + addNum:
		if page[0] == '</tr>':
			rowCount = rowCount + 1
		page = page[1:]
		
		if rowCount == 1:
			i = 1
			while page[i] != "</tr>":
				headerSave.append(page[i])
				i = i + 1
				
			rowCount = rowCount + 1 
	
	cut = 0
	while page[cut] != "</tr>":
		cut = cut + 1
			
	page = page[1:cut]
	
	knownIndex, cIndex = findKnown(c, headerSave)
	
	sIndex = -1
	spellList = 1
	

	if "warlock" in c:
		sIndex = findIndex(headerSave, "Slot Level")
		spellLvl = int(removeTags(page[sIndex])[:1])
	else:
		sIndex = findIndex(headerSave, "1st")
		spellLvl = findMaxSpellLevel(sIndex, page)
	
	if isMainCaster:
		if "wizard" in c:
			return spellLvl, str(classLevel * 2 + 4), page[cIndex]
		elif "druid" in c or "cleric" in c:
			return spellLvl, prepSpells(stats[4], classLevel), page[cIndex]
		elif "artificer" in c:
			return spellLvl, prepSpells(stats[3], classLevel, 2), page[cIndex]
		elif "paladin" in c:
			return spellLvl, prepSpells(stats[5], classLevel, 2), "0"
		elif "ranger" in c:
			return spellLvl, page[knownIndex], "0"
		else:
			return spellLvl, page[knownIndex], page[cIndex]
	else: 
		return spellLvl, page[knownIndex], page[cIndex]
def prepSpells(num, classLevel, div=1):
	n = int(int((num - 10)/2) + int(classLevel / div))
	
	print(n)
	
	if n < 1:
		return 1
	return str(n)
	
def findKnown(c, headerSave):
	if "sorcerer" in c or "warlock" in c or "bard" in c or "ranger":
		return findIndex(headerSave, "Spells Known"), findIndex(headerSave, "Cantrips Known")
	else:
		return -1, findIndex(headerSave, "Cantrips Known")
		
def pickSpells(cantrips, known, c, spellLvl, spellcastStr=""):
	r = []
	page = ""
	if spellcastStr == "":
		page = connection("dnd5e.wikidot.com/spells:" + c)
	else:
		if "artificer" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:artificer")
		elif "bard" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:bard")
		elif "cleric" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:cleric")
		elif "druid" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:druid")
		elif "paladin" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:paladin")
		elif "ranger" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:ranger")
		elif "wizard" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:wizard")
		elif "warlock" in spellcastStr:
			page = connection("dnd5e.wikidot.com/spells:warlock")
		

	
	spellList = getSpellOptions(page, spellLvl)
	spellChosen = []
	
	print("\n-------------------Cantrips-------------------")
	spellChosen.append(choice(spellList[0], cantrips))
	print("\n-------------------Level Spells-------------------")
	spellChosen.append(choice(spellList[1], known))
	
	return spellChosen
	
	

def getSpellOptions(page, spellLvl):
	
	spellNames = []
	
	for i in range(0, spellLvl):
		temp, cut = singleSpellLevel(page, i)
		page = page[cut+1:]
		spellNames.append(temp)
	
	for i in range(2, len(spellNames)):
		spellNames[1].extend(spellNames[i])
	
	spellNames = spellNames[:2]
	
	return spellNames
	
def singleSpellLevel(page, lvl=0):
	r = []

	i = 0
	#print(page)
	#exit()
	for i in range(0, len(page)):
		if "</table>" in page[i]:
			break;	
		
		if "</a>" in page[i] and "</li>" not in page[i] and "</em>" not in page[i]:
			if lvl > 0:
				r.append(removeTags(page[i]) + "(lvl " + str(lvl) + ")");
			else:
				r.append(removeTags(page[i]));
		i = i + 1
	return r, i;
	
	
def findMaxSpellLevel(start, page):
	lvl = 0
	
	while "-" not in page[start]:
		if lvl == 0:
			lvl = lvl + 1
		lvl = lvl + 1
		start = start + 1
	
	return lvl
		
def findIndex(l, str):
	for i in range(0, len(l)):
		if str in l[i]:
			return i
	return -1
	
	
def skillChoice(skills):
	num = 2
	useAll = False
	
	if "four" in skills:
		num = 4
	elif "three" in skills:
		num = 3
		
	if "any" in skills:
		useAll = True
		
	choices = []
	
	if useAll:
		choices = readTxt("./data/skills.txt")
	else:
		choices = skills.split(", ")
		i = re.search(r'\b(from )\b', choices[0])
		choices[0] = choices[0][i.end():]
		choices[len(choices) - 1] = choices[len(choices) - 1][4:]
		
	return choice(choices, num)

def equipmentChoice(page):
	index = findStart(["Equipment", "h5"], page) + 3
	
	equipment = []
	
	while "li" in page[index]:
		temp = page[index]
		temp = temp[4:len(temp) - 5]
	
		if "(a)" in page[index]:
			if "(c)" in page[index]:
				temp = temp.split(", ")				
			elif "(b)" in page[index]:
				temp = temp.split(" or ")
				
			for i in range(0, len(temp)):
				temp[i] = temp[i][4:]
				if " or " in temp[i]:
					temp[i] = temp[i][3:]
			temp = choice(temp)[0]
		
		num = 1
		
		temp = temp.split(" and ")
		
		for i in temp:
			if "two" in i:
					num = 2
		
			if "simple weapon" in i:	
				for j in range(0, num):
					choices = readTxt("./data/simple.txt")
					equipment.extend(choice(choices, 1))
			elif "martial weapon" in i:
				for j in range(0, num):
					choices = readTxt("./data/martial.txt")
					equipment.extend(choice(choices, 1))
			else:
				equipment.append(i)

		
		index = index + 1
		
	return(equipment)
	
def choice(choices, num=1):

	chosen = []

	for k in range(0, num):
			print("\n\nchoose one of the following by typing the number next to the name of your choice (eg: \"1: Choice\" means you enter 1):")
			j = 0
			while j < len(choices):
				if len(choices) - j > 3:
					print(str(j) + ": " +choices[j] + "   |  " + str(j+1) + ": "+ choices[j+1] + "   |  " + str(j+2) + ": " + choices[j+2] + "   |  " + str(j+3) + ": " + choices[j+3])
					j = j + 3
				elif len(choices) - j > 2:
					print(str(j) + ": " +choices[j] + "   |  " + str(j+1) + ": "+ choices[j+1] + "   |  " + str(j+2) + ": " + choices[j+2])
					j = j + 2
				elif len(choices) - j > 1:
					print(str(j) + ": " + choices[j] + "   |  " + str(j+1) + ": "+ choices[j+1])
					j = j + 1
				elif len(choices) - j > 0:
					print(str(j) + ": "  + choices[j])
				j = j + 1
			
			while True:
				c = input("make choice by entering the number to the left of your choice: ")
				
				try:
					if int(c) == 0 or (int(c) > 0 and int(c) <= len(choices)-1):
						chosen.append(choices[int(c)])
						choices.remove(choices[int(c)])
						break
					
					print("invalid choice, try again")
				
				except:
					print("invalid choice, try again")
			
	return chosen

def readTxt(file):
	f = open(file, 'r')
	data = f.readlines()
	for i in range(0, len(data)-1):
		data[i] = data[i][:len(data[i]) - 1]
	return data
	
def isolateAbilities(page):
	cleanedData = removeUnneeded(page);
	severeIndex = len(cleanedData)
	
	
	
	prev = ""
	
	for i in range(0, len(cleanedData)):
			
		if "At 20th level" in cleanedData[i] or "reach 20th level" in cleanedData[i] or ("." in prev and "    " in cleanedData[i]):
			severeIndex = i + 1
			break;

		prev = cleanedData[i]
	cleanedData = cleanedData[:severeIndex]
	
	for i in range(0, len(cleanedData)):
		prevChar = ""
	
		if prevChar == "<" and cleanedData[i][len(cleanedData[i]) - 1] not in ["<", ">"]:
			break;
			
		prevChar = cleanedData[i][len(cleanedData[i]) - 1]

	r = []
	i = 0
	
	while True:
		try:
			r.append([cleanedData[i], cleanedData[i+1]])
			i = i + 2
		except:
			break
	
	return r

def removeUnobtainedAbilities(feats, level):
	r = []
	
	
	stop = False
	for i in range(0, len(feats)):
		temp = feats[i][1]
		save = ""
		
		for j in range(1, level + 1):
			if " " + str(j) + "st level" in temp or " " + str(j) + "nd level" in temp or " " + str(j) + "rd level" in temp or " " + str(j) + "th level" in temp:
				r.append(feats[i])
				break
			elif j == level: 
				save = feats[i]
		
		if save != "":
			add = True
		
			for j in range(level + 1, 21):
				if " " + str(j) + "st level" in temp or " " + str(j) + "nd level" in temp or " " + str(j) + "rd level" in temp or " " + str(j) + "th level" in temp:
					add = False
					break
					
			if add:
				r.append(save)
	return r

	
def getSubclass(page, cl):
	tableIndex = findLine("Source", page)
	tableIndex = page.index(tableIndex)
	
	options = filterSubclassOp(page[tableIndex:])
	
	print("pick your subclass!")
	c = choice(options)[0]
	
	c = cl + ":" + c.lower().replace(" ", "-")
	
	url = "dnd5e.wikidot.com/" + c
	
	subclassFeats = isolateAbilities(connection(url, "3rd"))
	
	return subclassFeats, c
	
def filterSubclassOp(page):
	r = []
	
	for i in page:
		if "Unearthed Arcana" in i:
			return r
		
		if "</a>" in i:
			r.append(removeTags(i))
	

def getAbiFeats(stats, classFeats, level):

	num = 0

	for i in range(0, len(classFeats)):
		if "Ability Score Improvement" in classFeats[i][0]:
			
			for j in range(4, level):
				if str(j) in classFeats[i][1]:
					num = num + 1
					
	isFeat = ""
	
	feats = []
	
	while num > 0:
		error = ""
		while isFeat not in ["y", "n", "yes", "no"]:
			print(error)
			isFeat = input("with " + str(num) + " ABIs remaining would you like to take a feat(y/n):")
			error = "invalid response, type y or n:"
		
		if "y" in isFeat:
			feat = input("enter feat name:")
			feat = feat.lower().replace(" ", "-")
			p = connection("feat:" + feat)
	
			while feat not in p[0].lower():
				p = p[1:]
				
			feats.append(removeUnneeded(p))
		else:
			statChoice = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
			
			stat1 = choice(statChoice)
			stat2 = choice(statChoice)
			
			stats[statChoice.index(stat1)] = stats[statChoice.index(stat1)] + 1
			stats[statChoice.index(stat2)] = stats[statChoice.index(stat2)] + 1
	
	return stats, feats
	
def removeUnneeded(p):
	pR = []
	
	prev = ""
	for i in p:
		if ("<h3" in i or "<p" in i):
			pR.append(i)
		elif "<li" in i:
			pR.append("\t * " + i)
			
	pR = pR[6:]
	
	while "<h3" not in pR[0]:
		pR = pR[1:]
	
	extra = []
	
	i = 0
	
	
	while i in range(0, len(pR)):
		numSave = 0
		if "<h3" not in pR[i]:
		
			for j in range(i+1, len(pR)):
				if "<h3" not in pR[j]:
					pR[i] = pR[i] + "\n\n" + pR[j]
					extra.append(pR[j])
					numSave = numSave + 1
				else:
					break
		i = i + numSave + 1
		
	pR = [i for i in pR if i not in extra]
	
	return pR
	
def removeUnneededRace(p):
	pR = []
	
	for i in p:
		if ("<h1" in i or "<h2" in i or "<p" in i or "<li" in i):
			pR.append(i)

			
	while "<h1" not in pR[0]:
		pR = pR[1:]
	
	extra = []
	
	i = 0
	
	"""
	while i in range(0, len(pR)):
		numSave = 0
		if "<h3" not in pR[i]:
		
			for j in range(i+1, len(pR)):
				if "<h3" not in pR[j]:
					pR[i] = pR[i] + "\n\n" + pR[j]
					extra.append(pR[j])
					numSave = numSave + 1
				else:
					break
		i = i + numSave + 1
		
	pR = [i for i in pR if i not in extra]
	"""
	return pR
	
def removeTags(str):
	r = re.sub(r"<.*?>", r"", str)
	return r
	
def findStart(searchList, page):
	for i in range(0, len(page)):
		found = True
	
		for j in searchList:
			if j not in page[i]:
				found = False
				break
				
		if found:
			return i
	
	return -1
	
def findFeature(str, feats):
	for i in range(0, len(feats)):
		if str in feats[i][0]:
			return i
			
def isFeature(str, feats):
	for i in feats:
		if str in i[0]:
			return True
	
	return False
	
def findLine(str, page):
	for i in page:
		if str in i:
			return i
			
def findMax(list):
	max = list[i]
	
	for i in list:
		if i > list:
			max = i
			
	return max

if __name__ == '__main__':
	main()