import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    filecontents = dict()

    for r, d, f in os.walk(directory):
        for file in f:
            curr_file = os.path.join(directory, file)
            with open(curr_file, 'r', encoding="utf8") as myfile:
                data = myfile.read()
            filecontents[file] = data

    return filecontents

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document)
    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if w not in nltk.corpus.stopwords.words('english')]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_dict = dict()

    for doc in documents:
        contents = documents[doc]
        visited = []
        for word in contents:
            if word in word_dict:
                if word not in visited:
                    word_dict[word] += 1
                    visited.append(word)
            else:
                word_dict[word] = 1
                visited.append(word)

    total_doc = len(documents.keys())

    for word in word_dict:
        val = word_dict[word]
        word_dict[word] = math.log(total_doc/val)

    return word_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()

    for file in files:
        tfidfs[file] = 0
        for word in query:
            tf = sum(word == w for w in files[file])

            tfidfs[file] += tf * idfs[word]

    tfidfs = {k: v for k, v in sorted(tfidfs.items(), key=lambda item: item[1], reverse=True)}

    ans = list(tfidfs)

    return ans[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_dict = dict()

    for sentence in sentences:
        qtd = 0
        idf = 0
        for word in query:
            if word in sentences[sentence]:
                idf += idfs[word]
        for word in sentences[sentence]:
            if word in query:
                qtd += 1

        sentence_dict[sentence] = (idf, qtd/len(sentences[sentence]))

    sentence_dict = {k: v for k, v in
                     sorted(sentence_dict.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)}

    ans = list(sentence_dict)

    return ans[:n]

if __name__ == "__main__":
    main()
