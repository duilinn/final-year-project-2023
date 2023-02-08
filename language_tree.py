import re

father_path = "C:\\Users\\david\\TCD\\4th year\\final year project\\daughter_etymology.txt"
father_file = open(father_path, encoding='utf-8')
father_etymology = father_file.read()

languages_list_path = "C:\\Users\\david\\TCD\\4th year\\final year project\\languages_list.txt"
languages_list_file = open(languages_list_path, encoding='utf-8')
languages_list = languages_list_file.read().split('\n')

#print("-----\nfather_etymology = " + str(father_etymology) + "\n-----")


#tree data structure for languages and language info

class Tree:
    def __init__(self, language, parent_language="", word = "", coords=[0,0]):
        self.children = []
        self.language = language
        self.word = word
        self.parent_language = parent_language

    def get_children(self):
        return self.children
    
    def add_child(self, language, parent_language="", word="", level=0,  coords=[0,0]):
        prefix = ""
        for i in range(level): prefix += "\t"

        #print(prefix+"self: {0}: adding child {1}|{2}|{3}".format(self.language, language,parent_language,word))

        child = Tree(language, parent_language, word)
        if (parent_language==self.language):
            #print(prefix+"MATCH: adding to self {0} -> {1}".format(self.language, language))
            self.children.append(child)
            #print("adding")

        elif (len(self.children) > 0):
            #print(prefix+"MISMATCH: l={0}|par={1}|self={2}".format(\
            #language, parent_language, self.language))
            for x in self.children:
                x.add_child(language, parent_language, word, level+1)
        
    def add_word(self, language, word="", level=0):
            prefix = ""
            for i in range(level): prefix += "\t"

            #print(prefix+"self: {0}: adding word {1}|{2}".format(\
            #self.language, language,word))


            if (language==self.language):
                #print(prefix+"MATCH: adding to self {0}: {1}".format(self.language, word))
                self.word = word
                #print("adding")

            elif (len(self.children) > 0):
                #print(prefix+"MISMATCH: l={0}|self={1}".format(\
                #language, self.language))
                for x in self.children:
                    x.add_word(language, word, level+1)
                    
    def print_tree(self, current_level=0, lc=[]):

        for i in range(current_level - 1):
            if (lc[i]): print("     ",end="")
            else: print("│    ",end="")

        print("├───",end="")
            #else: print("├───",end="")
        
        print(self.language,end="")# + " " + self.word)
        if (self.word != ""): print(": " + self.word,end="")
        #print(".".join((["O" if x else "." for x in lc])))
        print()
        #print("self.get_children = {0}".format(len(self.get_children())))

        number_of_children = len(self.get_children())

        for x in range(len(self.get_children())):
            new_lc = lc[:]
            new_lc.append(x == (number_of_children-1))
            self.get_children()[x].print_tree(current_level+1, new_lc)
                



ie_tree = Tree("Proto-Indo-European",coords=[49.4, 31.2])
ie_tree.add_child("Proto-Germanic", "Proto-Indo-European",coords=[54.9, 9.2])

ie_tree.add_child("Old Frisian", "Proto-Germanic",coords=[53.35, 6.80])
ie_tree.add_child("West Frisian", "Old Frisian",coords=[53.14, 5.86])
ie_tree.add_child("Old Dutch", "Proto-Germanic",coords=[52.16, 5.20])
ie_tree.add_child("Middle Dutch", "Old Dutch",coords=[51.66, 5.34])
ie_tree.add_child("Dutch", "Middle Dutch", coords=[52.00, 5.00])
ie_tree.add_child("Old Saxon", "Proto-Germanic",coords=[52.37, 9.72])
ie_tree.add_child("Middle Low German", "Old Saxon",coords=[53.14, 9.67])
ie_tree.add_child("Old High German","Proto-Germanic",coords=[49.8,10.0])
ie_tree.add_child("Middle High German", "Old High German",coords=[50.4,11.7])
ie_tree.add_child("German", "Middle High German")

ie_tree.add_child("early Scandinavian", "Proto-Germanic")
ie_tree.add_child("Old Icelandic","early Scandinavian")
ie_tree.add_child("Norn", "early Scandinavian")
ie_tree.add_child("Old Swedish", "early Scandinavian")
ie_tree.add_child("Swedish", "Old Swedish")
ie_tree.add_child("Old Danish", "early Scandinavian")
ie_tree.add_child("Danish", "Old Danish")

ie_tree.add_child("Gothic", "Proto-Germanic")

