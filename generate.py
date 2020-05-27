import sys
from crossword import *
from queue import Queue


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            rem_words = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    rem_words.add(word)
            self.domains[var] -= rem_words


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False

        answer = False
        rem_word = set()
        for xword in self.domains[x]:
            found = False
            for yword in self.domains[y]:
                if xword[overlap[0]] == yword[overlap[1]]:
                    found = True
                    break
            if found is False:
                answer = True
                rem_word.add(xword)

        self.domains[x] -= rem_word
        return answer


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = Queue()
            for overlap in self.crossword.overlaps:
                arcs.put(overlap)

        while arcs.empty() is False:
            arc = arcs.get()
            update = self.revise(arc[0], arc[1])

            if update is True:
                if self.domains[arc[0]] is None:
                    return False
                for neighbour in self.crossword.neighbors(arc[0]):
                    arcs.put((neighbour, arc[0]))

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) != len(self.domains.keys()):
            return False
        for var in assignment:
            if assignment[var] is None:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        unique = set()
        for var in assignment:
            word = assignment[var]

            if len(word) != var.length:
                return False
            if word in unique:
                return False
            else:
                unique.add(word)
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    word_1 = assignment[neighbor]
                    if word[overlap[0]] != word_1[overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        rule_out_map = {}
        words = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for word in words:
            count = 0
            for neighbour in neighbors:
                words = self.domains[neighbour]
                if word in words:
                    count += 1
            rule_out_map[word] = count

        rule_out_map = {k: v for k, v in sorted(rule_out_map.items(), key=lambda item: item[1])}

        return list(rule_out_map)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = set()
        remaining_values = len(self.crossword.words)
        for var in self.domains:
            if var not in assignment:
                value = len(self.domains[var])
                if value < remaining_values:
                    unassigned = set()
                    unassigned.add(var)
                    remaining_values = value
                elif value == remaining_values:
                    unassigned.add(var)

        highest_degree = 0
        tie_set = set()
        for var in unassigned:
            value = len(self.crossword.neighbors(var))
            if value > highest_degree:
                highest_degree = value
                tie_set = set()
                tie_set.add(var)
            elif value == highest_degree:
                tie_set.add(var)

        return tie_set.pop()




    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        words = self.order_domain_values(var, assignment)

        for word in words:
            temp = assignment.copy()
            temp[var] = word

            if self.consistent(temp):
                assignment[var] = word
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result

    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
