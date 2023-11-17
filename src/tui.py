from textual.app import App, ComposeResult
from textual.widgets import Static, Label, ListItem, ListView, TextArea, Input
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.binding import Binding
from board import Board, Task


class TaskList(ListView):
    """
        Inherited widget from Listview to use as the kanban board columns
    """
    # Keybinds
    BINDINGS = [
        Binding("k", "cursor_up", "Cursor Up", show=False, priority=True),
        Binding("j", "cursor_down", "Cursor Down", show=False, priority=True),
    ]

class EditTaskScreen(Screen):
    """
        This is a screen used to edit the name of a task
    """
    CSS="""
        Label{
            width:50%;
            background: #282828;
            padding: 1;
        }
        Input{
            width:50%;
            background: #282828;
            padding: 0 0;
            border: #ebdbb9;
        }

        Input:focus{
            border: #458588;
        }
        TextArea{
            width: 50%;
            height: 25%;
            background: #282828;
            border: #ebdbb9;
        }
        TextArea:focus{
            border: #458588;
        }
    """
    BINDINGS = [
        Binding('ctrl+s', 'save', 'Save Changes', priority=True),
        Binding('escape', 'exit', 'Exit Without Changes', priority=True),
    ]
    def __init__(self,text):
        """
        Initialize the screen
        """
        super().__init__()
        self.text = text

    def compose(self):
        """
        Compose the widgets on the screen, this screen doesn't need dynamic layout changes
        """
        yield Label('Task Name:')
        yield Input(value=self.text.summary)
        yield Label('Score:')
        if self.text.score:
            yield Input(value=self.text.score)
        else:
            yield Input(value="")
        yield Label('Description:')
        if self.text.description:
            yield TextArea(self.text.description, language='markdown')
        else:
            yield TextArea(language='markdown')


    def action_save(self):
        query = self.query(selector=Input)
        self.text.summary = query.nodes[0].value
        self.text.score = query.nodes[1].value
        query = self.query(selector=TextArea)
        self.text.description = query.nodes[0].text
        self.dismiss(self.text)

    def action_exit(self):
        self.dismiss(None)

class EditColScreen(Screen):
    """
        This is a screen used to edit the name of a task
    """
    CSS="""
        Label{
            width:50%;
            background: #282828;
            padding: 1;
        }
        Input{
            width:50%;
            background: #282828;
            padding: 0 0;
            border: #ebdbb9;
        }
    """
    BINDINGS = [
        Binding('ctrl+s', 'save', 'Save Changes', priority=True),
        Binding('enter', 'save', 'Save Changes', priority=True),
    ]
    def __init__(self,text):
        """
        Initialize the screen
        """
        super().__init__()
        self.text = text

    def compose(self):
        """
        Compose the widgets on the screen, this screen doesn't need dynamic layout changes
        """
        yield Label('Column Name:')
        yield Input(value=self.text)


    def action_save(self):
        query = self.query(selector=Input)
        self.dismiss(query.nodes[0].value)


class KanbanForm(App):
    CSS_PATH = 'layout.tcss'
    BINDINGS = [
        Binding("l", "fnext", "Focus Next", show=False, ),
        Binding("a", "new_task", "Add New Task", show=False, ),
        Binding("h", "fprev", "Focus Prev", show=False, ),
        Binding("L", "move_up", "Focus Next", show=False),
        Binding("H", "move_down", "Focus Prev", show=False),
        Binding("e", "edit_task", "Edit Task", show=False,),
        Binding("r", "edit_column", "Edit Column Name", show=False,),
        Binding('q', 'exit', "Exit")
        ]

    def compose(self):
        """
        Initialization function for form
        """
        # Initialize our board class
        self.board = Board(file = '.board.yaml')
        self.cols = list()

        self.col_widgets = list()
        
         
        with Horizontal():
            for i,col in enumerate(self.board.get_columns()):
                if i < len(self.board.get_columns())-1:
                    col_class = 'column'
                else:
                    col_class = 'last-column'
                with Vertical(classes=col_class):
                    if i == 0:
                        yield Static(col, classes='header-focused')
                    else:
                        yield Static(col, classes='header')
                    yield TaskList(
                        *[ListItem(Label(task.summary)) for task in self.board.get_tasks()[i]])

    def action_fnext(self):
        """ Focus next column"""
        query = self.query(selector=Static)
        query = [node for node in query.nodes if str(node) == 'Static()']
        icol, _ = self.get_col_task()
        query[icol].classes="header"
        self.children[0].focus_next()
        try:
            query[icol+1].classes="header-focused"
        except IndexError:
            query[0].classes="header-focused"

        

    def action_move_up(self):
        icol, itask = self.get_col_task()
        text = self.board.get_task(icol, itask).summary
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
        query = self.query(selector=Static)
        query = [node for node in query.nodes if str(node) == 'Static()']
        icol, _ = self.get_col_task()
        query[icol].classes="header"
        self.children[0].focus_previous()
        try:
            query[icol-1].classes="header-focused"
        except IndexError:
            query[-1].classes="header-focused"

    def action_move_down(self):
        icol, itask = self.get_col_task()
        text = self.board.get_task(icol, itask).summary
        moved = self.board.move_task(icol, itask, -1)
        if moved:
            query = self.query(selector=TaskList)
            self.focused.highlighted_child.remove()
            query.nodes[icol-1].append(ListItem(Label(text)))
            self.focused.action_cursor_down()
            self.action_fprev()
            self.focused.action_cursor_down()

    def action_edit_task(self):
        icol, itask = self.get_col_task()
        task = self.board.get_task(icol, itask)
        self.push_screen(EditTaskScreen(task), self.update_task)
    
    def action_new_task(self):
        self.push_screen(EditTaskScreen(Task(None,None,None)), self.new_task)

    def action_edit_column(self):
        icol, itask = self.get_col_task()
        text = self.board.get_columns()[icol]
        self.push_screen(EditColScreen(text), self.update_col)

    def update_col(self, text):
        """ Update the column
        """
        icol, itask = self.get_col_task()
        query = self.query(selector=Static)
        query = [node for node in query.nodes if str(node) == 'Static()']
        query[icol].update(text)
        self.board.get_columns()[icol] = text


    def action_exit(self):
        """ Exit the application """
        self.board.write_yaml(file='.board.yaml')
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

        # Now get the index of the item in the list
        to_move = focused_col.highlighted_child
        task_index = None
        for i, child in enumerate(focused_col.children):
            if to_move == child: 
                task_index = i

        return col_index, task_index
    
    def update_task(self, task):
        """ This function gets the text inputted in the edit screen and updates the underlying 
            task and the board class
            
        """
        if task:
            icol, itask = self.get_col_task()
            self.focused.highlighted_child.children[0].update(task.summary)
            self.board.update_task(icol, itask, task)

    def new_task(self, task):
        """ This function adds a new task to our board
        """
        if task:
            icol,_ = self.get_col_task()
            self.focused.mount(ListItem(Label(task.summary)))
            self.board.add_task(icol, task)
            self.focused.highlighted_child
    
#    def on_key(self):
#        with open('log','a') as f:
#            f.write("{}".format(self.children[0].focus_next))

if __name__ == "__main__":
    kb = KanbanForm()
    kb.run()


