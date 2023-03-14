"# final-year-project-2023" 

## Portrayal of Etymologies from the Oxford English Dictionary (OED)

This program takes the etymology section of an OED entry and creates a map showing the given English word's cognates, with arrows tracing the word's descent, usually from Proto-Indo-European. A year can also be given, in which case the map will distinguish living languages from dead languages (at that time), as well as languages yet to exist. Otherwise living and dead languages are shown in the current year.

The maps given are not complete by any means as they only include words included in the OED entry itself.

How to use:

`language_tree.py <word> [-y <year>]`

where word is one of these test words:

- daughter
- father
- quick
- smart
- city
- money

and <year> is an ISO 8601 year between -4500 (4501 BC) and the current year.

##Examples

###"daughter" in 2000 AD

[!A map of Europe and Asia, showing cognate words to the English word "daughter", as of the year 2000 AD. Arrows connect the words, tracing the ancestry of the word back through the word's parent languages.](examples/daughter_2000_ad.png)

###"daughter" in 1000 AD
[!A map of Europe and Asia, showing cognate words to the English word "daughter", as of the year 1000 AD. Arrows connect the words, tracing the ancestry of the word back through the word's parent languages.](examples/daughter_1000_ad.png)

###"father" in 1000 BC
[!A map of Europe and Asia, showing cognate words to the English word "father", as of the year 1000 BC. Arrows connect the words, tracing the ancestry of the word back through the word's parent languages.](examples/father_1000_bc.png)

###"money" in 1000 AD
[!A map of Europe and Asia, showing cognate words to the English word "money", as of the year 1000 AD. Arrows connect the words, tracing the ancestry of the word back through the word's parent languages.](examples/money_1000_ad.png)