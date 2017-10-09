"""
Configure the tests for sheepdog.

To set up an environment for testing, emulate the dictionary and models
required to initialize sheepdog using "fake" dictionary and models, which are
defined in ``tests/dictionary`` and ``tests/models``.
"""

import sheepdog

from tests.dictionary import dictionary
from tests.models import models


# Set up sheepdog to use the fake dictionary defined in ``tests/dictionary``,
# loading the schemas from ``tests/dictionary/schemas``.
sheepdog.dictionary.init(dictionary)

print(dir(models))

sheepdog.models.init(models)
