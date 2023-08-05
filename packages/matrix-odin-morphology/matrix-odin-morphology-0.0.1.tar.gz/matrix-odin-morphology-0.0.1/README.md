# README #


### What is this repository for? ###

* This repo hosts a version of MOM sofware, originally developed by David Wax in 2014.
* It was later significantly changed by Olga Zamaraeva.
* It is part of the AGGREGATION project
* The software helps infer morphological position classes (slots) from interlinearized data.


### What to cite if I use MOM for my research? ###
* [Wax, David Allen. Automated grammar engineering for verbal morphology. Diss. 2014.](https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/25373/Wax_washington_0250O_12899.pdf?sequence=1&isAllowed=y)
* [Zamaraeva, Olga. Inferring Morphotactics from Interlinear Glossed Text: Combining Clustering and Precision Grammars. SIGMORPHON 2016 (2016): 141.](http://www.anthology.aclweb.org/W/W16/W16-20.pdf#page=153)

### How do I get set up? ###

* Please see the [Wiki](https://bitbucket.org/olzama/mom/wiki/). Most of the info is there, some may be outdated.

* There are dependencies; you should be able to easily install them by pip, but you may need to manually install Graphviz.

* You will need a config file. Please see a sample eng_config under config_files, ass well as documented_config for comments.

* You will need some files, particularly files containing what the program will treat as gloss grams and POS tags. See mom/util/collect_tags_xigt.py

* For morphosyntactic features, the program relies on FeatDict.py. mom/util/collect_tags_xigt.py will report if it finds grams that are not yet mapped to anything in FeatDict.py. Please enter them there manually, all lowercased, to whichever dictionary you think they should belong.

### Who do I talk to? ###

* Please contact Emily M. Bender about the AGGREGATION project and ask who is currently working on MOM. 
* You can also contact olga.zamaraeva@ (geeeeemail), who may or may not be able to help you at this point (she will try).