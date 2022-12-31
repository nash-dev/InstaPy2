from .location import LocationHelper
from .people import PeopleHelper

from typing import Tuple

# Generic Helpers
def parse_args(**kwargs) -> Tuple[bool, bool, bool, bool]:
        keys = ['randomize_likes', 'randomize_media', 'randomize_tags', 'skip_top']
        defaults = {'randomize_likes' : False, 'randomize_media' : False, 'randomize_tags' : False, 'skip_top' : True}
        args = []
        for key in keys:
            args.append(kwargs[key]) if key in kwargs.keys() else args.append(defaults[key])
        return tuple(args)