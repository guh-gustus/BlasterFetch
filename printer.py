import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.style import Style
from rich.theme import Theme
from rich.table import Table
from rich.rule import Rule
from rich import box
from itertools import batched

from fetcher import load_saved_digests
from globals import (Categories, 
                     Digest, 
                     DIGEST_DISPLAY_WIDTH)

class TitleStyle(Style):
    DEFAULT_STYLE = "bold underline"
    
    def __init__(self, link: str):
        super().__init__(bold=True,
                         underline=True,
                         link=link)

class Post(Panel):
    def __init__(self, 
                 digest: Digest,
                 width: int = DIGEST_DISPLAY_WIDTH):
        self._link = digest['url']
        self._digest_title: Text|str = Text(text=digest['title'],
                                            justify="center",
                                            style=TitleStyle(digest['url']))
        self._digest_description: Text|str = Text(digest['description'])
        
        super().__init__(self._format_text(self._digest_title, 
                                           self._digest_description),
                         width=width,
                         box=box.SIMPLE, 
                         padding=(0,0),
                         expand=False)
    
    @property
    def description(self): return self._digest_description
    
    @description.setter
    def description(self, new_desc: Text|str):
        self._digest_description = new_desc
        self._rebuild_text()        
    
    @property
    def digest_title(self): return self._digest_title
    
    @digest_title.setter
    def digest_title(self, new_title: Text|str):
        self._digest_title = new_title
        self._rebuild_text()
    
    @property
    def link(self): return self._link
    
    @link.setter
    def link(self, new_link: str):
        self._link = new_link
        self.digest_title.style = TitleStyle(new_link)
        self._rebuild_text()
    
    @staticmethod
    def _format_text(title: Text | str, 
                     description: Text | str) -> Text: 
        return Text.assemble(title,"\n",description,end="")
    
    def _rebuild_text(self): self.renderable = self._format_text(self._digest_title, 
                                                                 self._digest_description) 
class CategoryHeader:
    def __init__(self, 
                 category: Categories, 
                 width: int = DIGEST_DISPLAY_WIDTH):
        self._category = category
        self.header_text = self.category_text
    
    @property
    def category_text(self) -> str:
        if self._category == Categories.CAREER:
            return "Professional Development"
        else:
            return self._category.value
    @property
    def category(self): return self._category
    
    @category.setter
    def category(self, new_category: Categories) -> None:
        self._category = new_category
        self.text = self.category_text
    
    @property
    def header_text(self): return self._header_text
    
    @header_text.setter
    def header_text(self, new_text: str):
        self._header_text = self.format_text(new_text)
        self.text = self._header_text
    
    @staticmethod
    def format_text(text: Text | str, 
                    width=DIGEST_DISPLAY_WIDTH):
        lines = ["".join(chunk) for chunk in batched(str(text), width)]
        last_line = lines[-1]
        margins = width - 2 - len(last_line)
        left_len = margins // 2
        formatted_last_line = f"{"─" * left_len} {last_line} {"─" * (margins - left_len)}"
        return "\n".join(lines[:-1] + [formatted_last_line])
    
    @property
    def renderable(self):
        return Text(self.header_text,
                    justify="center",
                    end="")
        
COLUMN_HEIGHT_TOLERANCE = 2



def main():
    console = Console()
    digests = load_saved_digests()
    checked_date = datetime.date.today()
    num_columns = console.width // DIGEST_DISPLAY_WIDTH
    
    while str(checked_date) not in digests.keys():
        checked_date -= datetime.timedelta(days=1)

    grid = Table(padding=(0,1),
                 box=box.HORIZONTALS,
                 show_header=False)
    grid.title = f"{checked_date} Daily Blast"
    [grid.add_column() for _ in range(num_columns)]

    printed_digests = digests[str(checked_date)]
    elements = []
    for category, digest_items in printed_digests.items():
        elements.append(CategoryHeader(Categories(category)).renderable)
        [elements.append(Post(item)) for item in digest_items]
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
    
if __name__ == "__main__":
    main()