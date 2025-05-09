from util.graphics import NotesApp
import logging

from util.logging import setup_logging

#logging
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Launching NotesApp")



if __name__ == "__main__":    
    app = NotesApp()
    app.run()