#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NGrams class cuts a text on the space (or any other regular expression pattern), and returns the associated tokens (that are words, bigrams, paragraphs, ...) in a list of Span objects, or a list of strings, or a Tokens instance.
"""

import re
from tokenspan import Span
from .base_tokenizer import BaseTokenizer

class NGrams(BaseTokenizer,Span):
    """
NGrams is a sub-class of Span. It allows cutting the text (given as string parameter) on the space (whatever its length, a space can also be a newline or a tabulation), and extracting the words in between these spaces. One can change the regular expression (REGEX) in order to cut the parent string into different Span objects. For instance

```python
s = "A-B-C-D"
NGrams(s,regex='-').tokenize().toStrings()
# -> ['A', 'B', 'C', 'D']
```

would split the initial string into its constituents after cutting the string on the `'-'` symbol, and returns a list of the sub-strings (one would have obtained the same thing using `s.split('-')`.
                                                                                                                                         Other basic examples are
                                                                                                                                         
```python
s = "A-B-C-D"
NGrams(s,regex='-').tokenize(2).toStrings()
# -> ['A B', 'B C', 'C D']
NGrams(s,regex='-',subtoksep='@').tokenize(2).toStrings()
# -> ['A@B', 'B@C', 'C@D']
NGrams(s,regex='-',subtoksep='@').tokenize(2).ngrams
# -> [NGrams('A@B', [(0,1),(2,3)]),
#     NGrams('B@C', [(2,3),(4,5)]),
#     NGrams('C@D', [(4,5),(6,7)])] # a list of NGrams objects
NGrams(s,regex='-',subtoksep='@').tokenize(2).toTokens()
# -> Tokens(3 Token) : A@B  B@C  C@D # a Tokens object
```

The main interests in the NGrams class is to extract into Tokens objects, or Span objects the different tokens, in order to continue working on them.

By default
```python
s = "A    B \t C  \n D"
NGrams(s).tokenize().toStrings()
# -> ['A', 'B', 'C', 'D']
```
    """
    def __init__(self,
                 string=str(),
                 subtoksep=chr(32),
                 ranges=list(),
                 regex='\s+'):
        """
NGrams has all the parameters of a Span object, namely `string` (the string to be tokenized), a `subtoksep` that will be inserted between the different sub-tokens of a Span object (default is a free space), and a `ranges` list of range objects. In addition, the `regex` parameter allows to change the regular expression used to detect the spaces, default being `'\s+'` for any white space. For instance, changing `regex='\n'` would allow tokenization on paragraph.
        """
        Span.__init__(self,string=string,subtoksep=subtoksep,ranges=ranges)
        self.regex = regex
        self.ngrams = list()
        self._name_ = 'NGrams'
        return None
    
    @property
    def _subtokens_(self,):
        return self.ngrams
    
    def tokenize(self, ngram=1, regex='\s+', flags=0):
        """
Tokenize the parent string into tokens, that are themselves instances of NGrams.
Returns the NGrams object itself (tokenize is an in-place operation). The different tokens are then stored in NGrams.ngrams list.

Parameters | Type | Details
--- | --- | --- 
`ngram` | integer | the number of regular expression (`regex` parameter) that is withdraw in between two ngrams. In the default settings, `ngram=1` extracts words, `ngram=2` extracts bi-grams, ... 
`regex` | a REGEX (string) | a regular expression (REGEX) that will serve to identify the Token to be find
`flags` | some REGEX flags | flags are inherited from `re` package, and can be combined using a pipe symbol, for instance `flags=re.DOTALL|re.MULTILINE` apply both DOTALL (special character '.' also accepts new line) and MULTILINE (special characters '^' and '$' match begining and end of each new line)
        """
        self.regex = regex
        removes = (range(r_.start+r.start(),r_.start+r.end()) 
                   for r_ in self.ranges
                   for r in re.finditer(self.regex,
                                        self.string[r_.start:r_.stop],
                                        flags=flags))
        self.remove_ranges(removes)
        sub_spans = self.subSpans
        self.ngrams = []
        for i in range(len(sub_spans)-ngram+1):
            ranges = []
            for span in sub_spans[i:i+ngram]:
                ranges.extend(span.ranges)
            ngram_ = NGrams(self.string,
                            ranges=ranges,
                            subtoksep=self.subtoksep,
                            regex=self.regex)
            self.ngrams.append(ngram_)
        return self
