#!/bin/bash

# # #
# USAGE: ThisScript test.1.txt
#
# USAGE: ThisScript input.txt
# USAGE: ThisScript
#

INFILE=${1:-input.txt}

find_common_char() {
    # assuming each input line contains space separated words,
    # find characters that are common to all words of the line
    # echo "abc cde" | find_common_char
    # => c
    while IFS= read line; do
        # compute number of words in the line
        num_words=$(echo $line | tr ' ' '\n' | wc -l)

        # deduplicate characters in each word
        echo $line | tr " " "\n" |
        while IFS= read word; do
            # keep only one occurrence of a character
            echo $word | fold -w1 | sort | uniq
        done |
        # find character(s) that is/are common to all words
        sort | uniq -c |          # count characters individually
        grep -e " $num_words " |  # select those that occur num_word times
        grep -o '[^ ]*$'          # get the character selected
    done
}

chunk_in_two() {
    # inserts a space character at the position at the middle
    # of string received as stdin
    while IFS= read line; do
        half=$((${#line}/2))
        echo $line | fold -w $half | paste -sd' '
    done
}

get_char_priority() {
    # map a character to its priority
    # assume every input line is a single character
    while IFS= read char; do
        codep=$(printf "%d" "'$char")
        offset=96
        if $(echo $char | grep -qw '[A-Z]'); then
            offset=38
        fi
        echo $((codep - offset))
    done
}

solve_1() {
    cat "$@" |
    chunk_in_two |
    find_common_char |
    get_char_priority |
    paste -sd+ |
    bc
}

solve_2() {
    cat $@ |
    xargs -L 3 |
    find_common_char |
    get_char_priority |
    paste -sd+ |
    bc
}

score1=$(solve_1 "$INFILE")
echo "Part 1: Total is $score1"

score2=$(solve_2 "$INFILE")
echo "Part 2: Total is $score2"
