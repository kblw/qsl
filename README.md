## QSL - query search language

#### Usage for parsing search variable in query string (for HTTP requests)

### Grammar

    <lang> = sepBy ";" <rule>
    <rule> = <variable>: <expression> | -<variable>: <expression> # first symbol "-" for exclude the expression from search
    <variable> = [a-Z][a-Z0-9_-+]
    <expression> = <atom> | <list> | <interval>
    <atom> = <float> | <number> | <datetime> | <string>
    <list> = sepBy "," <expression>
    <interval> = <expression> .. <expression>

### Examples

    a: 1        - search by a=1
    a: 1..100   - search by a in (1, .., 100)
    a: .. 100   - serach by a <= 100
    a: 1 ..     - serach by a >= 1
    a: 1, 2, 3  - search by a in [1,2,3]
    -a: 1       - exclude a=-1 
