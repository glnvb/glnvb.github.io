# -*- coding: utf-8 -*-

import datetime
import glob
import os
import pytz
import re
import requests
import shlex
import slugify
import time
import yaml


class Track:
    re_number = re.compile(r'^([0-9]+) *\. *(.+)')

    def __init__(self, json):
        self.title = json['title'].replace('"', "'")
        self.number = None

        m = Track.re_number.match(self.title)
        if m:
            self.number, self.title = m.groups()

        self.permalink = json['permalink_url']

        self.artwork = json['artwork_url'] or ""

        self.timestamp_utc = datetime.datetime.strptime(json['display_date'], '%Y-%m-%dT%H:%M:%SZ')
        self.timestamp_local = pytz.timezone('Europe/Brussels').fromutc(self.timestamp_utc)
        self.tags = shlex.split(json['tag_list'])

        desc = json['description']
        self.description = desc[:desc.find('.')+1].replace('"', "'")

        self.post = re.sub(r'(https?://[^ \n]+)', '[\g<1>](\g<1>)', desc)

        self.title_slug = slugify.slugify(self.title)


class SoundCloudAPI:
    def __init__(self, client_id):
        self.client_id = client_id
        self.session = requests.Session()

        self.app_version = self.__get_app_version()

    def __get_app_version(self):
        return self.session.get('https://soundcloud.com/versions.json').json()['app']

    def __get(self, url, params=None):
        r = self.session.get(url, params=params)
        while not r.content:
            r = self.session.get(url, params=params)
            time.sleep(1)
        r = r.json()
        while r == {}:
            r = self.__get(url, params)
        return r

    def get_tracks(self, user_id):
        result = []

        tracks = self.__get(
            f'https://api-v2.soundcloud.com/users/{user_id}/tracks', params={
                'client_id': self.client_id,
                'app_version': self.app_version,
                'app_locale': 'en',
                'linked_partitioning': 1,
                'offset': 0,
                'limit': 20
            })
        for t in tracks['collection']:
            result.append(Track(t))

        while tracks.get('next_href', None):
            tracks = self.__get(tracks['next_href'], params={
                'client_id': self.client_id,
                'app_version': self.app_version,
                'app_locale': 'en',
            })
            for t in tracks['collection']:
                result.append(Track(t))

        return result


class JekyllMarkdown:
    def __init__(self, filepath, filecontent=None):
        self.filepath = filepath
        self._filecontent = filecontent

        self.front_matter = None
        self.content = None
        self.__read()

    def __read(self):
        front_matter = ''
        content = ''

        if not self._filecontent:
            with open(self.filepath, 'r') as file:
                self._filecontent = file.readlines()
        else:
            self._filecontent = self._filecontent.splitlines()

        is_front_matter = False
        is_content = False

        for line in self._filecontent:
            if line.strip() == '---' and is_front_matter == False:
                is_front_matter = True
                continue
            elif line.strip() == '---':
                is_front_matter = False
                is_content = True
                continue

            if is_front_matter:
                front_matter += line + '\n'
            elif is_content:
                content += line + '\n'

        self.front_matter = yaml.safe_load(front_matter)
        self.content = content

    def write(self):
        with open(self.filepath, 'w') as file:
            file.write('---\n')
            file.write(yaml.dump(self.front_matter))
            file.write('---\n')
            file.write(self.content.strip())


class JekyllTags:
    def __init__(self, tag_dir):
        self.tag_dir = tag_dir
        self.tags = set()
        self.__parse_tags()

    def __parse_tags(self):
        for tag_file in glob.glob(f'{self.tag_dir}/*.markdown'):
            tag_md = JekyllMarkdown(tag_file)
            self.tags.add(tag_md.front_matter['tag-name'])

    def filter_track(self, track):
        """Filter the tags of the track and only keep the ones that exist in Jekyll.

        Parameters
        ----------
        track : Track
        """
        track.tags = [t for t in track.tags if t in self.tags]
        return track


class JekyllPosts:
    re_date = re.compile('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]')

    def __init__(self, post_dir, new_post_template, update_post_template):
        self.post_dir = post_dir
        if not os.path.exists(self.post_dir):
            os.makedirs(self.post_dir)

        self.new_post_template = new_post_template
        with open(self.new_post_template, 'r') as template_file:
            self.new_post_template = template_file.read()

        self.update_post_template = update_post_template
        with open(self.update_post_template, 'r') as template_file:
            self.update_post_template = template_file.read()

        self.unpublished_posts = {}
        self.__parse_posts()

    def __parse_posts(self):
        for post_file in glob.glob(f'{self.post_dir}/*.markdown'):
            if not JekyllPosts.re_date.match(os.path.basename(post_file)):
                post = JekyllMarkdown(post_file)
                soundcloud_track = post.front_matter.get('embed_player', {}).get('src', None)
                if soundcloud_track:
                    self.unpublished_posts[soundcloud_track] = post_file

    def write_track(self, track):
        filename = track.timestamp_local.strftime("%Y-%m-%d") + "-" + track.title_slug + ".markdown"
        filepath = os.path.join(self.post_dir, filename)

        if track.permalink in self.unpublished_posts:
            # update
            template = self.update_post_template.replace('%TITLE%', f'"{track.title}"')
            template = template.replace('%NUMBER%', track.number or 'null')
            template = template.replace('%ARTWORK_URL%', track.artwork)
            template = template.replace('%DATE%', track.timestamp_local.strftime("%Y-%m-%d %H:%M:%S %z"))
            template = template.replace('%PERMALINK%', track.permalink)

            updated_front_matter = JekyllMarkdown(None, template).front_matter
            existing_post = JekyllMarkdown(self.unpublished_posts[track.permalink])
            existing_post.front_matter.update(updated_front_matter)
            existing_post.write()
            os.rename(existing_post.filepath, filepath)

        elif not os.path.exists(filepath):
            # new
            template = self.new_post_template.replace('%TITLE%', f'"{track.title}"')
            template = template.replace('%NUMBER%', track.number or 'null')
            template = template.replace('%ARTWORK_URL%', track.artwork)
            template = template.replace('%DATE%', track.timestamp_local.strftime("%Y-%m-%d %H:%M:%S %z"))
            template = template.replace('%TAGS%', ", ".join([f'"{tag}"' for tag in track.tags]))
            template = template.replace('%PERMALINK%', track.permalink)
            template = template.replace('%DESCRIPTION%', f'"{track.description}"')
            template = template.replace('%POST%', track.post)
            with open(filepath, 'w') as f:
                f.write(template)


if __name__ == '__main__':
    new_post_template = os.path.join(os.path.dirname(__file__), 'new_post_template.markdown')
    update_post_template = os.path.join(os.path.dirname(__file__), 'update_post_template.markdown')
    post_dir = os.path.join(os.path.dirname(__file__), os.pardir, '_posts', 'podcast')
    tag_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'tags')

    client_id = os.environ['CLIENT_ID']
    user_id = os.environ['USER_ID']

    jekyll_tags = JekyllTags(tag_dir)
    jekyll_posts = JekyllPosts(post_dir, new_post_template, update_post_template)

    soundcloud_tracks = SoundCloudAPI(client_id).get_tracks(user_id)
    for track in soundcloud_tracks:
        jekyll_tags.filter_track(track)
        jekyll_posts.write_track(track)
