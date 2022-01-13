# -*- coding: utf-8 -*-

import os
import requests
import datetime
import pytz
import slugify
import shlex
import re
import time

user_id = 252268476
client_id = os.environ['CLIENT_ID']

session = requests.Session()

with open(os.path.join(os.path.dirname(__file__), 'post_template.markdown'), 'r') as template_file:
    template = template_file.read()

with open(os.path.join(os.path.dirname(__file__), 'tag_template.markdown'), 'r') as template_file:
    tag_template = template_file.read()

posts_dir = os.path.join(os.path.dirname(__file__), os.pardir, '_posts', 'podcast')
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

tag_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'tags')
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

app_version = session.get('https://soundcloud.com/versions.json').json()['app']


class Track:
    def __init__(self, json):
        self.title = json['title'].replace('"', "'")
        self.permalink = json['permalink_url']

        self.artwork = json['artwork_url'] or ""

        self.timestamp_utc = datetime.datetime.strptime(json['display_date'], '%Y-%m-%dT%H:%M:%SZ')
        self.timestamp_local = pytz.timezone('Europe/Brussels').fromutc(self.timestamp_utc)
        self.tags = shlex.split(json['tag_list'])

        desc = json['description']
        self.description = desc[:desc.find('.')+1].replace('"', "'")

        self.post = re.sub(r'(https?://[^ \n]+)', '[\g<1>](\g<1>)', desc)

        self.title_slug = slugify.slugify(self.title)

    def to_markdown(self, template):
        filename = self.timestamp_local.strftime("%Y-%m-%d") + "-" + self.title_slug + ".markdown"

        template = template.replace('%TITLE%', f'"{self.title}"')
        template = template.replace('%ARTWORK_URL%', self.artwork)
        template = template.replace('%DATE%', self.timestamp_local.strftime("%Y-%m-%d %H:%M:%S %z"))
        template = template.replace('%TAGS%', ", ".join([f'"{tag}"' for tag in self.tags]))
        template = template.replace('%PERMALINK%', self.permalink)
        template = template.replace('%DESCRIPTION%', f'"{self.description}"')
        template = template.replace('%POST%', self.post)
        return filename, template


class TrackCollection:
    def __init__(self):
        self.all_tags = {}
        self.tracks = []

        self.tag_blocklist = ["geschiedenis", "podcast"]
        self.tag_mincount = 2

    def add_track(self, track):
        self.tracks.append(track)
        for tag in track.tags:
            if tag.lower() not in self.all_tags:
                self.all_tags[tag.lower()] = [1, tag]
            else:
                self.all_tags[tag.lower()][0] += 1

    def tags_to_keep(self):
        tags_to_keep = []
        for tag, data in self.all_tags.items():
            count, orig_tag = data
            if count >= self.tag_mincount:
                tags_to_keep.append(tag)

        return [t for t in tags_to_keep if t not in self.tag_blocklist]

    def clean_tags(self):
        tags_to_keep = self.tags_to_keep()
        for track in self.tracks:
            track.tags = [t for t in track.tags if t.lower() in tags_to_keep]

    def to_markdown(self, template):
        self.clean_tags()

        for t in self.tracks:
            filename, content = t.to_markdown(template)
            filename = os.path.join(posts_dir, filename)
            if not os.path.exists(filename):
                with open(filename, 'w') as post_file:
                    post_file.write(content)

    def to_tags(self, template):
        tags_to_keep = self.tags_to_keep()
        for t in [t for t in self.all_tags if t in tags_to_keep]:
            slug = slugify.slugify(t)
            filename = os.path.join(tag_dir, slug + '.markdown')
            content = template.replace('%TAGNAME%', self.all_tags[t][1])
            if not os.path.exists(filename):
                with open(filename, 'w') as tag_file:
                    tag_file.write(content)


def get(url, params=None):
    r = session.get(url, params=params)
    while not r.content:
        r = session.get(url, params=params)
        time.sleep(1)
    print(r.content)
    r = r.json()
    while r == {}:
        r = get(url, params)
    return r


def parse_tracks(collection, tracks):
    for t in tracks:
        track = Track(t)
        collection.add_track(track)


collection = TrackCollection()

tracks = get(f'https://api-v2.soundcloud.com/users/{user_id}/tracks', params={
    'client_id': client_id,
    'app_version': app_version,
    'app_locale': 'en',
    'linked_partitioning': 1,
    'offset': 0,
    'limit': 20
})
parse_tracks(collection, tracks['collection'])

while tracks.get('next_href', None):
    tracks = get(tracks['next_href'], params={
        'client_id': client_id,
        'app_version': app_version,
        'app_locale': 'en',
    })
    parse_tracks(collection, tracks['collection'])

collection.to_markdown(template)
collection.to_tags(tag_template)
