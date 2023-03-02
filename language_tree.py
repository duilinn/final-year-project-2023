import re
from entries import entries
import lingtypology
import folium

languages_list_path = "C:\\Users\\david\\TCD\\4th year\\final year project\\languages_list.txt"
languages_list_file = open(languages_list_path, encoding='utf-8')
languages_list = languages_list_file.read().split('\n')

#print("-----\nfather_etymology = " + str(father_etymology) + "\n-----")

lang_dict = {
    "Early Runic" : "Old Runic",
    "Early Scandinavian (runic: Sweden)" : "Older Runic",
    "(Orkney)" : "Old Norn",
    "(Shetland)" : "Old Norn",
    "Orkney" : "Old Norn",
    "Shetland" : "Old Norn",
    "Norn Orkney" : "Old Norn",
    "Norn Shetland" : "Old Norn",
    "Norn" : "Old Norn",
    "early Irish": "Early Irish",
    "Old Avestan": "Avestan",
    "Younger Avestan": "Avestan",
    "ancient Greek": "Ancient Greek",
    "Armenian": "Eastern Armenian"
}

#tree data structure for languages and language info
def base_form(lang):
    if lang in lang_dict:
        return lang_dict[lang]
    else:
        if len(lang) > 1: 
            return lang[0].upper() + lang[1:]
        else:
            return lang

