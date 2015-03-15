__author__ = 'erich_000'
import itertools

global score_dict
global wwf_dict
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
# return void
def user_input():
    # ask user for letters on rack
    rack = raw_input("Please enter your letters separated by single spaces")
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
def make_blank_racks(rack):
    print "'rack' input into make_blank_racks(): ", rack
    all_racks = []
    # check how many blanks, add tiles once or twice
    blank_count = rack.count('blank')
    rack.remove('blank')
    # make 26 racks ready to append to
    a = 0
    while a < 26:
        all_racks.append(rack)
        a += 1
    print "26 racks without blank: ", all_racks
    curr_char_code = 97
    # upper limit should be 123 - 101 for debugging
    while curr_char_code < 100:
        curr_char = chr(curr_char_code)
        print "appending " + curr_char + " to all_racks[%d]" % (curr_char_code - 97)
        all_racks[curr_char_code-97].append(curr_char)
        curr_char_code += 1
    # return all_racks as list of lists of separate characters
    print "all racks at end of make_blank_racks", all_racks
    return all_racks


# use list of tiles to find all permutations in rack
# return list of permutations
def permute(rack):
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
        print "string has no blanks"
        all_racks.append(rack)
    for j in all_racks:
        # change first rack into string
        current_rack = ''.join(j)
        print "current_rack: ", current_rack
        # find permutations of that string
        perms = itertools.permutations(current_rack)
        # loop through perms and append to all_perms
        for k in perms:
            all_perms.append(k)
    print "all perms before stringify loop: ", all_perms
    all_perms_strings = []
    for j in all_perms:
        perm_as_string = ''.join(j)
        all_perms_strings.append(perm_as_string)
    print "all_racks: ", all_racks
    print "all_perms: ", all_perms
    print "all_perms_strings: ", all_perms_strings
    return all_perms


# find highest-scoring word
def find_best_word(rack):
    possible_words = permute(rack)
    # compare all words for point value, return highest
    pass


def output(best_word):
    # print best scoring word plus score
    pass


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
    print "your rack = ", rack
    #all_racks = permute(rack)
    make_blank_racks(rack)
    """
    best_word = find_best_word(rack)
    output(best_word)
    """


main()
