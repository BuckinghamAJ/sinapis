from pathlib import Path
from profanity.extras import ProfanityFilter
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger('app')

pf = ProfanityFilter()

class SeedProfanityFilter(ProfanityFilter):
    def __init__(self, word_list: Path = None, **kwargs):
        super().__init__(**kwargs)
        self._words_file = word_list if word_list else self._words_file

spf = SeedProfanityFilter(word_list=Path(Path(__file__).parent, 'config', 'wordlist.txt'))

def validate_is_profane(value):
    if pf.is_profane(value) is True:
        logger.debug(spf.censor(value))
        raise ValidationError('Please remove any profanity/swear words.')