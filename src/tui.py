from textual.app import App, ComposeResult
from textual.widgets import Static, Label, ListItem, ListView
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from board import Board


class TaskList(ListView):
    """
        Inherited widget from Listview to use as the kanban board columns
    """
    # Keybinds
    BINDINGS = [
        Binding("k", "cursor_up", "Cursor Up", show=False, priority=True),
        Binding("j", "cursor_down", "Cursor Down", show=False, priority=True),
    ]


class KanbanForm(App):
    CSS_PATH = 'layout.tcss'
    BINDINGS = [
        Binding("l", "fnext", "Focus Next", show=False, priority=True),
        Binding("h", "fprev", "Focus Prev", show=False, priority=True),
        Binding("L", "move_up", "Focus Next", show=False, priority=True),
        Binding("H", "move_down", "Focus Prev", show=False, priority=True),
        Binding('q', 'exit', "Exit", priority=True, show=False) 
    ]

    def compose(self):
        """
        Initialization function for form
        """
        # Initialize our board class
        self.board = Board(file = '.board.md')
        self.cols = list()

        self.col_widgets = list()
        
         
        with Horizontal():
            for i,col in enumerate(self.board.get_columns()):
                if i < len(self.board.get_columns())-1:
                    col_class = 'column'
                else:
                    col_class = 'last-column'
                with Vertical(classes=col_class):
                    yield Static(col, classes='header')
                    yield TaskList(
                        *[ListItem(Label(task)) for task in self.board.get_tasks()[i]])

        # Now make all TaskLists except the first have no highlights
    def action_fnext(self):
        """ Focus next column"""
        self.children[0].focus_next()

    def action_move_up(self):
        icol, itask = self.get_col_task()
        text = self.board.get_task(icol, itask)
        moved = self.board.move_task(icol, itask, 1)
        if moved:
            query = self.query(selector=TaskList)
            self.focused.highlighted_child.remove()
            query.nodes[icol+1].append(ListItem(Label(text)))
            self.focused.action_cursor_down()
            self.action_fnext()
            self.focused.action_cursor_down()

        
    def action_fprev(self):
        """ Focus previous column """
        self.children[0].focus_previous()

    def action_move_down(self):
        icol, itask = self.get_col_task()
        text = self.board.get_task(icol, itask)
        moved = self.board.move_task(icol, itask, -1)
        if moved:
            query = self.query(selector=TaskList)
            self.focused.highlighted_child.remove()
            query.nodes[icol-1].append(ListItem(Label(text)))
            self.focused.action_cursor_down()
            self.action_fprev()
            self.focused.action_cursor_down()

    def action_exit(self):
        """ Exit the application """
        self.exit()

    def get_col_task(self):
        """ 
        This function gets the relevant column and task from the Board object for the current
        selected item in the tui.
        """
        focused_col = self.focused
        query = self.query(selector=TaskList)

        # First get the column index
        for i, child in enumerate(query.nodes):
            if focused_col == child:
                col_index = i

        # Now get the indext of the item in the list
        to_move = focused_col.highlighted_child
        for i, child in enumerate(focused_col.children):
            if to_move == child: 
                task_index = i

        return col_index, task_index
        

#    def on_key(self):
#        with open('log','a') as f:
#            f.write("{}".format(self.children[0].focus_next))

if __name__ == "__main__":
    kb = KanbanForm()
    kb.run()


