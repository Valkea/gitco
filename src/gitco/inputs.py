from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory


class RetryException(Exception):
    def __init__(self, message):
        super().__init__(message)
    def __str__(self):
        return f"{self.message}"

class ExitException(Exception):
    def __init__(self, message=""):
        super().__init__(message)
    def __str__(self):
        return f"{self.message}"


# printed_lines = 0
# def clear_printed_lines():
#     pass
#     # global printed_lines
#     # for _ in range(printed_lines):
#     #     print('\033[F\033[K', end='')  # Move cursor up and clear line
#     # printed_lines = 0  # Reset counter


# Bottom help toolbar

def bottom_toolbar():
    cmd_list = [
        'New line on <b><style bg="ansired">ENTER</style></b>',
        'Apply command on <b><style bg="ansired">Double ENTER</style></b>',
        'Regenerate on <b><style bg="ansired">Ctrl+R</style></b>',
        'Exit on <b><style bg="ansired">Ctrl+C</style></b>',
    ]
    return HTML(" " + " | ".join(cmd_list))

# Create custom key bindings

bindings = KeyBindings()

@bindings.add("c-c")
def _(event):
    exit(0)

prompt_status = None
@bindings.add("c-r")
def _(event):

    global prompt_status
    prompt_status = "retry"

    buffer = event.current_buffer
    # buffer.text = "retry"
    buffer.validate_and_handle()
    # clear_printed_lines()  # Clear only printed lines

@bindings.add("enter")
def _(event):
    buffer = event.current_buffer

    # Submit if it's a single-line or final input
    if buffer.text.strip() and not buffer.text.endswith('\n'):
        # global printed_lines
        # printed_lines += 1
        buffer.insert_text("\n")

    # Add a newline if Enter is pressed with empty input
    else:
        buffer.validate_and_handle()
        #buffer.insert_text("EXIT\n")

# Multiline

def prompt_continuation(width, line_number, is_soft_wrap):
    return ' ' * 12

# Edit msg 

def prepare_command(suggested_commit_msg):

    # Initialize
    history = InMemoryHistory()
    session = PromptSession(history=history)

    # global printed_lines
    # printed_lines = 0

    global prompt_status
    prompt_status = None

    # Prompt with a default message
    # printed_lines += 2
    new_message = session.prompt(
        f'\nModify or Confirm your command:\n ',
        default = suggested_commit_msg,
        multiline = True,
        prompt_continuation = prompt_continuation,
        bottom_toolbar = bottom_toolbar,
        key_bindings = bindings,
    )

    # print(f"Updated message: {new_message}")
    return new_message.replace("\n", " "), prompt_status
