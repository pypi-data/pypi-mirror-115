Wildgram tokenizes english text into "wild"-grams (tokens of varying word count)
that match closely to the the natural pauses of conversation. I originally built
it as the first step in an abstraction pipeline for medical language: since
medical concepts tend to be phrases of varying lengths, bag-of-words or bigrams
doesn't really cut it.

Wildgram works by measuring the size of the noise (stopwords, punctuation, and
whitespace) and breaks up the text against noise of a certain size
(it varies slightly depending on the noise).

Parameters:

text
Required: Yes
Default: No
What it is: the text you want to wildgram.

stopwords
Required: No
Default: STOPWORDS list (importable, mostly based on NLTK's stop word list)
What it is: a list of stop words that you want to mark as noise, that will act as breaks between tokens.
Custom Override: a list of strings that you want to split on.

topicwords
Required: No
Default: TOPICWORDS list (importable)
What it is: a list of stop words that you want to mark as tokens because they have meaning, but often serve to break up larger pieces of text. Examples include numbers, negation words like "won't", etc. Includes numbers,
negations, and that kind of thing. Words that start with a number and end with a non-space, non-digit string
are split up, because the assumption is they are meaningfully distinct -- e.g. "123mg" -> "123", "mg".
Custom Override: a list of strings that you want to split on. You can also store a mixed list of
dictionaries and strings, dictionaries in the form {token: "text", tokenType: "custom type"}
for example, by default any negation stop words (like "no") have a tokenType of "negation".
If no tokenType is set, the type is "token".

include1gram
Required: No
Default: True
What it is: when set to true, wildgram will also return every individual word or token as well as any phrases it finds.
Custom Override: Boolean (false). When set to false, wildgram will only return the phrases it finds, not 1grams as well.

joinerwords
Required: No
Default: JOINERWORDS list (importable, words like "of")
What it is: a list of stop words (must also be included in stop word list if overridden) that join two phrases together. Example: "shortness of breath" -> "shortness", "breath", "shortness of breath".
Custom Override: a list of strings you want to join on. WORDS MUST BE IN STOPWORDS LIST FOR THIS TO WORK. The assumption is you wouldn't want a joiner word that is also a topic word.

returnNoise
Required: No
Default: True
What it is: when set to true, wildgram will also return each individual noise token it created to find the phrases.
Custom Override: Boolean (false). When set to false, it will not return the noise tokens.


includeParent
Required: No
Default: False
Note: In the process of being deprecated, because I didn't find it to be useful in topic organizing.
What it is: when set to true, wildgram will also return the "parent" of the token, in a pseudo-dependency tree.
This tree is generated using a ranked list of the prior (in the text) styles of punctuation to approximate
the relationships between tokens. Noise tokens act as branching nodes while normal tokens can only be leaf nodes,
so in practice this is used to determine the "uncles" of the token. Examples of how this might be useful is
linking list like elements under a larger heading or figuring out the unit of a number based on the context (which may not be on the same line). Since noise tokens are the branching nodes, returnNoise must be set to true if includeParent is true.
Custom Override: Boolean (True). When set to True, it will not return the parent.


Returns:
a list of dictionaries, each dictionary in the form:
```python
example = {
"startIndex": 0,
"endIndex", 5,
"token": "hello",
"tokenType": "token" # if noise, token type is "noise"
"index": 0
}
```
The list is sorted in ascending (smallest->largest) order for the startIndex, then the endIndex.


Example code:

```python
from wildgram import wildgram
ranges = wildgram("and was beautiful", returnNoise=False)

#[{
#"startIndex": 8,
#"endIndex", 17,
#"token": "beautiful",
#"tokenType": "token",
# "index": 0
#}]

from wildgram import wildgram
ranges = wildgram("and was beautiful day")
print(ranges)
'''
[{
  "startIndex": 0,
  "endIndex": 8,
  "token": "and was ",
  "tokenType": "noise",
  "index": 0
},
{
  "startIndex": 8,
  "endIndex": 17,
  "token": "beautiful",
  "tokenType": "token",
  "index": 1
},
{
  "startIndex": 8,
  "endIndex": 21,
  "token": "beautiful day",
  "tokenType": "token",
  "index": 2
},
{
  "startIndex": 17,
  "endIndex": 18,
  "token": " ",
  "tokenType": "noise",
  "index": 3
},
{
  "startIndex": 18,
  "endIndex": 21,
  "token": "day",
  "tokenType": "token",
  "index": 4
}
]
'''
```

With versions >= 0.2.9, there is also the class WildRules. This applies a set of
rules to the tokenized wildgram, making a basic rule based classifier. This shall
be optimized in future versions for speed, etc. In later versions, it also allows you
to specify given phrases nearby.

With version >= 0.4.1, there is also the class WildForm. This lets you group
the output of wildrules into potentially overlapping or incomplete forms. In later versions, we will
add extra validation functionality
example:
```python
from wildgram import WildRules, WildForm

test= WildRules([{"unit": "TEST", "value": "unknown", "spans": ["testing", "test"], "spanType": "token", "nearby": [{"spanType": "token", "spans": ["1234"]}]}, {"unit": "Dosage", "value": {"asType": "float", "spanType": "token"}, "spans": ["numeric"], "spanType": "tokenType"}])
ret = test.apply("testing test 123")
# note the unit for testing test is unknown, because it is missing 1234 in the general area
# note it can do basic parsing for values, say numbers.
[{'unit': 'unknown', 'value': "unknown" 'token': 'testing test', 'startIndex': 0, 'endIndex': 12}, {'unit': 'Dosage', "value": 123.0, 'token': '123', 'startIndex': 13, 'endIndex': 16}]

ret = test.apply("testing test 1234")
## returns the unit TEST, since 1234 is in the area
[{'unit': 'TEST', 'value': "unknown" 'token': 'testing test', 'startIndex': 0, 'endIndex': 12}, {'unit': 'Dosage', "value": 1234.0, 'token': '1234', 'startIndex': 13, 'endIndex': 17}]

forms = WildForm()
## lets add a basic form, with one "question" (e.g. a unit-value pair where the value is "")
forms.add_form({"unit": "test", "value": "testing", "children": [{"unit": "test", "value": "", "children": []}]})


## lets add a second form, with two "questions"
forms.add_form({"unit": "test", "value": "testing", "children": [{"unit": "test", "value": "", "children": []}, {"unit": "Dosage", "value": "", "children": []}]})
## lets apply this to this phrase:
rules = WildRules([{"unit": "test", "value": "unknown", "spans": ["testing", "test"], "spanType": "token"}, {"unit": "Dosage", 'value': {"spanType": "token", "asType": "float"}, "spans": ["numeric"], "spanType": "tokenType"}])

ret = rules.apply("testing, can anyone hear me? testing 1234")
## output:
[{'unit': 'test', 'value': 'unknown', 'token': 'testing', 'startIndex': 0, 'endIndex': 7}, {'unit': 'unknown', 'value': 'unknown', 'token': 'anyone hear me', 'startIndex': 13, 'endIndex': 27}, {'unit': 'test', 'value': 'unknown', 'token': 'testing', 'startIndex': 29, 'endIndex': 36}, {'unit': 'Dosage', 'value': 1234.0, 'token': '1234', 'startIndex': 37, 'endIndex': 41}]

forms.apply(ret)
## returns
## note: returns four forms: 2 filled out copies of the first form (for each instance of "testing", note start/endIndex)
## 2 copies of the second form: note that 1 copy has a missing value for dosage, since in 1 instance of testing there
## is no value of dosage that is not nearer to the previous
## so inter-form overlap is possible, but not intra-form overlap
## tokens are assigned right to left, so if there is a conflict the value belongs to the stuff on the left, and then the
## new question gets to start its own form even if the other form is incomplete
## it keeps track of the closest token (from rules) and if there are >= 3 tokens between the closest token in the form
## and the current one it also creates a new form, since it assumes the information will be close together
## this assumption may be modified, or overridden in time. I haven't decided yet, but it holds up pretty well for the things
## i want to pull from notes.
[{'unit': 'test', 'value': 'testing', 'children': [{'unit': 'test', 'value': 'unknown', 'children': [], 'startIndex': 0, 'endIndex': 7, 'token': 'testing'}]}, {'unit': 'test', 'value': 'testing', 'children': [{'unit': 'test', 'value': 'unknown', 'children': [], 'startIndex': 29, 'endIndex': 36, 'token': 'testing'}]}, {'unit': 'test', 'value': 'testing', 'children': [{'unit': 'test', 'value': 'unknown', 'children': [], 'startIndex': 0, 'endIndex': 7, 'token': 'testing'}, {'unit': 'Dosage', 'value': '', 'children': []}]}, {'unit': 'test', 'value': 'testing', 'children': [{'unit': 'test', 'value': 'unknown', 'children': [], 'startIndex': 29, 'endIndex': 36, 'token': 'testing'}, {'unit': 'Dosage', 'value': 1234.0, 'children': [], 'startIndex': 37, 'endIndex': 41, 'token': '1234'}]}]


```
## Handling Form meta information:

On the data element you want it to apply, add a child with unit "EHR" and value "META-FORM":
```python3
{your data element "children": [{'unit': 'EHR', 'value': 'META-FORM', 'children': []}]}
```
Meta information can be added in no particular order as a child of the EHR:META-FORM pair.

Available Arguments:
"EHR":"INTRA-FORM-SHARABLE" - if added, it will allow the same data element to be added to multiple copies of the same form. Default is that it assumes that elements cannot be shared across copies of the same form. An example would be a sentence like "for 3 weeks had nausea, diarrhea, and vomiting" would associate the element weeks:3 with nausea AND diarrhea AND vomiting. Note that the reverse isn't true -- so "had nausea, diarrhea, and vomiting for 3 weeks", weeks:3 is only associated with vomiting, since the meaning isn't clear (is it they have nausea/diarrhea/vomiting, and vomiting for 3 weeks or 3 weeks for all three?).
 





That's all folks!
