# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .domovita import DomovitaSpider
from .kufarJSON import KufarjsonSpider
from .neagent import NeagentSpider
from .onlinerJSON import OnlinerjsonSpider
from .realt import RealtSpider

__all__ = ['DomovitaSpider', 'KufarjsonSpider', 'NeagentSpider', 'OnlinerjsonSpider', 'RealtSpider']