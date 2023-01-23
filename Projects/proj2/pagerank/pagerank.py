import copy
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


# >>> crawl('./corpus0')
# {
# '1.html': {'2.html'},
# '2.html': {'3.html', '1.html'},
# '3.html': {'4.html', '2.html'},
# '4.html': {'2.html'}
# }


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus 格式如下 corpus = {'1.html': {'2.html'}, '2.html': {'3.html', '1.html'}, '3.html': {'4.html', '2.html'},
    # '4.html': {'2.html'}}

    result = {}
    # 1.if the page has no out_to links, i.e. the page is a lonely island
    linkedPages = corpus[page]
    if len(linkedPages) == 0:
        prob = 1 / len(corpus)
        for corpus_page in corpus:
            result[corpus_page] = prob

        return result
    # 2.if the page has linked pages, there are two cases:
    # the linked ones / the lonely ones
    prob_1 = (1 - damping_factor) / len(corpus)
    prob_2 = damping_factor / len(linkedPages)
    for corpus_page in corpus:
        if corpus_page in linkedPages:
            result[corpus_page] = prob_1 + prob_2
        else:
            result[corpus_page] = prob_1

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    next_page = random.choice(list(corpus))
    for i in range(n):
        model = transition_model(corpus,next_page,damping_factor)
        next_page = random.choices(list(model), weights = model.values(),k=1).pop()
        if next_page in pagerank:
            pagerank[next_page]+=1
        else:
            pagerank[next_page] = 1

    for item in pagerank:
        pagerank[item] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for page in list(corpus):
        pagerank[page] = 1 / len(corpus)

    # result 是否收敛
    converged = False
    while not converged:
        pagerank_copy = copy.deepcopy(pagerank)
        pagerank_diff = {}
        for page in list(corpus):
            pr = 0

            for page_i, pages in corpus.items():
                if page in pages:
                    pr += pagerank[page_i] / len(pages)
                elif len(pages) == 0:
                    pr += 1 / len(corpus)

            pagerank[page] = (1 - damping_factor) / len(corpus) + (damping_factor * pr)
            pagerank_diff[page] = abs(pagerank[page] - pagerank_copy[page])
            # print(pagerank_diff)

        converged = True
        for page in pagerank_diff:
            if pagerank_diff[page] > 0.001:
                converged = False

    # normalize:
    sum_pagerank = 0
    for k in pagerank:
        sum_pagerank += pagerank[k]

    if sum_pagerank == 1:
        return pagerank
    else:
        for k in pagerank:
            pagerank[k] = pagerank[k] / sum_pagerank
        return pagerank



if __name__ == "__main__":
    main()
