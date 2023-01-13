# Advent of Code 2022, Day 7

## Instructions

Running `main.py` will launch a command prompt to access the file system built
after solving this problem

## Help

```
ls                      - List items
mkdir [name]            - Creates new directory
mkfile [size] [name]    - Creates new file
pwd                     - Prints current path
sml_dirs [limit]        - Returns the sum of all child directories 
                                that are below the limit in size. 
                                Run from root with a limit of 100000 for part 1 answer
find_space [space_required] - Finds the smallest directory larger then the space required
                                Run from root with a value of 30000000 for the answer to part 2
help [command:optional] - Prints help to screen
clear                    - Clears the terminal screen
exit                     - Exits the program
part1                    - Moves to root and runs sml_dirs with the parameters
                                for part 1
part2                    - Moves to root and runs find_space with the parameters for part 2
```
