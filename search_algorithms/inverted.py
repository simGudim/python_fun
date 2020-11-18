import re
import os


class Indexer(object):
    def __init__(self, docs):
        self.docs = docs

    def __repr__(self):
        return self.docs

    @classmethod
    def from_directory(cls, directory = None, basedir = True):
        docs = list()
        if basedir:
            directory = os.path.abspath(os.path.dirname(__file__))
            for file in os.listdir(directory):
                if file.endswith("txt"):
                    with open('doc1.txt', 'r') as f:
                        doc = f.read()
                        for i in doc.split('\n\n'):
                            i = re.sub(r'[^a-zA-Z0-9]+', " ", i)
                            docs.append(i)
        else:
            for file in os.listdir(directory):
                if file.endswith("txt"):
                    with open('doc1.txt', 'r') as f:
                        doc = f.read()
                        for i in doc.split('\n\n'):
                            i = re.sub(r'[^a-zA-Z0-9]+', " ", i)
                            docs.append(i)

        return cls(docs)

    @property
    def index(self):
        index = {}
        for idx, doc in enumerate(self.docs):
            doc = re.sub(r'[^a-zA-Z0-9]+', " ", doc)
            for i in doc.split():
                if i in index:
                    index[i.lower()].add(idx)
                else:
                    index[i.lower()] = {idx}

        return index

    @property
    def unique_terms(self):
        unique_terms = {term.lower() for doc in self.docs for term in doc.split()}
        return unique_terms

    def or_postings(self, word1, word2):
        if word1 in self.index.keys() and word2 in self.index.keyx():
            post1 = list(self.index[word1])
            post2 = list(self.index[word2])
            p1 = 0
            p2 = 0
            result = list()
            while p1 < len(post1) and p2 < len(post2):
                ## if the first values in reference to the pointer are equal, append one of them to the list
                if post1[p1] == post2[p2]:
                    result.append(post1[p1])
                    p1 += 1
                    p2 += 1
                # if the second word is in earlier document append that doc to the results
                elif post1[p1] > post2[p2]:
                    result.append(post2[p2])
                    p2 += 1
                ## if only the first word in earlier document than append that
                else:
                    result.append(post1[p1])
                    p1 += 1
            while p1 < len(post1):
                result.append(post1[p1])
                p1 += 1
            while p2 < len(post2):
                result.append(post2[p2])
                p2 += 1
            return result
        else:
            return "One of both words are not in the index"

    def and_postings(self, word1, word2):
        if word1 in self.index.keys() and word2 in self.index.keys():
            post1 = list(self.index[word1])
            post2 = list(self.index[word2])
            p1 = 0
            p2 = 0
            result = list()
            ## loop through the index until both pointers equal to the length
            while p1 < len(post1) and p2 < len(post2):
                if post1[p1] == post2[p2]:
                    result.append(post1[p1])
                    p1 += 1
                    p2 += 1
                elif post1[p1] > post2[p2]:
                    p2 += 1
                else:
                    p1 += 1
            return result
        else:
            return "no such words in the index"
        


def main():
    indexer = Indexer.from_directory()
    print(indexer.and_postings("a", "the"))
    print(indexer.unique_terms)

if __name__ == "__main__":
    main()






