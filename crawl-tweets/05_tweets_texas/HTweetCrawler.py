import sys
import os
import getopt
import logging
import codecs
from requests_oauthlib import OAuth1
import urllib
import requests
import simplejson
import time
import httplib
from calendar import timegm
import datetime
import re


class HTweetCrawler(object):
    'Crawling latest tweets of users'
    def __init__(self, argv):
        self.TWEETS_PER_CALL = 200
        self.INCLUDE_RTS = True
        self.EXCLUDE_REPLIES = False
        self._error_backoff = 10

        try:
            opts, args = getopt.getopt(argv, "hn:k:i:o:e:l:t:c:m:s:r:")
        except getopt.GetoptError:
            print "python HTweetCrawler.py -n <numeric_id> -k <keyfile> -i <inputfile> -o <outputfile> -e <errorfile> -l <logfile> -t <templatefile> -c <cursorfile> -m <max_tweets> -s <is_screenname> -r <rawjsonfile>"
            sys.exit()

        for opt, arg in opts:
            if opt == "-h":
                print "python HTweetCrawler.py -n <numeric_id> -k <keyfile> -i <inputfile> -o <outputfile> -e <errorfile> -l <logfile> -t <templatefile> -c <cursofrfile> -m <max_tweets> -s <is_screenname> -r <rawjsonfile>"
                sys.exit()
            elif opt == "-n":
                self.numeric_id = int(arg)
            elif opt == "-k":
                self.keyfile = arg
            elif opt == "-i":
                self.inputfile = arg
            elif opt == "-o":
                self.outputfile = arg
            elif opt == "-e":
                self.errorfile = arg
            elif opt == "-l":
                self.logfile = arg
            elif opt == "-t":
                self.templatefile = arg
            elif opt == "-c":
                self.cursorfile = arg
            elif opt == "-m":
                self.max_tweets = int(arg)
            elif opt == "-s":
                self.is_screenname = bool(arg)
            elif opt == "-r":
                self.rawjsonfile = arg
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=self.logfile,
                            filemode="w")
        self.logger = logging.getLogger(__name__)

        self.keys = []
        self.key_index = 0

        self.reset_times = []
        
        with open(self.keyfile) as fi:
            for line in fi:
                terms = [term.strip() for term in line.split()]
                consumer_key = terms[0]
                consumer_secret = terms[1]
                access_token_key = terms[2]
                access_token_secret = terms[3]
                self.keys.append((consumer_key, consumer_secret, access_token_key, access_token_secret))
                self.reset_times.append(self._current_epoch())
        self.logger.info("%d keys loaded" % len(self.keys))
        self._oauth()
        self._load_last_status()
        self._save_fields = []
        with open(self.templatefile) as fi:
            for line in fi:
                self._save_fields.append("status" + "".join([".get(\"%s\")" % term.strip() for term in line.split()]))
        self.logger.debug("save fields: " + str(self._save_fields))
        # sys.exit()

    def _current_epoch(self):
        return timegm(datetime.datetime.utcnow().timetuple())

    def _reset_time(self):
        return self.reset_times[self.key_index]

    def _save_reset_time(self, reset_time):
        self.reset_times[self.key_index] = reset_time

    def _oauth(self):
        key_info = self.keys[self.key_index]
        consumer_key = key_info[0]
        consumer_secret = key_info[1]
        access_token_key = key_info[2]
        access_token_secret = key_info[3]
        self._auth = OAuth1(consumer_key, consumer_secret,
                            access_token_key, access_token_secret)
        self.key_index = (self.key_index + 1) % len(self.keys)
        self.logger.info("OAuth authorization with [%s]" % access_token_key)

    def _load_last_status(self):
        if not os.path.exists(self.cursorfile):
            self.last_status = -1
        else:
            self.last_status = int(open(self.cursorfile).read())

    def _saveLastStatus(self, line_index):
        with open(self.cursorfile, "w") as fo:
            fo.write("%d" % line_index)

    def _getTweets(self, user_id=None, screen_name=None, max_id=0):
        parameters = {}
        target_url = "https://api.twitter.com/1.1/statuses/user_timeline.json?%s"
        if user_id:
            parameters["user_id"] = user_id
        else:
            parameters["screen_name"] = screen_name

        if max_id:
            parameters['max_id'] = max_id
        parameters["count"] = self.TWEETS_PER_CALL
        parameters["include_rts"] = self.INCLUDE_RTS
        parameters["exclude_replies"] = self.EXCLUDE_REPLIES
        self.logger.debug(urllib.urlencode(parameters))
        return requests.get(target_url % urllib.urlencode(parameters),
                            auth=self._auth)

    def _parseJson(self, content):
        return simplejson.loads(content)

    def _sleep(self):
        self.logger.info("sleep %d secs..." % self._error_backoff)
        time.sleep(self._error_backoff)
        self._error_backoff = self._error_backoff * 2

    def run(self):
        with open(self.inputfile) as fi, codecs.open(self.outputfile, "a", "utf-8") as fo, codecs.open(self.rawjsonfile, "a", "utf-8") as out_rawjson, open(self.errorfile, "a") as fe:
            for line_index, line in enumerate(fi):
                if self.last_status >= line_index:
                    continue
                to_crawl = line.strip()
                self.logger.info("[%d] index: %d, user: %s" % (self.numeric_id, line_index, to_crawl))
                last_min_id = 0
                crawled_statuses_count = 0
                while True:
                    try:
                        if self.is_screenname:
                            response = self._getTweets(screen_name=to_crawl, max_id=last_min_id)
                        else:
                            response = self._getTweets(user_id=to_crawl, max_id=last_min_id)
                    except Exception as e:
                        self.logger.error("request err", exc_info=True)
                        self._sleep()
                        continue

                    self.logger.debug("HTTP status code [%d]" % response.status_code)
                    if response.status_code == httplib.OK:
                        self._error_backoff = 10
                    else:
                        if response.status_code == httplib.UNAUTHORIZED:
                            # tweets are protected
                            fe.write("%s\tProtected account\n" % (to_crawl))
                            self.logger.error("[%s] is a protected account" % to_crawl)
                            break
                        elif response.status_code == httplib.NOT_FOUND:
                            fe.write("%s\tDeleted account\n" % (to_crawl))
                            self.logger.error("[%s] is a deleted account" % to_crawl)
                            break
                        elif response.status_code == 429:   # Twitter's own code
                            self.logger.error("Too many requests [%d]" % self.key_index)
                            self._save_reset_time(int(response.headers["x-rate-limit-reset"]))
                            self._oauth()
                            if self._reset_time() >= self._current_epoch():
                                delta = self._reset_time() - int(self._current_epoch())
                                self.logger.info("sleep %d secs based on reset time" % delta)
                                time.sleep(delta + 5)   # buffer
                            continue
                        elif (response.status_code == httplib.SERVICE_UNAVAILABLE or
                              response.status_code == httplib.INTERNAL_SERVER_ERROR):   # Twitter's server-side error
                            self.logger.error("Twitter's Error [%d]" % response.status_code)
                            self._sleep()
                            continue
                        else:   # Error codes that we don't know yet
                            self.logger.error("%s\t%d\n" % (to_crawl, response.status_code))
                            self._sleep()
                            continue

                    if "x-rate-limit-remaining" in response.headers:
                        self.logger.info("remaining requests: %s" % str(response.headers["x-rate-limit-remaining"]))

                    try:
                        rawjson = self._parseJson(response.content)
                        out_rawjson.write(str(rawjson))
                        out_rawjson.write("\n")
                    except simplejson.JSONDecodeError as jde:
                        # rarely happens
                        self.logger.error("json parse errors", exc_info=True)
                        self._sleep()
                        continue

                    if not rawjson or len(rawjson) == 1:
                        break
                    for status in rawjson:
                        result = []
                        for parse_command in self._save_fields:
                            try:
                                result.append(" ".join(unicode(eval(parse_command)).splitlines()))
                            except AttributeError as ae:
                                # no field exists
                                result.append("None")
                        fo.write("\t".join(result) + "\n")
                    crawled_statuses_count += len(rawjson)
                    last_min_id = rawjson[-1]["id"]
                    self.logger.info("[%d-%d] %s's %s tweets crawled until [%d] created at %s" % (self.numeric_id, line_index, to_crawl, len(rawjson), last_min_id, rawjson[-1]["created_at"]))
                    if crawled_statuses_count >= self.max_tweets:
                        break

                self._saveLastStatus(line_index)

if __name__ == "__main__":
    htc = HTweetCrawler(sys.argv[1:])
    htc.run()