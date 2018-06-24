# BabelDictionary

#### What is BabelDictionary?
**BabelDictionary** is a Python project that analyzes a random page of [The Library of Babel](https://libraryofbabel.info/) and checks for dictionary words. It then posts the three longest words to the Twitter account [@BabelDictionary](https://twitter.com/BabelDictionary)

#### How does it work?
BabelDictionary requests a random page from the library and uses the *lxml* library to scrape the page title and contents. Then, using a list of 466,000  English words provided by [this repository](https://github.com/dwyl/english-words) it searches the contents for any matches and returns the three longest word results. Simple!

#### Why though?  ¯\\\_(ツ)_/¯
The Library of Babel has always been an interesting concept to me, and who doesn't love a Twitter Bot? Maybe we'll find something interesting.

#### Changelog
* **24th June 2018**
    * Updated dictionary source
    * Optimise searching method

##### Attribution
* [Twitter Profile Logo](https://www.vecteezy.com/vector-art/168469-free-books-libro-icons-vector) 