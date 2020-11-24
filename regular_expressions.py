import re


text_to_search = '''
    123123214125425fbgdfagfdagfdgdsGSg
    sdgsGSDGsfgrsgdsgdsgsdG

    HA HAHAHAHAH

    META CHARACTERS  (Need to be escaped):
    . ^$@%^^&*#^$${ } [] ( )

    coreyms.com

    12343-5425-2435-21451235
    324523.325.425243.134.32.5

    MRs. Robinson
    Mr. Sahfer
    Mr. T
    Mr. Davis
'''

pattern = re.compile(r'gs')
matches = pattern.finditer(text_to_search)
for i in matches:
    print(i)

pattern_escape = re.compile('\.')
mathces_escape = pattern_escape.finditer(text_to_search)
for i in mathces_escape:
    print(i)

url_escape = re.compile('coreyms\.com')
matches_url = url_escape.finditer(text_to_search)
for i in matches_url:
    print(i)