ie_tree.add_child("Proto-Indo-Iranian", "Proto-Indo-European")
ie_tree.add_child("Sanskrit", "Proto-Indo-Iranian")
ie_tree.add_child("Old Avestan", "Proto-Indo-Iranian")
ie_tree.add_child("Younger Avestan", "Proto-Indo-Iranian")

ie_tree.add_child("ancient Greek", "Proto-Indo-European")

ie_tree.add_child("classical Latin", "Proto-Indo-European")
ie_tree.add_child("Old French","classical Latin")
ie_tree.add_child("Middle French","Old French")
ie_tree.add_child("Old Occitan","classical Latin")
ie_tree.add_child("Occitan","Old Occitan")
ie_tree.add_child("Catalan","classical Latin")
ie_tree.add_child("Spanish","classical Latin")
ie_tree.add_child("Portuguese","classical Latin")
ie_tree.add_child("Italian","classical Latin")

ie_tree.add_child("Oscan", "Proto-Indo-European")

ie_tree.add_child("Proto-Celtic", "Proto-Indo-European")
ie_tree.add_child("Gaulish","Proto-Celtic")
ie_tree.add_child("Early Irish","Proto-Celtic")

ie_tree.add_child("Armenian","Proto-Indo-European")

ie_tree.add_child("Tocharian A","Proto-Indo-European")
ie_tree.add_child("Tocharian B","Proto-Indo-European")

ie_tree.print_tree(0, [False])

language_words_pairs = []

#parse lines according to
#LANGUAGE_NAME - WORD_INFO - LANGUAGE NAME- WORD_INFO


language_vs_word_positions = ""
x = 0
item = father_etymology


#locate language-words pairs

while (x < len(item)):
    lang_found = False
    
    for language in languages_list:
        #if item.find(language) == x:
        indices = [index for index in range(len(item)) if item.startswith(language, index)]
        if x in indices:
            lang_found = True
            lang_length = len(language)

            for j in range(lang_length):
                language_vs_word_positions += "l"
                x += 1
        #else:
            #print("item: \n {0} \n language: {1}\nx: {2}\nitem.find(language): {3}".format(item,language,x,item.find(language)))
    if (not lang_found):
        language_vs_word_positions += "w"
        x += 1

#print("item:\n{0}\n\nlvw:\n{1}\n".format(item, language_vs_word_positions))
#break up each language-words pair

j = 0

punctuation = "<>().:;"
while (j < len(item)):
    #print("j = {0}".format(j))
    current_language = ""
    current_words = ""

    while (language_vs_word_positions[j] == "l"):
        if (item[j] not in punctuation): current_language += item[j]
        j += 1

    while (j < len(item) and language_vs_word_positions[j] == "w"):
        if (item[j] not in punctuation): current_words += item[j]
        j += 1

    current_language = current_language.strip()
    current_words = current_words.strip()
    
    if current_words[-1] == ",": current_words = current_words[:-1]

    #fix nordic languages


    #print("current_language, current_words = " + current_language + " | " + current_words + "\n")
    language_words_pairs.append([current_language,current_words])

language_words_pairs = [[x.strip(),y.strip()] for [x,y] in language_words_pairs]

#add words to language tree
for [language_name, words] in language_words_pairs:
    ie_tree.add_word(language_name, words)

print ("\n#####################################\n")

ie_tree.print_tree()

"""
Etymology: Cognate with Old Frisian fader , feder (West Frisian
faar ), Old Dutch fadar , fader (Middle Dutch v ̄ader , Dutch vader
), Old Saxon fadar , fader (Middle Low German v ̄ader ), Old High
German fater (Middle High German vater , German Vater ), early
Scandinavian (runic: Sweden) faþiR , Old Icelandic faðir , Norn
(Orkney) fa , (Shetland) fy (definite form fyrin ), Old Swedish faþir
(Swedish fader , (now usually) far ), Old Danish fathær (Danish
fader , (now usually) far ), Gothic fadar (in an isolated attestation
in Galatians 4:6; the ordinary word is atta : see dad n.1),
< the same Indo-European base as Sanskrit pitr. , Old Avestan ptar
(Younger Avestan pitar ), ancient Greek , classical Latin pater ( >
Old French paire , pedre , Old French, Middle French pere , French
père , Old Occitan, Occitan paire , Catalan pare , Spanish padre ,
Portuguese pãe , Italian padre ), Oscan patir , Gaulish ater- , atr- ,
Early Irish athair , Armenian hayr , Tocharian A p ̄acar , Tocharian
B p ̄acer ,
probably originally a derivative (with suffixation) of a nursery word
of the pa type (see papa n.2). A similar suffix is found in other
Indo-European relationship terms (compare mother n.1, brother n.,
daughter n.), although these suffixes may ultimately be of different
origin.
"""