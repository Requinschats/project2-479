import os
from pathlib import Path
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from naive_indexer import select_doc_id


def select_tokenized_document(string_document):
    return RegexpTokenizer(r'\w+').tokenize(string_document)


def select_file_content(file_name):
    return Path('reuters21578/' + file_name).read_text()


def select_nonpositional_posting_token_list():
    token_list = []
    for file_name in os.listdir("reuters21578")[:5]:
        file_content = select_file_content(file_name)
        tokenized_content = list(set(select_tokenized_document(file_content)))
        doc_id = select_doc_id(file_content)
        token_list += list(map(lambda token: (token, doc_id), tokenized_content))
        token_list = list(filter(lambda token_docId: token_docId != "UNKNOWN", token_list))
    return token_list


def select_positional_posting_token_list():
    token_list = []
    for file_name in os.listdir("reuters21578")[:5]:
        file_content = select_file_content(file_name)
        tokenized_content = select_tokenized_document(file_content)
        doc_id = select_doc_id(file_content)
        token_list += list(map(lambda token: (token, doc_id), tokenized_content))
        token_list = list(filter(lambda token_docId: token_docId != "UNKNOWN", token_list))
    return token_list


def select_token_set():
    token_set = set()
    for file_name in os.listdir("reuters21578")[:5]:
        file_content = select_file_content(file_name)
        tokenized_content = select_tokenized_document(file_content)
        for token in tokenized_content:
            token_set.add(token)
    return token_set


def select_token_list_without_numbers(token_list, is_posting):
    if is_posting:
        return list(filter(lambda token_docId: not (token_docId[0].isdigit()), token_list))
    else:
        return list(filter(lambda token: not token.isdigit(), token_list))


def select_lower_case_token_list(token_list, is_posting, is_positional):
    if is_posting:
        lower_case_token_list = list(
            map(lambda token_docId: (token_docId[0].lower(), token_docId[1]), token_list))
        return set(lower_case_token_list) if not is_positional else lower_case_token_list
    else:
        return set(map(lambda token: token.lower(), token_list))


def select_token_list_without_stop_words(token_list, is_posting):
    english_stopwords = stopwords.words("english")
    if is_posting:
        return list(filter(lambda token_docId: token_docId[0] not in english_stopwords, token_list))
    else:
        return list(filter(lambda string: string not in english_stopwords, token_list))


def select_stemmed_token_list(token_list, is_posting, is_positional):
    stemmer = PorterStemmer()
    if is_posting:
        stemmed_token_list = map(lambda token_docId: stemmer.stem(token_docId[0], token_docId[1]), token_list)
        return list(set(stemmed_token_list)) if not is_positional else list(stemmed_token_list)
    else:
        return list(map(lambda string: stemmer.stem(string), token_list))


def add_entry_global_index(global_index, token, doc_id):
    if token in global_index:
        global_index[token].append(doc_id)
    else:
        global_index[token] = [doc_id]


def output_variation(original_list, new_list):
    original_list_length = len(original_list)
    new_list_length = (len(new_list))
    print("Variation -" + str(100 - int((new_list_length / original_list_length) * 100)) + "%\n")


def output_compression_stats(token_list, category, is_posting, is_positional=False):
    print("\n -- " + category + " -- ")
    print("Unfiltered: " + str(len(token_list)))

    token_list_without_numbers = select_token_list_without_numbers(token_list, is_posting)
    print("No numbers: " + str(len(token_list_without_numbers)))
    output_variation(token_list, token_list_without_numbers)

    token_list_lower_case = select_lower_case_token_list(token_list_without_numbers, is_posting,
                                                         is_positional)
    print("Case folding: " + str(len(token_list_lower_case)))
    output_variation(token_list_without_numbers, token_list_lower_case)

    token_list_without_stop_words = select_token_list_without_stop_words(token_list_lower_case,
                                                                         is_posting)
    print("Without stop words: " + str(len(token_list_without_stop_words)))
    output_variation(token_list_lower_case, token_list_without_stop_words)

    token_list_stemmed = select_stemmed_token_list(token_list_without_stop_words, is_posting, is_positional)
    print("Stemming: " + str(len(token_list_stemmed)))
    output_variation(token_list_without_stop_words, token_list_stemmed)


def output_distinct_term_stats():
    token_list = select_token_set()
    output_compression_stats(token_list, "Distinct terms", False)


def output_non_positional_stats():
    token_list = select_nonpositional_posting_token_list()
    output_compression_stats(token_list, "Non positional postings", True)


def output_positional_posting_stats():
    token_list = select_positional_posting_token_list()
    output_compression_stats(token_list, "Positional postings", True, True)


output_distinct_term_stats()
output_non_positional_stats()
output_positional_posting_stats()
