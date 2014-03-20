from zm import AutoReloader
from zm import Options as ZMOptions

AutoReloader(ZMOptions.get('zm_home'))

from zm import ZM
application = ZM().answerRequest

