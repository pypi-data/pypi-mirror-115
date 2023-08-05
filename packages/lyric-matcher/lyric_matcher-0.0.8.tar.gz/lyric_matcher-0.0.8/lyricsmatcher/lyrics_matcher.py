# Python Version == 3.8.10
# coding=utf-8
# This is a sample Python script.
# Authors: Hanhaodi Zhang, Zhaoyng Bu

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.



import sys


def lyrics2sections(path):
    """

    Args:
        path: path of txt file

    Returns:
        sections: list of all sections

    """

    f = open(path)
    lines = f.readlines()
    section = ""
    sections = []
    for line in lines:
        if line.startswith('['):
            continue
        if line == "\n" and section != "":
            section = section.lower()
            sections.append(section)
            section = ""
        else:
            section += line
    sections.append(section.lower())
    f.close()

    return sections


def format_list(list):

    """

    Args:
        list: list

    Returns:
        format_list: list wo/ space

    """

    format_list = []
    for s in list:
        format_s = ''.join(e for e in s if e.isalnum())
        format_list.append(format_s)

    return format_list


def lyrics2sentences(path):

    """

    Args:
        path: path of txt file

    Returns:
        times: list of timestamps
        sentences: list of all sentences

    """

    f = open(path)
    lines = f.readlines()
    times = []
    sentences = []
    for line in lines:
        line = line.strip()
        if line.endswith(']'):
            continue
        line = line.split(']')
        times.append(line[0] + ']')
        sentences.append(line[1].lower())
    return times, sentences


def find_number_in_section(sentence, section):

    """

    Args:
        sentence: str
        section: str

    Returns:
        count: # of same str showed in previous sections

    """

    length_a = len(section)
    length_b = len(sentence)
    count = 0
    i = 0
    for j in range(length_a):
        if section[j] == sentence[i]:  # until find 'str' in sections
            if i == length_b - 1:  # i = len(sentence) ensure we get 'str' instead of other str
                count = count + 1  # if so, count +1
                i = 0
            else:
                i += 1  # if not match, i+1
                if j < (length_a - 1) and section[j + 1] != sentence[
                    i]:  # if j < len(section) and second str in sentence could not match next str in section
                    i = 0  # reset i = 0
        else:
            continue
    return count


def find_time(sentences, section_id, sections, time, short_length):

    """

    Args:
        sentences: sentences list
        section_id: index of section
        sections: sections list
        time: timestamp list
        short_length: int

    Returns:
        time[time_index]: timestamp of sections

    """

    if section_id == 0:
        return time[0]
    cu_section = sections[section_id]
    first_se_sentence = cu_section[:short_length]

    number = 0
    for i in range(section_id):
        n_i = find_number_in_section(first_se_sentence, sections[i])
        number += n_i  # calculate # of key sentences in former sections

    time_n = 0
    time_index = 0
    for i in range(len(sentences)):

        time_i = find_number_in_section(first_se_sentence, sentences[i])
        time_n += time_i  # calculate # of key sentences in former sentences
        if time_n == number + 1:
            time_index = i - 1
    return time[time_index]

    print('no match check the function')


def find_len(sentences):

    """

    Args:
        sentences: list of sentences

    Returns:
        shortest_length: shortest length of sentences

    """

    shortest_length = 10000
    for sentence in sentences:
        if len(sentence) < shortest_length:
            shortest_length = len(sentence)
    return shortest_length


def lyrics_matcher(lyric_section_path,lyric_time_path):
    sections = lyrics2sections(lyric_section_path)
    times, sentences = lyrics2sentences(lyric_time_path)
    format_section = format_list(sections)
    format_sentence = format_list(sentences)

    l = find_len(format_sentence)

    t = []
    for i in range(len(format_section)):
        t_i = find_time(format_sentence, i, format_section, times, l)
        t.append(t_i)

    return t




