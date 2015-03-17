__author__ = 'erich_000'
import itertools

global score_dict
global wwf_dict
global user_rack
score_dict = {}
wwf_dict = {}


# read letter_point values - returns dictionary
def get_values():
    global score_dict
    fid = open('letter_point_values.txt')
    letter_points = []
    for line in fid:
        line = line.strip()
        letter_points.append(line)
    # make dictionary from list letter_points
    # step 1: make letter score pairs into duples
    letter_points_duples = []
    for i in letter_points:
        blank_index = i.find(' ')
        tile = i[0:blank_index]
        tile = tile.lower()
        tile_value = i[blank_index + 1:len(i)]
        current_duple = (tile, int(tile_value))
        letter_points_duples.append(current_duple)
    score_dict = dict(letter_points_duples)


# get user input
def user_input():
    # ask user for letters on rack
    global user_rack
    rack = raw_input("Please enter your letters separated by single spaces")
    user_rack = rack[:]
    # make lower
    rack = str(rack)
    rack = rack.lower()
    # print "rack = ", rack
    rack = rack.split(' ')
    #print "rack split", rack
    # parse input into list
    rack_tiles = []
    j = 0
    while j < len(rack):
        rack_tiles.append(rack[j])
        j += 1
    #print "rack divided into individual tiles (list): ", rack_tiles
    good_size = len(rack_tiles) <= 7
    if good_size:
        return rack_tiles
    else:
        print "rack too large!"
        return -1


# calculate the score of a given string
# return int
# 'word', dict[tile_values]
def calc_score(word):
    global score_dict
    # argument [word] = string
    # calculate score for word
    word_tile_values = []
    for i in word:
        word_tile_values.append(score_dict[i])
    return sum(word_tile_values)


# get WWF word list
# create dictionary with words and their scores
# return dictionary
def get_wff_dictionary():
    global wwf_dict
    fid = open('WWF_all_words.txt')
    wordlist = []
    for line in fid:
        line = line.strip()
        # print "adding word %s to dictionary" % line
        wordlist.append(line)
    # make duples for wordlist and word scores
    wordlist_scores = []
    print "setting scores..."
    for i in wordlist:
        # use calc_score
        current_word_score = calc_score(i)
        current_duple = (str(i), current_word_score)
        # print "appending current_duple(", i, ", ", current_word_score, ")"
        wordlist_scores.append(current_duple)
    wwf_dict = dict(wordlist_scores)


# make all possible racks for a rack containing a blank
# called in get_letter_perms
def make_blank_racks(rack):
    all_racks = []
    # check how many blanks, add tiles once or twice
    blank_count = rack.count('blank')
    rack.remove('blank')
    curr_char_code = 97
    #print "all_racks before loop: ", all_racks
    while curr_char_code < 123:
        curr_char = chr(curr_char_code)
        curr_rack = rack[:]
        curr_rack.append(curr_char)
        all_racks.append(curr_rack)
        curr_char_code += 1
    # return all_racks as list of lists of separate characters
    # print "all racks at end of make_blank_racks"
    if 'blank' in all_racks[0]:
        all_racks_copy = all_racks[:]
        all_racks = []
        print "recursing..."
        for i in all_racks_copy:
            rack_list = make_blank_racks(i)
            for r in rack_list:
                all_racks.append(r)
        return all_racks
    else:
        return all_racks


# use list of tiles to find all permutations in rack
# return list of permutations as strings
# called in find_best_word(rack)
def get_letter_perms(rack):
    print "getting letter permutations of all sizes..."
    # convert rack to string
    # if no 'blank', no problem
    # if blank, make list of racks to feed to itertools.permutations
    all_racks = []
    all_perms = []
    # see if rack has blank. if so, make list of all possible racks.
    contain_blank = 'blank' in rack
    if contain_blank:
        # make list of all possible racks (replacing 'blank' with every letter)
        all_racks = make_blank_racks(rack)
    else:
        # append only rack to first index of all_racks[]
        # print "string has no blanks"
        all_racks.append(rack)
    # if there are no blanks, all_racks contains one list (one rack)
    all_perms_strings = []
    for j in all_racks:
        # change first rack into string
        current_rack = ''.join(j)
        # find permutations of that string and all sub-strings
        rack_len = len(j)
        all_lens = []
        while rack_len > 0:
            all_lens.append(rack_len)
            rack_len -= 1
        #print "all_lens ==", all_lens
        for l in all_lens:
            perms = itertools.permutations(current_rack, l)
            # loop through perms and append to all_perms
            for p in perms:
                all_perms.append(p)
    for j in all_perms:
        perm_as_string = ''.join(j)
        all_perms_strings.append(perm_as_string)
    # print "all_racks: ", all_racks
    # print "all_perms: ", all_perms
    #print "all_perms_strings: ", all_perms_strings

    # get all n - 1, n - 2 ... n - (n-1) letter combinations

    return all_perms_strings


# ADD TICK-TOCK PREDICTION HERE
# ADD SUPPORT FOR TIE-SCORE TOP WORD
# find highest-scoring word output
def find_best_word(rack):
    global wwf_dict
    letter_perms = get_letter_perms(rack)
    # high_word is list.  probably one word, but can have a tie
    high_word = []
    high_score = 0
    print "number of letter combinations to search: %i" % len(letter_perms)
    for w in letter_perms:
        #print "searching word " + w + " in dictionary"
        is_word = w in wwf_dict.keys()  # check if word is in dictionary
        if is_word:
            score = wwf_dict[w]
            if len(w) == 7: score = score + 35
            if score > high_score:
                high_word = [w]
                high_score = score
                print high_word, "new high score :", high_score
            elif score == high_score:
                high_word.append(w)
                high_score = score
                print high_word, "new high score :", high_score
    if high_score > 0:
        """
        print "\nbest word: " + high_word
        print "score: %i" % high_score
        """
        return high_word
    else:
        print "high_score == 0; no word found"
        return high_score

    # get score for each word in dictionary, store highest scoring word


def output(best_word):
    # best_word will be list, can have more than one item (best word)
    print "\n-=-=-=-=-\noutput:"
    global wwf_dict
    global user_rack  # this is initial rack
    print "initial user rack: ", user_rack
    best_word_counter = 1
    for w in best_word:
        score = wwf_dict[w]
        # format string to print as separate tiles
        best_tiles = []
        i = 0
        while i < len(w):
            best_tiles.append(w[i])
            best_tiles.append(' ')
            i += 1
        # separately present leftover tiles
        best_tiles_separated = ''.join(w)
        if len(best_word) > 1:
            print "best word", best_word_counter, ':', best_tiles_separated
        else:
            print "best word:", best_tiles_separated
        best_word_counter += 1
        print "score:", score
    # YOU MUST RE-DO LEFTOVERS
    print "RE-DO LEFTOVERS"


def main():
    # get dictionary of tile point values
    global score_dict
    global wwf_dict
    print "reading in tile values..."
    get_values()
    # print 'score dictionary:', score_dict
    print "reading in Words W/ Friends wordlist..."
    get_wff_dictionary()
    rack = -1
    while rack == -1:
        # user_input() returns -1 if rack is too large
        rack = user_input()
    best_word = find_best_word(rack)
    output(best_word)


main()
