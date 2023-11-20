***Code checker***

**Ownership**
You must include your name and andrewId in a comment at the top of every file you submit. Your andrewId must be labeled as such. Use the following: "andrewId: myid"
This is good practice for later in life, when you will want to document all code that you contribute to projects.

**Comments**
You should write concise, clear, and informative comments that supplement your code and improve understanding.
Comments should be included with any piece of code that is not self-documenting.
Comments should also be included at the start of every function (including helper functions).
Comments should not be written where they are not needed.
5-point error: not writing any comments at all.
2-point error: writing too many or too few comments, or writing bad comments.


**Functions**
You should use top-down design to break large programs down into helper functions where appropriate.
This also means that no function should become too long (and therefore unclear).
5-point error: not using any helper functions (where helper functions are needed).
2-point error: using too many or too few helper functions.
2-point error: writing a function that is more than 20 lines long.
Exceptions: blank lines and comments do not count towards this line limit, and this rule does not apply to graphics functions and init()/run() functions in animations.



**Variable names**
Use meaningful variable and function names (whenever possible).
Variables and functions should be written in the camelCase format. In this format, the first letter is in lowercase, and all following words are uppercased (eg: tetrisPiece).
Variable names should not overwrite built-in function names; for example, str is a bad name for a string variable. Common built-in keywords to avoid include dict, dir, id, input, int, len, list, map, max, min, next, object, set, str, sum, and type.
5-point error: not having any meaningful variable names (assuming variables are used).
2-point error: using some non-meaningful variable names.
Exceptions: i/j for index/iterator, c for character, s for string, and n/x/y for number.
2-point error: not using camelCase formatting.
2-point error: using a built-in function name as a variable.


**Unused Code**
Your code should not include any dead code (code that will never be executed).
Additionally, all debugging code should be removed once your program is complete, even if it has been commented out.
2-points error: having any dead or debugging code.


**Formatting**
Your code formatting should make your code readable. This includes:
Not exceeding 80 characters in any one line (including comments!).
Indenting consistently. Use spaces, not tabs, with 4 spaces per indent level (most editors let you map tabs to spaces automatically).
Using consistent whitespace throughout your code.
Good whitespace: x=y+2, x = y+2, or x = y + 2
Bad whitespace: x= y+2, x = y +2, or x = y   + 2
2-point error: having bad formatting in any of the ways described above.