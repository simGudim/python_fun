review_1 = "The Glider II is a great soccer ball hello great"
review_2 = "What a bad soccer ball hello great"
review_3 = "I am happy with The glider hello great"

docs = [review_1, review_2, review_3]

unique_terms = {term for doc in docs for term in doc.split()}
inverted_index = {}

for i, doc in enumerate(docs):
    for term in doc.split():
        if term in inverted_index:
            inverted_index[term].add(i)
        else:
            inverted_index[term] = {i}

def or_postings(post1, post2):
    p1 = 0
    p2 = 0
    result = list()
    while p1 < len(post1) and p2 < len(post2):
        
        if post1[p1] == post2[p2]:
            result.append(post1[p1])
            p1 += 1
            p2 += 1
        elif post1[p1] > post2[p2]:
            result.append(post2[p2])
            p2 += 1
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

pl_1 = list(inverted_index['soccer'])
pl_2 = list(inverted_index['glider'])
print(or_postings(pl_1, pl_2))


def and_postings(post1, post2):
    p1 = 0
    p2 = 0
    result = list()
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



pl_1 = list(inverted_index['great'])
pl_2 = list(inverted_index['hello'])
print(and_postings(pl_1, pl_2))


