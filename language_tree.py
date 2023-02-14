import re
from entries import entries

languages_list_path = "C:\\Users\\david\\TCD\\4th year\\final year project\\languages_list.txt"
languages_list_file = open(languages_list_path, encoding='utf-8')
languages_list = languages_list_file.read().split('\n')

#print("-----\nfather_etymology = " + str(father_etymology) + "\n-----")

lang_dict = {
    "Early Runic" : "Old Norse",
    "Early Scandinavian (runic: Sweden)" : "Old Norse",
    "(Orkney)" : "Norn (Orkney)",
    "(Shetland)" : "Norn (Shetland)",
    "Orkney" : "Norn (Orkney)",
    "Shetland" : "Norn (Shetland)",
    "Norn Orkney" : "Norn (Orkney)",
    "Norn Shetland" : "Norn (Shetland)",
    "early Irish" : "Old Irish",
}

#tree data structure for languages and language info
def base_form(lang):
    if lang in lang_dict:
        return lang_dict[lang]
    else:
        return lang

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
            print(prefix+"MATCH: adding to self {0} -> {1}".format(self.language, language))
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


            if (base_form(language)==self.language):
                #print(prefix+"MATCH: adding to self {0}: {1}".format(self.language, word))
                self.word = word
                #print("adding")

            elif (len(self.children) > 0):
                #print(prefix+"MISMATCH: l={0}|self={1}".format(\
                #language, self.language))
                for x in self.children:
                    x.add_word(language, word, level+1)
                    
    def print_tree(self, current_level=0, lc=[],force_show = False, ancestor_langs=[]):

        #print this node

        if (self.word !="" or force_show):
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

        #print children

        number_of_children = len(self.get_children())

        for x in range(len(self.get_children())):
            new_lc = lc[:]
            new_lc.append(x == (number_of_children-1))
            new_ancestor_langs = ancestor_langs[:]
            new_ancestor_langs.append(self.language)

            self.get_children()[x].print_tree(current_level+1, new_lc, force_show,new_ancestor_langs)
                

while(True):
    #choose English word to get its etymology
    chosen_word = input("Enter an English word: ")
    if chosen_word in entries:
        full_item = entries[chosen_word]
    else:
        continue

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

    ie_tree.add_child("Old Norse", "Proto-Germanic")
    ie_tree.add_child("Old Icelandic","Old Norse")
    ie_tree.add_child("Norn", "Old Norse")
    ie_tree.add_child("Norn (Shetland)", "Old Norse")
    ie_tree.add_child("Norn (Orkney)", "Old Norse")
    ie_tree.add_child("Old Swedish", "Old Norse")
    ie_tree.add_child("Swedish", "Old Swedish")
    ie_tree.add_child("Old Danish", "Old Norse")
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
    ie_tree.add_child("Anglo-Norman","Old French")
    ie_tree.add_child("Old Occitan","classical Latin")
    ie_tree.add_child("Occitan","Old Occitan")
    ie_tree.add_child("Catalan","classical Latin")
    ie_tree.add_child("Spanish","classical Latin")
    ie_tree.add_child("Portuguese","classical Latin")
    ie_tree.add_child("Italian","classical Latin")

    ie_tree.add_child("Oscan", "Proto-Indo-European")

    ie_tree.add_child("Proto-Celtic", "Proto-Indo-European")
    ie_tree.add_child("Gaulish","Proto-Celtic")
    ie_tree.add_child("Old Irish","Proto-Celtic")
    ie_tree.add_child("Irish","Old Irish")
    ie_tree.add_child("Welsh","Proto-Celtic")

    ie_tree.add_child("Armenian","Proto-Indo-European")

    ie_tree.add_child("Tocharian A","Proto-Indo-European")
    ie_tree.add_child("Tocharian B","Proto-Indo-European")

    ie_tree.add_child("Early Runic","Proto-Germanic")

    ie_tree.add_child("Mycenaean Greek","Proto-Indo-European")

    ie_tree.add_child("Proto-Balto-Slavic","Proto-Indo-European")
    ie_tree.add_child("Proto-Baltic","Proto-Balto-Slavic")
    ie_tree.add_child("Old Prussian","Proto-Baltic")
    ie_tree.add_child("Lithuanian","Proto-Baltic")

    ie_tree.add_child("Proto-Slavic","Proto-Balto-Slavic")
    ie_tree.add_child("Old Church Slavonic","Proto-Slavic")

    #ie_tree.print_tree(0, [False], force_show=True)

    language_words_pairs = []

    #parse lines according to
    #LANGUAGE_NAME - WORD_INFO - LANGUAGE NAME- WORD_INFO


    language_vs_word_positions = ""
    x = 0

    #split item into origin and etymology
    etymology_start = full_item.find("Etymology: ")

    origin = full_item[8:etymology_start]
    item = full_item[etymology_start + 11:]

    print("Origin: V\n"+ origin +"\netymology: V\n"+item+"-----")

    #locate language-words pairs

    while (x < len(item)):
        lang_found = False
        
        for language in languages_list:
            #print("{0}, {1}\t".format(x, language),end="")
            #if item.find(language) == x:
            indices = [index for index in range(len(item)) if item.startswith(language, index)]
            #print("Found at indices {0}".format(str(indices)))
            if x in indices:
                print("MATCH FOUND:\t",end="")
                print("{0}, {1}\t".format(x, language),end="")
                print("Found at indices {0}".format(str(indices)))
            
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

        key_words_that_remove = ["now chiefly","and further ", "plural",\
                                 "inflected","now usually","in an isolated",\
                                "apparently ","also ","and also ",\
                                "although ", "10th ", "11th ", "12th ",\
                                "13th ", "14th ", "15th ", "16th ",
                                "17th ", "18th ", "19th ", "20th ",\
                                "strong and ","or its ", "only attested",\
                                "base ","alive","weak", "further etymology ",\
                                "Further etymology ", "probably ",\
                                "‘to", "base as ", "definite form ",\
                                "to ", "impersonal ", "organized"]
        
        min_location = 10000
        for key_word in key_words_that_remove:
            #print("{0}:\t{1}".format(current_words, key_word))
            location = current_words.find(key_word)
            if location > -1 and location < min_location:
                #print("FOUND")
                min_location = location
        
        if min_location < 10000:
            current_words = current_words[0:min_location]

        current_language = current_language.strip()
        current_words = current_words.strip()
        
        if len(current_words) > 0 and current_words[-1] == ",": current_words = current_words[:-1]

        #fix nordic languages


        print("current_language, current_words = " + current_language + " | " + current_words)
        language_words_pairs.append([current_language,current_words])

    language_words_pairs = [[x.strip(),y.strip()] for [x,y] in language_words_pairs]
    language_words_pairs = [[x,y] for [x,y] in language_words_pairs if x != "" and y != ""]

    print(str(language_words_pairs))
    #add words to language tree
    for [language_name, words] in language_words_pairs:
        print("adding {0}, {1}".format(language_name, words))
        ie_tree.add_word(language_name, words)

    print ("\n#####################################\n")

    ie_tree.print_tree(force_show=False)

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
origin."""