import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_model = dict()

    linked_pages = corpus[page]

    next_page_count = len(linked_pages)
    total_page_count = len(corpus)

    if next_page_count == 0:
        for page in corpus:
            trans_model[page] = 1/total_page_count
        return trans_model

    for page in corpus:
        if page in linked_pages:
            trans_model[page] = damping_factor*(1/next_page_count) + (1-damping_factor)*(1/total_page_count)
        else:
            trans_model[page] = (1-damping_factor)*(1/total_page_count)

    return trans_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()

    for page in corpus:
        page_rank[page] = 0

    curr_page = random.choice(list(corpus.keys()))

    page_rank[curr_page] += 1

    for i in range(n-1):
        model = transition_model(corpus, curr_page, damping_factor)
        curr_page = generate_sample(model)
        page_rank[curr_page] += 1

    for page in page_rank:
        page_rank[page] /= n

    return page_rank


def generate_sample(model):

    randomNumber = random.random()

    for page in model:
        if randomNumber <= model[page]:
            return page
        randomNumber -= model[page]

    return None

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    page_source = dict()

    total_page_count = len(corpus)

    for page in corpus:
        page_rank[page] = 1/total_page_count
        page_source[page] = set()
        page_link = corpus[page]
        if len(page_link) == 0:
            for keys in corpus.keys():
                page_link.add(keys)
            corpus[page] = page_link


    for page in corpus:
        linked_pages = corpus[page]

        for p in linked_pages:
            if p in page_source.keys():
                temp = page_source.get(p)
                temp.add(page)
                page_source[p] = temp


    while True:

        max_change = 0
        for page in page_rank:

            linked_pages = page_source[page]
            val = 0

            for p in linked_pages:
                links = len(corpus[p])
                val += page_rank[p]/links

            new_rank = ((1-damping_factor)/total_page_count) + (damping_factor * val)

            max_change = max(max_change, abs(page_rank[page] - new_rank))
            page_rank[page] = new_rank

        if max_change <= 0.001:
            return page_rank



if __name__ == "__main__":
    main()
