import feedparser
import requests
class RssFeed:
<<<<<<< HEAD
    news_entries = []
    def __init__(self, feeds):
        self.news_entries = []
        for feed in feeds:
            try:
                feed_news = feedparser.parse(feed["FeedUrl"])
                if feed_news.bozo == 1:
	                print("Bozo bit set. Malformed XML received.")
                iter_range = 4
                if len(feed_news.entries) <= 5:
	                iter_range = len(feed_news.entries)
                title = feed_news['feed']['title']
                self.news_entries.append(title)
                for i in range(0, iter_range):
	                title = feed_news.entries[i].title
	                self.news_entries.append(title)
            except Exception as ex:
                print("Failed to parse uri to XML feed.")
                print("{0}".format(ex))

    def get_entries(self):
        feed_text = ""
        for entry in self.news_entries:
            if len(entry) > 20:
                new_entry = entry[:20] + '-\n' + entry[20:]
                feed_text += new_entry + '\n'
            else:			
                feed_text += entry + '\n'
        return feed_text
=======
	news_entries = []
	def __init__(self, feeds):
		self.news_entries = []
		for feed in feeds:
			try:
				feed_news = feedparser.parse(feed["FeedUrl"])
				if feed_news.bozo == 1:
					print("Bozo bit set. Malformed XML received.")
				iter_range = 4
				if len(feed_news.entries) <= 5:
					iter_range = len(feed_news.entries)
				title = feed_news['feed']['title']
				self.news_entries.append(title)
				for i in range(0, iter_range):
					title = feed_news.entries[i].title
					self.news_entries.append(title)
			except Exception as ex:
				print("Failed to parse uri to XML feed.")
				print("{0}".format(ex))
	
	def get_entries(self):
		feed_text = ""
		for entry in self.news_entries:
			feed_text += entry + '\n'
		return feed_text
>>>>>>> 94739632b643f65f3f2555f985998ab09cf446e7

