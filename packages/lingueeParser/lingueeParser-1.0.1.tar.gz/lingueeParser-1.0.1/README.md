# Linguee Parser

This is a parser for the Linguee dictionary. It is prohibited by the terms and conditions to use this script to forward their service to third parties. For more information see below.

This script parses the translation based on the html IDs and classes. Therefore, if Linguee decides to change the HTML this script is going to brake.

## How to use the script?
1. Download the script with pip or git
2. Import it: `from lingueeParser import linguee`
3. Create an instance of the object: `parser = linguee.Linguee(("english", "german"))`
4. Search for terms: `term = parser.search('spam')`

Notes:
> You can access all your searches with `parser.get_dictionary()`

> Search gives only the term the same would be `parser.get_dictionary()['spam']`


## Terms and Conditions
If you use the API, make sure you comply with Linguee [Terms and Conditions](https://www.linguee.com/page/termsAndConditions.php), and in particular with that clause:

Both private and business usage of linguee.com services is free of charge. It is however strictly prohibited to forward on our services to third parties against payment