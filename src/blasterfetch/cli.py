from .services import fetcher, filterer, parser, renderer
from .storage import DataManager

def app():
    data_manager = DataManager()
    digests = data_manager.load()
    renderer.render(digests)