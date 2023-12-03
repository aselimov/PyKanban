""" This module contains classes and functions to contain the kanban board information """

import numpy as np
import yaml

class Task:
    """ This class represents each task, 
    """
    def __init__(self, summary, score, description):
        """ Initialize the task class
        """
        # Each task has the following properties
        self.summary = summary # Summary of the task
        self.score = score # Score for ticket
        self.description = description # Description of ticket


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

        self.file = file

        if file:
            self.read_yaml(file)


    def read_yaml(self, file):
        """ Read the yaml file in and set up the data 

        Arguments:
        file - yaml file to read in
        """

        # Read in the data
        with open(file, 'r') as f:
            data = yaml.safe_load(f)

        # Assign the data to board variables
        self.columns = data['columns']
        self.tasks = [[] for col in self.columns]
        for task in data['tasks']:
            self.tasks[self.columns.index(task['column'])].append(
                    Task(task['summary'], task['score'], task['description']))

    def write_yaml(self, file):
        """ Write the yaml file 

        Arguments:
        file - yaml file to write to
        """

        # Set up data to write out 
        data = dict()
        data['columns'] = self.columns
        data['tasks'] = list()
        for col,task_list in zip(self.columns, self.tasks):
            for task in task_list:
                data['tasks'].append({'column':col, 'summary':task.summary, 'score':task.score, 
                                      'description':task.description})

        with open(file, 'w') as f:
            yaml.dump(data, f)
                

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

    def update_task( self, icol, itask, task):
        """ Update the task based on text """
        self.tasks[icol][itask] = task

    def add_task( self, icol, task):
        """Add a task to icol"""
        self.tasks[icol].append(task)

    def del_task(self, icol, itask):
        del self.tasks[icol][itask]

