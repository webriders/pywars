from common import *
from heroku import *

import os

if os.environ.get('DEPLOYMENT_SERVER') == 'heroku':
    from heroku import *
else:
    try:
        from local import *
    except ImportError:
        print "Please, provide your local configuration for this project.\n" \
              "See conf/settings/samples/ for more details"
        import sys
        sys.exit(1)