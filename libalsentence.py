#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
libalsentence - lib for split text to sentences
working with russian text.

Author: Denis Popov
E-mail: d.popov93@mail.ru
Created: 10.01.2021
Version: 0.0.0.1
'''

import re
alphabets= "([A-Za-z]|[А-Яа-я])"
prefixes = "(Mr|St|Mrs|Ms|Dr|г|в|д|с|гор|сел|пос|сут|мин|ч|км|гр|л|нар|изд)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co|Корп)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "(([A-Za-z]|[А-Яа-я])[.]([A-Za-z]|[А-Яа-я])[.](?:([A-Za-z]|[А-Яа-я])[.])?)"
websites = "[.](com|net|org|io|gov|zone|click|best|vision|cool|com|online|capital|center|country|info|expert|site|xyz|space|city|team|guru|mobi|one|world|plus|net|tel|today|top|uno|town|link|pro|website|page|ru|рф|su|moscow|москва|дети|онлайн|сайт|орг|рус|agency|blog|buzz|club|digital|directory|fyi|gripe|guide|help|how|ink|media|news|press|radio|report|review|reviews|tips|wiki|camera|design|digital|gallery|graphics|live|photo|photography|photos|pics|pictures|studio|video|watch|webcam)"
puct_signs = ["\.", "\,", "\!", "\?", "\:", "\;"]

def text_to_sentences(string):
	string = " " + string + "  "
	string = string.replace("\n"," ")
	string = re.sub(prefixes,"\\1<prd>",string)
	string = re.sub(websites,"<prd>\\1",string)
	if "Ph.D" in string: string = string.replace("Ph.D.","Ph<prd>D<prd>")
	string = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",string)
	string = re.sub(acronyms+" "+starters,"\\1<stop> \\2",string)
	string = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",string)
	string = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",string)
	string = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",string)
	string = re.sub(" "+suffixes+"[.]"," \\1<prd>",string)
	string = re.sub(" " + alphabets + "[.]"," \\1<prd>",string)
	if "”" in string: string = string.replace(".”","”.")
	if "\"" in string: string = string.replace(".\"","\".")
	if "!" in string: string = string.replace("!\"","\"!")
	if "?" in string: string = string.replace("?\"","\"?")
	string = string.replace(".",".<stop>")
	string = string.replace("?","?<stop>")
	string = string.replace("!","!<stop>")
	string = string.replace("<prd>",".")
	sentences = string.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences
	
def normalize_string_array(string_array):
	str_array = []
	for string in string_array:
		if string != None:
			str_array.append(normalize_string(string))
	if not str_array:
		return None
	else:
		return str_array
	
def normalize_string(string):
	string = re.sub(":", ": ", string)
	string = re.sub(";", "; ", string)

	# Remove extra whitespaces
	string = re.sub(' +', ' ', string)
	string = re.sub('\t', '', string)
	
	# Fix punctuation signs
	for sign in puct_signs:
		string = re.sub(' +' + sign, sign[1], string)
	
	return string.lower()
