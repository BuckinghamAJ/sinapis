from pathlib import Path
from profanity.extras import ProfanityFilter
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger('app')
import os

word_list = Path(os.path.abspath(os.path.dirname(__file__)), 'config', 'wordlist.txt')
censor_list = None
with open(word_list, 'r') as f:
    censor_list = [line.strip() for line in f.readlines()]

pf = ProfanityFilter(custom_censor_list=censor_list)

class SeedProfanityFilter(ProfanityFilter):
    def __init__(self, word_list: Path = None, **kwargs):
        super().__init__(**kwargs)
        self._words_file = word_list if word_list else self._words_file



spf = SeedProfanityFilter(word_list=Path(os.path.abspath(os.path.dirname(__file__)), 'config', 'wordlist.txt'))


def validate_is_profane(value):
    if pf.is_profane(value) is True:
        bad_words = pf.get_profane_words()
        logger.debug(bad_words)
        logger.debug(pf.censor(value))
        raise ValidationError('Please remove any profanity/swear words.')
