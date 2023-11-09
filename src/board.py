""" This module contains classes and functions to contain the kanban board information """

class Board:
    def __init__(self):
        """ Initialize the Board class, this class has three important class variables. 
        These are:
        self.sprint | str - name of the current sprint
        self.columns | list(str) - columns in kanban board
        self.tasks | list(list(str)) - tasks in each column

        """
        self.sprint = None
        self.columns = list()
        self.tasks = list()


    def parse_md(self, file):
        """ Upon starting the code we need to parse the markdown file which contains our board 
        information

        Arguments: 
        file - the path to the markdown file containing the board information
        """
        
        with open(file,'r') as f:
            for line in f:
                item_type = line.split(' ')[0]
                # Assign sprint 
                if item_type == '#':
                    # If sprint has already been defined we should exit the loop
                    if self.sprint:
                        break

                    # Otherwise assign it
                    try:
                        self.sprint = ' '.join(line.split(' ')[1:])

                    except IndexError:
                        # If a sprint title is not defined we default it to ' ' which we process 
                        # later
                        self.sprint=' '
                
                # Define a new column and add a list to the tasks variable that corresponds to that
                # column
                elif item_type == "##":
                    self.columns.append(' '.join(line.split(' ')[1:]))
                    self.tasks.append(list())

                # Now add the task to the list structures
                elif item_type == "-":
                    self.tasks[-1].append(' '.join(line.split(' ')[1:]))


    def print_board_items(self):
        for col, tasks in zip(self.columns, self.tasks):
            print(col, tasks)


