#!/usr/env/python3

import re
import argparse
from urllib.parse import unquote
from collections import Counter

configs = {
    "path_regex": r"/+([\w\-_]+)/*",
    "param_name_regex": r"[?]+|[&]*([\w\-_]+)=",
    "param_value_regex": r"=+([\w\-_]+)"
}


def get_file_content(args):
    """Reads contents of file into variable and returns it."""
    with open(args.filepath, "r") as file:
        content = file.read()
        file.close()

    return content


def extract_regex(urls, config="path_regex", all=False):
    """Extracts items from URL file using the given regex pattern and returns the matches sorted."""    # noqa: E501
    matches = []

    if all:
        for regex in (configs["path_regex"],
                      configs["param_name_regex"],
                      configs["param_value_regex"]):
            pattern = regex
            matches.append(re.findall(pattern, urls))
    else:
        if config == "param_name_regex":
            pattern = configs["param_name_regex"]
            matches.append(re.findall(pattern, urls))
        elif config == "param_value_regex":
            pattern = configs["param_value_regex"]
            matches.append(re.findall(pattern, urls))
        else:
            pattern = configs["path_regex"]
            matches.append(re.findall(pattern, urls))

    matches.sort()

    return matches


def word_counter(matches):
    """Returns a dictionary of given terms with its corresponding number of occurences."""     # noqa: E501
    words = flatten_list(matches)
    words = list(filter(None, words))
    counter = Counter(words)
    counts = dict(zip(counter.keys(), counter.values()))

    return counts


def flatten_list(list):
    """Creates one flat list out of given list of embedded lists,  and returns it."""  # noqa: E501
    return [item for sublist in list for item in sublist]


def create_wordlist(matches):
    """Creates a sorted and unique wordlist from the given regex matches and returns the wordlist."""   # noqa: E501
    words = flatten_list(matches)
    output = []

    for word in words:
        if word in output:
            continue
        else:
            output.append(word)

    output.sort()
    wordlist = remove_empty_items(output)

    return wordlist


def write_file_content(args, content, count=False):
    """Writes given contents into file."""
    with open(args.outfile, "w") as file:
        if count:
            for k, v in content.items():
                file.write("{0} {1}\n".format(v, k))
        else:
            for line in content:
                file.write(line + "\n")
        file.close()


def remove_empty_items(wordlist):
    """Will remove any empty lines from the wordlist and return the wordlist."""    # noqa: E501
    emptied = list(filter(None, wordlist))

    return emptied


def print_wordlist(wordlist, count=False):
    """Prints out each word in the wordlist."""
    if count:
        for k, v in wordlist.items():
            print("{0}   {1}".format(v, k))
    else:
        for word in wordlist:
            print(word)


def driver(args, flag, decode, out, count):
    """Helper function to main"""
    urls = get_file_content(args)

    if decode:
        urls = unquote(urls)
    else:
        pass

    if flag == "v":
        matches = extract_regex(urls, config="param_value_regex", all=False)
        wordlist = create_wordlist(matches)
    elif flag == "p":
        matches = extract_regex(urls, config="param_name_regex", all=False)
        wordlist = create_wordlist(matches)
    elif flag == "A":
        matches = extract_regex(urls, config=None, all=True)
        wordlist = create_wordlist(matches)
    else:
        matches = extract_regex(urls, config="path_regex", all=False)
        wordlist = create_wordlist(matches)

    if count:
        wordlist = word_counter(matches)
    else:
        pass

    if out:
        write_file_content(args, wordlist, count)
    else:
        print_wordlist(wordlist, count)


def main():
    """Driving code of the script."""
    parser = argparse.ArgumentParser(
            prog="w-extract",
            description="w-extract creates custom wordlists by extracting \
                        pathnames (default behavior), parameter names, or \
                        parameter values from URLs to aid in web discovery \
                        and exploitation efforts.",
            epilog="Written by Steven Howe, v1.0")

    parser.add_argument("filepath",
                        help="filepath of file containing list of URLs")

    parser.add_argument("-p", "--parameters",
                        help="extracts found parameter names into a wordlist",
                        action="store_true")

    parser.add_argument("-v", "--values",
                        help="extracts found parameter values into a wordlist",
                        action="store_true")

    parser.add_argument("-A", "--all",
                        help="extracts pathnames, parameter names, and values \
                            into a wordlist",
                        action="store_true")

    parser.add_argument("-c", "--count",
                        help="counts occurences of extracted items",
                        action="store_true")

    parser.add_argument("-u", "--urldecode",
                        help="URL decodes values",
                        action="store_true")

    parser.add_argument("-o", "--outfile",
                        help="filepath of file which output will be written \
                            to")
    args = parser.parse_args()

    if args.outfile:
        out = True
    else:
        out = False

    if args.count:
        count = True
    else:
        count = False

    if args.urldecode:
        decode = True
    else:
        decode = False

    if args.parameters:
        driver(args, "p", decode, out, count)
    elif args.values:
        driver(args, "v", decode, out, count)
    elif args.all:
        driver(args, "A", decode, out, count)
    else:
        driver(args, "", decode, out, count)


if __name__ == "__main__":
    main()
