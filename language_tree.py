import re
from entries import entries
import lingtypology
import folium
import numbers

languages_list_path = "C:\\Users\\david\\TCD\\4th year\\final year project\\languages_list.txt"
languages_list_file = open(languages_list_path, encoding='utf-8')
languages_list = languages_list_file.read().split('\n')

#print("-----\nfather_etymology = " + str(father_etymology) + "\n-----")

lang_dict = {
    "Early Runic" : "Proto-Norse",
    "Early Scandinavian": "Proto-Norse",
    "Early Scandinavian (runic: Sweden)" : "Proto-Norse",
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
    "Armenian": "Eastern Armenian",
    "West Frisian": "Western Frisian",
    "Old High German": "Old High German (ca. 750-1050)",
    "classical Latin": "Latin",
    "Gaulish": "Transalpine Gaulish",
    "Tocharian A": "Tokharian A",
    "Tocharian B": "Tokharian B",
    "Indo-European": "Proto-Indo-European",
}

extra_coords = {
    "Old Dutch": (51.8,4.8),
    "Middle Dutch": (51.7,5.0),
    "Middle Low German": (52.4,10.1),
    "Middle High German": (51.6,10.7),
    "Proto-Norse": (54.2,10.3),
    "Old Norse": (55.2,10.3),
    "Old Icelandic": (64.0,-16.5),
    "Old Norn": (59.3,-2.4),
    "Old Swedish": (58.4,15.4),
    "Old Danish": (55.4,9.4),
    "Old French": (48.7, 1.0),
    "Middle French": (48.3, 1.5),
    "Oscan": (41.0, 15.7),

    "Proto-Indo-European": (49.4, 34.2),
    "Proto-Germanic": (54.3, 9.5),
    "Proto-Indo-Iranian": (53.0, 64.8),
    "Proto-Celtic": (47.6, 13.7),
    "Mycenaean Greek": (37.5,23.1),
    "Proto-Balto-Slavic": (54.3,26.9),
    "Old Occitan": (45.8,2.7),
    "Proto-Baltic": (55.5, 26.4),
    "Proto-Slavic" : (50.6, 25.8),
    "Anglo-Norman": (49.0, -0.2),
    "Old Church Slavonic": (42.3, 22.4),
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
        #self.has_descendant_words = 0
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
        
            print(self.language + "(" + str(self.has_descendant_words()) + ")",end="")# + " " + self.word)
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
                
    def get_language(self, language_name, current_level=0):
        for i in range(current_level): print("\t", end="")
        #print("self name = {0}, language_name = {1}".format(self.language, language_name))
        
        #base case

        if len(self.children) == 0:
            if self.language == language_name:
                return self
            else:
                return 0
        
        #recursive case

        else:
            if self.language == language_name:
                return self
            else:
                result = 0
                current_result = 0

                for child in self.get_children():
                    current_result = child.get_language(language_name, current_level+1)

                    if current_result != 0:
                        result = current_result
                
                return result

        # current_result = self

        # if self.language != language_name:
        #     for i in range(current_level): print("\t", end="")
        #     print("returning self")
        # else:
        #     result_in_children = False

        #     for child in self.children:
        #         for i in range(current_level): print("\t", end="")
        #         print("going through children")

        #         temp_result = child.get_language(language_name, current_level+1)
        #     return result

    def has_descendant_words(self):

        #base case

        if len(self.get_children()) == 0:
            return self.word != ""
        
        #recursive case

        else:
            if self.word != "":
                return True
            else:
                result = False
                current_result = False

                for child in self.get_children():
                    current_result = child.has_descendant_words()

                    if current_result == True:
                        result = current_result

                return result

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
    ie_tree.add_child("Western Frisian", "Old Frisian")
    ie_tree.add_child("Old Dutch", "Proto-Germanic")
    ie_tree.add_child("Middle Dutch", "Old Dutch")
    ie_tree.add_child("Dutch", "Middle Dutch")
    ie_tree.add_child("Old Saxon", "Proto-Germanic")
    ie_tree.add_child("Middle Low German", "Old Saxon")
    ie_tree.add_child("Old High German","Proto-Germanic")
    ie_tree.add_child("Middle High German", "Old High German")
    ie_tree.add_child("German", "Middle High German")

    ie_tree.add_child("Proto-Norse", "Proto-Germanic")
    ie_tree.add_child("Old Norse", "Proto-Norse")
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
    ie_tree.add_child("Old Occitan","Latin")
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


        #print("current_language, current_words = " + current_language + " | " + current_words)
        language_already_in_pairs = False
        for [x,y] in language_words_pairs:
            if x == current_language:
                language_already_in_pairs = True
        if not language_already_in_pairs:
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

    ie_tree.print_tree(force_show=True)

    #testing get_language()

    french = ie_tree.get_language("French")
    french_parent = ie_tree.get_language(french.parent_language)
    print("French = {0}, French.parent = {1}".format(french.language, french_parent.language))

    #adding "hidden" parent languages to languages that have words

    language_queue = [ie_tree]

    while len(language_queue) > 0:
        for x in language_queue:
            print("{0}, {1}".format(x.language, x.word),end="\t")
        print("\n")
        if language_queue[0].has_descendant_words():
            if language_queue[0].word == "":
                print("adding {0}".format(language_queue[0].language))
                language_words_pairs.append((base_form(language_queue[0].language), "-"))
            
            for child in language_queue[0].get_children():
                print("appending {0}".format(child.language))
                language_queue.append(child)

        language_queue.pop(0)
        

    #displaying map

    lang_names = list((base_form(x[0]) for x  in language_words_pairs))
    lang_words = list((x[1] for x  in language_words_pairs))

    print("~~~~~")
    for x in lang_names:
        print(str(x), end=", ")

    print("\n~~~~~\n")

    for x in lang_words:
        print(str(x), end=", ")

    print("\n~~~~~\n")

    #create base folium map
    m = folium.Map((0, 0), zoom_start=2)

    coordinates = list(map(lingtypology.glottolog.get_coordinates, lang_names))
    
    #print language coordinates solely from glottolog

    for i in range(len(coordinates)):
        print("## {0} {1}".format(lang_names[i], coordinates[i]))

    #adding lines between points on map

    for first_lang_index in range(len(lang_names)):


        #print("########### L1 = {0}".format(lang_names[first_lang_index]),end="\n")
        
        if not ((coordinates[first_lang_index] is not None) and coordinates[first_lang_index][0] > -180 and \
           (coordinates[first_lang_index] is not None) and coordinates[first_lang_index][1] > -90):
            coordinates[first_lang_index] = extra_coords[lang_names[first_lang_index]]
            #add point on map

        folium.Marker((coordinates[first_lang_index][0], coordinates[first_lang_index][1]), \
                        popup=(lang_names[first_lang_index] + ": " + lang_words[first_lang_index])).add_to(m)

        for second_lang_index in range(len(lang_names)):
            #print("\tL2 = {0}".format(lang_names[second_lang_index]),end="\n")


            #    print("~~~~~ {0} = {1} ~~~~~".format(ie_tree.get_language(lang_names[first_lang_index]), lang_names[second_lang_index]))
            if ie_tree.get_language(lang_names[first_lang_index]) != 0 and \
                 ie_tree.get_language(lang_names[first_lang_index]).parent_language == lang_names[second_lang_index]:
                print("\t\tis parent")
                if (coordinates[first_lang_index] is not None) and coordinates[first_lang_index][0] > -180 and \
                    (coordinates[first_lang_index] is not None) and coordinates[first_lang_index][1] > -90 and \
                    (coordinates[second_lang_index] is not None) and coordinates[second_lang_index][0] > -180 and \
                    (coordinates[second_lang_index] is not None) and coordinates[second_lang_index][1] > -90:

                    """print("\t\t\tis right coords")
                    print("\t\t\tcoords1 = {0},{1}, coords2 = {2},{3}, li1 = {4}, li2 = {5}".format(coordinates[first_lang_index][0],\
                                                                              coordinates[first_lang_index][1],\
                                                                              coordinates[second_lang_index][0],\
                                                                              coordinates[second_lang_index][1],\
                                                                              first_lang_index, second_lang_index))"""
                    trail_coordinates = []

                    trail_coordinates.append((coordinates[first_lang_index][0], coordinates[first_lang_index][1]))
                    trail_coordinates.append((coordinates[second_lang_index][0], coordinates[second_lang_index][1]))
                        
                    print("\t\t\ttrail_coordinates is now {0}, coordinates = {1}".format(trail_coordinates, list(coordinates)))
                    folium.PolyLine(trail_coordinates, tooltip="Connections between languages").add_to(m)


    #print full list of language coordinates
 
    for i in range(len(coordinates)):
        print("## {0} {1}".format(lang_names[i], coordinates[i]))

    print("lang_names length = {0}, lang_words length = {1}".format(len(lang_names), len(lang_words)))

    m.save("language_tree.html")

    # #create lingtypology map
    # m = lingtypology.LingMap(lang_names)
    # m.add_popups(lang_words)
    
    # m.base_map = folium_map
    # m.create_map()
    # m.save("language_tree.html")

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