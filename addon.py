# -*- coding: utf-8 -*-

from BeautifulSoup import SoupStrainer, BeautifulSoup as BS
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

DEBUG = False

__addon__ = xbmcaddon.Addon()
__plugin__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')

URL = 'http://www.openfilm.com'
RSS_URL = 'rss://www.openfilm.com/mrss/boxee/?&v=1&a=1'


class Main:
  def __init__(self):
    if ("action=categories" in sys.argv[2]):
      self.list_categories()
    elif ("action=sort" in sys.argv[2]):
      self.get_sort()
    else:
      self.main_menu()

  def main_menu(self):
    if DEBUG:
      self.log('main_menu()')
    folders = [{'title':"Editor's Picks", 'url':'rss://www.openfilm.com/mrss/boxee/?pid=1&s=-6'},
               {'title':'Most Popular', 'url':'rss://www.openfilm.com/mrss/boxee/?s=1'},
               {'title':'Most Recent', 'url':'rss://www.openfilm.com/mrss/boxee/?s=3'},
               {'title':'Categories', 'url':'%s?action=categories' % sys.argv[0]}]
    for i in folders:
      self.add_directory_item(i['title'], i['url'])
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def list_categories(self):
    if DEBUG:
      self.log('list_categories()')
    html = urllib.urlopen(URL).read()
    soup = BS(html, parseOnlyThese=SoupStrainer('ul', {'id': 'header_main_menu'}))
    for a in soup.li.div.ul.findAll('a'):
      title = a.string.replace('&amp;', '&')
      link = URL + a['href']
      parameters = '%s?action=sort&url=%s' % (sys.argv[0], urllib.quote_plus(link))
      self.add_directory_item(title, parameters)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def get_sort(self):
    if DEBUG:
      self.lOG('get_sort()')
    html = urllib.urlopen(self.arguments('url')).read()
    soup = BS(html, parseOnlyThese=SoupStrainer('ul', {'class': 'sortingMenu sortBlock'}))
    for li in soup('li'):
      title = li.a.string
      link = RSS_URL + li.a['href'].split('?')[1].replace('&amp;', '&')
      self.add_directory_item(title, link)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def add_directory_item(self, title, link):
    listitem = xbmcgui.ListItem(title, thumbnailImage=__icon__)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), link, listitem, True)

  def arguments(self, arg):
    _arguments = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
    return urllib.unquote_plus(_arguments[arg])

  def log(self, description):
    xbmc.log("[ADD-ON] '%s v%s': '%s'" % (__plugin__, __version__, description), xbmc.LOGNOTICE)

if __name__ == '__main__':
  Main()
