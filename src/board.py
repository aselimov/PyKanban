""" This module contains classes and functions to contain the kanban board information """

class Board:
    def __init__(self, file = None):
        """ Initialize the Board class, this class has three important class variables. 
        These are:
        self.sprint | str - name of the current sprint
        self.columns | list(str) - columns in kanban board
        self.tasks | list(list()) - tasks in each column

        """
        self.sprint = None
        self.columns = list()
        self.tasks = list()

        self.file = ''
        self.file = file

        if file:
            self.parse_md(file)


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
                    # The tasks are a list of [col index, task name]
                    self.tasks[-1].append(" "+' '.join(line.split(' ')[1:]))


    def write_md(self):
        with open(self.file, 'w') as f:
            f.write('#\n\n')
            for i,col in enumerate(self.columns):
                f.write('## {}\n\n'.format(col))
                for task in self.tasks[i]:
                    f.write('- {}\n'.format(task[1][1:]))
                f.write('\n')
                

    def move_task(self, col_index, task_index, direction):
        """ This class method moves tasks between columns by incrementing/decrementing the column
        index
         
         Arguments:
         col_index - index of the column we are in
         task_index - index of the task we are changing in the column
         direction - direction to move the task

         Returns:
         moved - True if a task was moved else false
        """
        task = self.tasks[col_index][task_index]
        if col_index+direction >= 0 and col_index+direction < len(self.columns):
            self.tasks[col_index+direction].append(task)
            del self.tasks[col_index][task_index]
            return True

        else: 
            return False



    def print_board_items(self):
        for i, col in enumerate(self.columns):
            print(col)
            print(self.tasks[i])

    def get_columns(self):
        """ Return  columns"""
        return self.columns

    def get_tasks(self):
        """ Return  tasks"""
        return self.tasks

    def get_task(self, icol, itask):
        """ Return a task based on column and task index"""
        return self.tasks[icol][itask]
