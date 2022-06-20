# Tibetan grammar boxing tool

This little application allows to mark up the grammar structure of Tibetan sentences. You can type on the left side of the screen and the right side of the screen will show a generated PDF document that is based on your input. This PDF document can also be downloaded by using the menu in the upper right corner of the screen.

To get started, just delete the text on the left side of the screen, paste in some Tibetan text and then annotate it as you like.


The following conventions are used while typing:

* Lines that start with a > character are considered to contain Tibetan text where boxes can be defined, for example:

> དམིགས་པ་

* If a line starts with two >> characters instead of one then the Tibetan Text is also indented, for example:

>> དམིགས་པ་

* Boxes are defined by using square brackets. The format is: [text below:text above:Tibetan text], for example:

>> [observe:trans v.:དམིགས་པ་]


* It is also possible to create plain boxes or to only specify the text above or below, such as:

>> [དམིགས་པ་], or [observe:དམིགས་པ་], or [:trans v.:དམིགས་པ་]

* It is also possible to label a portion of Tibetan text without drawing a box around it. This is done by using parentheses instead of square brackets with the following format (text below:text above:Tibetan text), for example:

>> (if / when:s.p.:ན་), or (if / when:ན་), or (:s.p.:ན་)


* Boxes can be nested, for example:

>> [[true sufferings:object:སྡུག་བདེན་](:2nd:ལ་)[observe:trans v.:དམིགས་པ]](:6th:འི་)[afflictions:noun:ཉོན་མོངས་]


* Even for nested boxes it is possible to add labels on all levels of nesting, such as this:

>> [afflictions that observe true sufferings:
>    [observing true sufferings:
>      [true sufferings:object:སྡུག་བདེན་](:2nd:ལ་)[observe:trans v.:དམིགས་པ]
>    ](:6th:འི་)[afflictions:noun:ཉོན་མོངས་]
>  ]
(In the above example the entered text is also typed in multiple lines that each start with a > character. While typing, the text for a Tibetan passage can split up into multiple lines at any point as long as each line of the passage continues to start with a > character.  Splitting things into multiple lines is completely optional and has no effect on the output, but it may help to keep track of longer annotations and nested brackets.)


* English lines (i.e., lines that *don't* start with a > character) can be formatted with *markdown* formatting conventions. The formatting options are described at: https://pandoc.org/MANUAL.html#pandocs-markdown

# Bigger example:

The following example is based on Craig Preston's book *How to Read Classical Tibetan, Vol. 2: Buddhist Tenets* and shows how Tibetan text can be annotated:

> [
>   [
>     [true sufferings:object:སྡུག་བདེན་](:2nd:ལ་)[observe:trans v.:དམིགས་པ]
>   ](:6th:འི་)[afflictions:noun:ཉོན་མོངས་]
>   [completely:adj:མ་ལུས་པ](:2nd:ར་)[abandon:verb:སྤངས་པ་]
>   (if  / when:s.p.:ན་)
> ]
> 
> [
>  [true sufferings:obj.:སྡུག་བདེན་][abandon:trans.v.:སྤངས་པ]
> ](:2nd:ར་)
> [posit:འཇོགས་པ][because:post:འི་ཕྱིར་]

"This is so because when one has abandoned completely the afflictions that observe true sufferings, [that is] posited as having abandoned true sufferings."

# Source code
The source code is available at: https://github.com/christiansteinert/tibetan-boxing

It is a relatively quick hack but it works :-).