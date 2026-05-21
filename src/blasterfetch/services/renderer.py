import datetime
from itertools import batched

from rich.console import Console, Group
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

from blasterfetch.enums import Categories
from blasterfetch.types import Digest, DigestDateManager, DateNotFoundError

DEFAULT_COLUMN_WIDTH = 40
        
COLUMN_HEIGHT_TOLERANCE = 2

def format_digests(digests: list[Digest],
                  width: int = DEFAULT_COLUMN_WIDTH) -> list[Panel]:
    formatted = []
    for digest in digests:
        title = Text(text=digest['title'], justify="center", 
                     style=f"bold underline link {digest['url']}")
        description = Text(digest['description'])
        
        panel = Panel(Text.assemble(title,"\n",description,end=""),
                      width=width,
                      box=box.SIMPLE,
                      padding=(0,0),
                      expand=False)
        formatted.append(panel)
    return formatted

def format_category_header(category_value: str,
                           width: int = DEFAULT_COLUMN_WIDTH):
    category = Categories(category_value)
    text = ("Professional Development"  if category == Categories.CAREER 
            else category_value)
    formatted_text = add_horizontal_rule(text, width)
    return Text(formatted_text,
                justify="center",
                end="")

def add_horizontal_rule(text: str, 
                        width: int):
    lines = ["".join(chunk) for chunk in batched(str(text), width)]
    last_line = lines[-1]
    margins = width - 2 - len(last_line)
    left_len = margins // 2
    formatted_last_line = f"{"─" * left_len} {last_line} {"─" * (margins - left_len)}"
    return "\n".join(lines[:-1] + [formatted_last_line])


def render(digests: DigestDateManager,
           date_to_render: datetime.date | None = None,
           strict_date: bool = False,
           column_width: int = DEFAULT_COLUMN_WIDTH):
    if date_to_render is None:
        date_to_render = datetime.date.today()
    console = Console()
    num_columns = console.width // column_width
    
    if strict_date and str(date_to_render) not in digests.keys():
        raise DateNotFoundError()
    
    while str(date_to_render) not in set(digests.keys()):
        date_to_render -= datetime.timedelta(days=1)

    grid = Table(padding=(0,1),
                 box=box.HORIZONTALS,
                 show_header=False)
    grid.title = f"{date_to_render} Daily Blast"
    [grid.add_column() for _ in range(num_columns)]

    printed_digests = digests[str(date_to_render)]
    elements = []
    for category, digest_items in printed_digests.items():
        elements.append(format_category_header(category))
        elements.extend(format_digests(digest_items))
        
    total_height = sum([len(console.render_lines(element)) for element in elements])
    column_height = total_height//num_columns - COLUMN_HEIGHT_TOLERANCE
    columns = [Group() for _ in range(num_columns)]
    
    total_height = 0
    column_num = 0
    for i, element in enumerate(elements):
        total_height += len(console.render_lines(element))
        columns[column_num].renderables.append(element)
        
        if total_height >= column_height:
            column_num += 1
            total_height = 0
        
        if column_num == (num_columns - 1):
            columns[column_num].renderables.extend(elements[i+1:])
            break
    
    grid.add_row(*columns)
    console.print(grid, justify="center")