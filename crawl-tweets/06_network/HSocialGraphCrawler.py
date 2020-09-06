#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import getopt
import logging
import codecs
from requests_oauthlib import OAuth1
import urllib
import requests
import time
import httplib
from calendar import timegm
from datetime import datetime
import re
import json


class HSocialGraphCrawler(object):
    """Crawling Followers/Followees of users"""

    def __init__(self):
        self.numeric_id = int(sys.argv[1])

        with open("config.json") as fi:
            self.config = json.loads(fi.read())

        self.records_per_call = self.config["records_per_call"]
        self.default_error_backoff = self.config["error_backoff"]
        self.error_backoff = self.default_error_backoff
        self.proxy_file = "%s/%s.%.2d" % (self.config["proxy_dir"], 
            os.path.basename(self.config["proxy_file"]), self.numeric_id)
        self.key_file = "%s/%s.%.2d" % (self.config["key_dir"], 
            os.path.basename(self.config["key_file"]), self.numeric_id)
        self.input_file = "%s/%s.%.2d" % (self.config["input_dir"], 
            os.path.basename(self.config["input_file"]), self.numeric_id)
        self.output_file = "%s/%s.%s.%.2d" % (self.config["output_dir"], 
            self.config["output_file_prefix"], 
            datetime.utcnow().isoformat().replace("-", "").replace(":", "").split(".")[0], 
            self.numeric_id)
        self.error_file = "%s/%s.%.2d" % (self.config["error_dir"], 
            self.config["error_file_prefix"], self.numeric_id)
        self.log_file = "%s/%s.%.2d" % (self.config["log_dir"], 
            self.config["log_file_prefix"], self.numeric_id)
        self.cursor_file = "%s/%s.%.2d" % (self.config["cursor_dir"], 
            self.config["cursor_file_prefix"], self.numeric_id)
        self.is_screen_name = self.config["is_screen_name"]
        logging.basicConfig(level=self.config["log_level"],
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=self.log_file,
                            filemode="w")
        self.logger = logging.getLogger(__name__)
        self.keys = []
        self.key_index = 0
        self.reset_times = []
        self.proxies = {}

        with open(self.proxy_file) as fi:
            for line in fi:
                terms = [term.strip() for term in line.split(":")]
                ip = terms[0]
                port = terms[1]
                login = terms[2]
                pwd = terms[3]
                proxy_url = 'https://%s:%s@%s:%s' % (login, pwd, ip, port)
                self.proxies["https"] = proxy_url
                # os.environ['http_proxy'] = proxy_url


        with open(self.key_file) as fi:
            for line in fi:
                terms = [term.strip() for term in line.split()]
                consumer_key = terms[0]
                consumer_secret = terms[1]
                access_token_key = terms[2]
                access_token_secret = terms[3]
                self.keys.append((consumer_key, consumer_secret, 
                    access_token_key, access_token_secret))
                self.reset_times.append(self._current_epoch())
        self.logger.info("%d keys loaded" % len(self.keys))
        self._oauth()
        self._load_last_status()

    def _current_epoch(self):
        return timegm(datetime.utcnow().timetuple())

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
        if not os.path.exists(self.cursor_file):
            self.last_status = -1
        else:
            self.last_status = int(open(self.cursor_file).read())

    def _save_last_status(self, line_index):
        with open(self.cursor_file, "w") as fo:
            fo.write("%d" % line_index)

    def _crawl(self, target_url, user_id=None, screen_name=None, cursor=-1):
        parameters = {}
        if user_id:
            parameters["user_id"] = user_id
        else:
            parameters["screen_name"] = screen_name

        parameters["count"] = self.records_per_call 
        parameters["cursor"] = cursor
        self.logger.debug(urllib.urlencode(parameters))

        return requests.get(target_url % urllib.urlencode(parameters), auth=self._auth, proxies=self.proxies, timeout = 10)

    def _get_social_graph(self, target_url, to_crawl, fo, fe):
        crawled_record_count = 0
        next_cursor = -1
        while True:

            self.logger.debug("START request")
            try:
                if self.is_screen_name:
                    response = self._crawl(target_url, screen_name=to_crawl, cursor=next_cursor)
                else:
                    response = self._crawl(target_url, user_id=to_crawl, cursor=next_cursor)
            except Exception as e:
                self.logger.error("request err", exc_info=True)
                self._sleep()
                continue
            self.logger.debug("END request")

            self.logger.debug("HTTP status code [%d]" % response.status_code)
            if response.status_code == httplib.OK:
                self.error_backoff = self.default_error_backoff
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
                    self._oauth() # proceed to the next key
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
                
            # self.logger.debug("response.content:" + response.content)
            try:
                rawjson = json.loads(response.content)
            except:
                # rarely happens
                self.logger.error("json parse errors", exc_info=True)
                self._sleep()
                continue

            if "followers" in target_url:
                fo.write("%s\t<-followers\t%s\n" % (to_crawl, str(rawjson["ids"])))
            else:
                fo.write("%s\tfollowing->\t%s\n" % (to_crawl, str(rawjson["ids"])))

            crawled_record_count += len(rawjson["ids"])
            next_cursor = rawjson["next_cursor"]
            if not next_cursor:
                self.logger.info("%d records of user [%s] are crawled..." % (crawled_record_count, to_crawl))
                break                               

    def _sleep(self):
        self.logger.info("sleep %d secs..." % self.error_backoff)
        time.sleep(self.error_backoff)
        self.error_backoff = self.error_backoff * 2

    def run(self):
        with open(self.input_file) as fi, codecs.open(self.output_file, "a", "utf-8") as fo, open(self.error_file, "a") as fe:
            for line_index, line in enumerate(fi):
                if self.last_status >= line_index:
                    continue
                to_crawl = line.strip()
                self.logger.info("[%d] index: %d, user: %s" % (self.numeric_id, line_index, to_crawl))
                if self.config["crawl_followers"]:
                    self._get_social_graph("https://api.twitter.com/1.1/followers/ids.json?%s", to_crawl, fo, fe)
                if self.config["crawl_followings"]:
                    self._get_social_graph("https://api.twitter.com/1.1/friends/ids.json?%s", to_crawl, fo, fe)

                self._save_last_status(line_index)
        self.logger.info("Crawling finished...")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Please use run.sh instead of directly running .py"
        exit()
    hsgc = HSocialGraphCrawler()
    hsgc.run()
