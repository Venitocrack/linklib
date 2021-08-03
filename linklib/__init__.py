"""
a link utils,WARNING:are not utils of a url-likelink,are links to link information,
path´s,or inclusive to link a global information for n sublinks
"""
from linklib.utils import LinkBase
from linklib.utils import loader
from linklib.utils import PathLink
from linklib.utils import path_loader
from linklib.utils import is_link
from linklib.utils import misc 
from linklib.connects import connected,ConnLink
from linklib.connects import n_connect as connect 
from linklib.connects import connect as _connect 
from linklib.connects import undefined
from linklib.utils import valid
from linklib.utils.misc import generator

class Link(LinkBase):
	pass

__version__ = '1.0.1'

__license__ = 'CC-BY'

__author__ = "Venitocrack"

__source__ = "github.com/Venitocrack/linklib"