class Tree:
    def __init__(self, language, parent_language="", word = "", coords=[0,0],tree_type="inherited"):
        self.children = []
        self.language = language
        self.word = word
        self.parent_language = parent_language
        self.tree_type = tree_type
        self.first_word = False

    def get_children(self):
        return self.children
    
    def add_child(self, language, parent_language="", word="", level=0,  coords=[0,0],tree_type="inherited"):
        prefix = ""
        for i in range(level): prefix += "\t"

        #print(prefix+"self: {0}: adding child {1}|{2}|{3}".format(self.language, language,parent_language,word))

        child = Tree(language, parent_language, word, tree_type=self.tree_type)
        if (parent_language==self.language):
            #print(prefix+"MATCH: adding to self {0} -> {1}".format(self.language, language))
            self.children.append(child)
            #print("adding")

        elif (len(self.children) > 0):
            #print(prefix+"MISMATCH: l={0}|par={1}|self={2}".format(\
            #language, parent_language, self.language))
            for x in self.children:
                x.add_child(language, parent_language, word, level+1, tree_type=self.tree_type)

    def remove_child(self, language):
        child_found = False
        new_children = self.children
        current_index = 0
        for child in self.children:
            if child.language == language:
                new_children = self.children[:current_index] + self.children[current_index+1:]
                child_found = True
            current_index += 1

        if child_found == False:
            for child in self.children:
                child.remove_child(language)
            
        self.children = new_children

    def add_word(self, language, word="", level=0,tree_type="inherited",first_word=False):
            #print(str(first_word))
            prefix = ""
            for i in range(level): prefix += "\t"

            #print(prefix+"self: {0}: adding word {1}|{2}".format(\
            #self.language, language,word))


            if (base_form(language)==self.language):
                #print(prefix+"MATCH: adding to self {0}: {1}".format(self.language, word))
                
                #print("#\t\t\tadding {0}, lang: {1} first word: {2}".format(word,language,first_word))
                if first_word:
                    self.first_word = True

                if self.word == "":
                    self.word = word

                #print("adding")

            elif (len(self.children) > 0):
                #print(prefix+"MISMATCH: l={0}|self={1}".format(\
                #language, self.language))
                for x in self.children:
                    x.add_word(language, word, level+1,tree_type=tree_type,first_word=first_word)
    
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

    #split item into origin and etymology
    etymology_start = full_item.find("Etymology: ")

    origin = full_item[8:etymology_start]
    item = full_item[etymology_start + 11:]

    #determine if word is inherited or borrowed

    this_tree_type = ""
    if origin.find("inherited") > -1:
        this_tree_type = "inherited"
    elif origin.find("borrowing") > -1:
        this_tree_type = "borrowing"

    print("{0} {1}".format(origin.find("inherited"),origin.find("borrowing")))
    
    print("Origin: V\n"+ origin +"\netymology: V\n"+item+"-----\n"+"tree_type: "+this_tree_type)

    ie_tree = Tree("Proto-Indo-European",coords=[49.4, 31.2], tree_type="inherited")
    ie_tree.add_child("Proto-Germanic", "Proto-Indo-European")

    ie_tree.add_child("Old Frisian", "Proto-Germanic")
    ie_tree.add_child("West Frisian", "Old Frisian")
    ie_tree.add_child("Old Dutch", "Proto-Germanic")
    ie_tree.add_child("Middle Dutch", "Old Dutch")
    ie_tree.add_child("Dutch", "Middle Dutch")
    ie_tree.add_child("Old Saxon", "Proto-Germanic")
    ie_tree.add_child("Middle Low German", "Old Saxon")
    ie_tree.add_child("Old High German","Proto-Germanic")
    ie_tree.add_child("Middle High German", "Old High German")
    ie_tree.add_child("German", "Middle High German")

    ie_tree.add_child("Old Norse", "Proto-Germanic")
    ie_tree.add_child("Old Icelandic","Old Norse")
    ie_tree.add_child("Old Norn", "Old Norse")
    ie_tree.add_child("Old Swedish", "Old Norse")
    ie_tree.add_child("Swedish", "Old Swedish")
    ie_tree.add_child("Old Danish", "Old Norse")
    ie_tree.add_child("Danish", "Old Danish")

    ie_tree.add_child("Gothic", "Proto-Germanic")

    ie_tree.add_child("Proto-Indo-Iranian", "Proto-Indo-European")
    ie_tree.add_child("Sanskrit", "Proto-Indo-Iranian")
    ie_tree.add_child("Old Avestan", "Proto-Indo-Iranian")
    ie_tree.add_child("Younger Avestan", "Proto-Indo-Iranian")

    ie_tree.add_child("Ancient Greek", "Proto-Indo-European")

    ie_tree.add_child("Latin", "Proto-Indo-European")
    ie_tree.add_child("Old French","Latin")
    ie_tree.add_child("Middle French","Old French")
    ie_tree.add_child("French","Middle French")
    ie_tree.add_child("Anglo-Norman","Old French")
    ie_tree.add_child("Old Occitan","classical Latin")
    ie_tree.add_child("Occitan","Old Occitan")
    ie_tree.add_child("Catalan","Latin")
    ie_tree.add_child("Spanish","Latin")
    ie_tree.add_child("Portuguese","Latin")
    ie_tree.add_child("Italian","Latin")

    ie_tree.add_child("Oscan", "Proto-Indo-European")

    ie_tree.add_child("Proto-Celtic", "Proto-Indo-European")
    ie_tree.add_child("Gaulish","Proto-Celtic")
    ie_tree.add_child("Early Irish","Proto-Celtic")
    ie_tree.add_child("Irish","Early Irish")
    ie_tree.add_child("Welsh","Proto-Celtic")

    ie_tree.add_child("Eastern Armenian","Proto-Indo-European")

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

        current_language = base_form(current_language.strip())
        current_words = current_words.strip()
        
        if len(current_words) > 0 and current_words[-1] == ",": current_words = current_words[:-1]

        #fix nordic languages


        #print("current_language, current_words = " + current_language + " | " + current_words)
        language_words_pairs.append([current_language,current_words])

    language_words_pairs = [[x.strip(),y.strip()] for [x,y] in language_words_pairs]
    language_words_pairs = [[x,y] for [x,y] in language_words_pairs if x != "" and y != ""]

    print(str(language_words_pairs))

    #add words to language tree

    first_word = True
    for [language_name, words] in language_words_pairs:
        #print("-----\nadding to tree {0}, {1}, {2}\n-----".format(language_name, words,first_word))
        f = first_word
        ie_tree.add_word(language_name, words, first_word=f)

        #add english under the most recent source language
        if f and this_tree_type == "borrowing":
                ie_tree.remove_child("English")
                ie_tree.add_child("English", language_name)
                ie_tree.add_word("English", chosen_word, first_word = False)

        first_word = False

    print ("\n#####################################\n")

    ie_tree.print_tree(force_show=False)

    #displaying map

    lang_names = (x[0] for x  in language_words_pairs)
    lang_words = (x[1] for x  in language_words_pairs)

    print("~~~~~")
    for x in lang_names:
        print(str(x), end=", ")

    print("\n~~~~~\n")

    for x in lang_words:
        print(str(x), end=", ")

    print("\n~~~~~\n")

    coordinates = map(lingtypology.glottolog.get_coordinates, lang_names)

    m = lingtypology.LingMap(lang_names)

    # for coordinate_pair in coordinates:
    #     folium.Marker([coordinate_pair[0], coordinate_pair[1]],
    #           popup=folium.Popup('test popup',
    #                              show=True, sticky=True)).add_to(m)

    m.add_popups(lang_words)
    m.create_map()
    m.save("language_tree.html")

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