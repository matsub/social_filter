# -*- coding: utf-8 -*-
__author__ = 'shamison'

from twitter import *
import configparser
import os
import sys
import re

import MeCab

# config.iniから読み込み. consumer_keyとかを諸々書いておく
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
oauth_config = config['oauth']

# ツイートやらプロフィールを取ってくるため作成
tw = Twitter(
    auth=OAuth(
        oauth_config['token'],
        oauth_config['token_secret'],
        oauth_config['consumer'],
        oauth_config['consumer_secret']
    )    
)


def yes_no_input():
    yes = re.compile("^y(e|es)?$", flags=re.IGNORECASE)
    no = re.compile("^(no?)?$", flags=re.IGNORECASE)

    while True:
        choice = input("are you sure to tweet this? [y/N]: ")
        if yes.match(choice):
            return True
        elif no.match(choice):
            return False
        print("couldn't understand: %s" % choice)


def tweet(tweet_str):
    tw_str = social_filter(tweet_str)[:120]
    print('TEXT:', tw_str)
    if yes_no_input():
        tw.statuses.update(status=tw_str+' #social_filter')


def convert(text_info):
    others = re.compile("^(助.?|副|記号)")
    noun = re.compile("^名詞")
    adj = re.compile("^形容詞")
    verb = re.compile("^動詞")

    for t in text_info:
        if t[0] == 'EOS':
            raise StopIteration

        if others.match(t[1]):
            yield t[0]
        elif noun.match(t[1]):
            yield "にゃん"
        elif adj.match(t[1]):
            yield "にゃ"
        elif verb.match(t[1]):
            yield "にゃーん"
        else:
            yield t


def social_filter(input_str):
    mt = MeCab.Tagger('mecabrc')
    text_info = map(lambda t: t.split("\t"),
            mt.parse(input_str).split("\n"))
    return ''.join(convert(text_info))

if __name__ == '__main__':
    tweet(sys.argv[1])
