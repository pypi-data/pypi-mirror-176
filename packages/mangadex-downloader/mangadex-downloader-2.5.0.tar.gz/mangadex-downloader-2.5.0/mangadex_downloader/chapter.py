# MIT License

# Copyright (c) 2022 Rahman Yusuf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import queue
from pathvalidate import sanitize_filename

from .user import User
from .language import Language
from .fetcher import (
    get_bulk_chapters,
    get_chapter_images,
    get_chapter,
    get_all_chapters
)
from .network import Net, base_url
from .errors import ChapterNotFound, GroupNotFound, UserNotFound
from .group import Group
from .config import config, env
from .utils import convert_int_or_float
# from . import range as range_mod # range_mod stands for "range module"

log = logging.getLogger(__name__)

class ChapterImages:
    def __init__(
        self,
        chapter,
        start_page=None,
        end_page=None,
        _range=None,
    ) -> None:
        self.chap = chapter
        self.id = chapter.id
        self.data_saver = config.use_compressed_image
        self._images = []
        self._low_images = []
        self._data = None
        self._base_url = None
        self._hash = None
        self.start_page = start_page
        self.end_page = end_page
        self.range = _range
        self.force_https = config.force_https

        self.legacy_range = (start_page or end_page)
    
    def fetch(self):
        data = get_chapter_images(self.id, force_https=self.force_https)
        # Construct image url
        self._data = data
        self._base_url = data.get('baseUrl')
        self._hash = data['chapter']['hash']
        self._images = data['chapter']['data']
        self._low_images = data['chapter']['dataSaver']

    def _check_range_page_legacy(self, page, log_info):
        if self.start_page is not None:
            if not (page >= self.start_page):

                if log_info:
                    log.info("Ignoring page %s as \"start_page\" is %s" % (
                        page,
                        self.start_page
                    ))

                return False

        if self.end_page is not None:
            if not (page <= self.end_page):

                if log_info:
                    log.info("Ignoring page %s as \"end_page\" is %s" % (
                        page,
                        self.end_page
                    ))

                return False

        return True

    def _check_range_page(self, page, log_info):
        if self.legacy_range:
            return self._check_range_page_legacy(page, log_info)

        if self.range is not None and not self.range.check_page(self.chap, page):

            if log_info:
                log.info(f"Ignoring page {page}, because page {page} is in ignored list")

            return False
        
        return True

    def iter(self, log_info=False):
        if self._data is None:
            raise Exception("fetch() is not called")

        quality_mode = 'data-saver' if self.data_saver else 'data'
        images = self._low_images if self.data_saver else self._images

        page = 1
        for img in images:

            if not self._check_range_page(page, log_info):
                page += 1
                continue

            url = '{0}/{1}/{2}/{3}'.format(
                self._base_url,
                quality_mode,
                self._hash,
                img
            )

            yield page, url, img

            page += 1

class AggregateChapter:
    def __init__(self, data) -> None:
        self.id = data.get('id')
        self.chapter = data.get('chapter')
        self.others_id = data.get('others')

class Chapter:
    def __init__(
        self,
        _id=None,
        data=None,
        use_group_name=True,
        use_chapter_title=False
    ):
        if _id and data:
            raise ValueError("_id and data cannot be together")

        if data is None:
            data = get_chapter(_id)['data']

        self.id = data['id']
        self._attr = data['attributes']

        # Get scanlation groups and manga
        rels = data['relationships']

        groups = []
        manga_id = None
        user = None
        for rel in rels:
            rel_id = rel['id']
            rel_type = rel['type']
            if rel_type == 'scanlation_group':
                groups.append(Group(data=rel))
            elif rel_type == 'manga':
                manga_id = rel_id
            elif rel_type == 'user':
                user = User(data=rel)
        
        if manga_id is None:
            raise RuntimeError(f"chapter {_id} has no manga relationship")

        self.user = user
        self.groups = groups
        self.groups_id = [group.id for group in groups]
        self.manga_id = manga_id
        self._name = None
        self._simpl_name = None
        self.oneshot = False
        self.use_group_name = use_group_name
        self.use_chapter_title = use_chapter_title

        self._lang = Language(self._attr['translatedLanguage'])

        self._parse_name()

    @property
    def volume(self):
        vol = self._attr['volume']
        if vol is not None:
            # As far as i know
            # Volume manga are integer numbers, not float
            try:
                return convert_int_or_float(vol)
            except ValueError:
                pass

            # Weird af volume name
            # Example: https://api.mangadex.org/manga/485a777b-e395-4ab1-b262-2a87f53e23c0/aggregate
            # (Take a look volume '3Cxx')
            return vol

        # No volume
        return vol

    @property
    def chapter(self):
        try:
            return self._attr['chapter'].strip()
        except AttributeError:
            # null value
            return None

    @property
    def title(self):
        return self._attr['title']

    @property
    def pages(self):
        return self._attr['pages']

    @property
    def language(self):
        return self._lang

    def _parse_name(self):
        name = ""
        simpl_name = ""

        if self.title is None:
            lower_title = ""
        else:
            lower_title = self.title.lower()

        if 'oneshot' in lower_title:
            self.oneshot = True
            if self.chapter is not None:
                name += f'Chapter. {self.chapter} '
                simpl_name += f"Ch. {self.chapter} "

            name += 'Oneshot'
            simpl_name += 'Oneshot'
        else:
            # Get combined volume and chapter
            if self.volume is not None:
                name += f'Volume. {self.volume} '
                simpl_name += f"Vol. {self.volume} "

            name += f'Chapter. {self.chapter}'
            simpl_name += f"Ch. {self.chapter}"

        self._name = name.strip()
        self._simpl_name = simpl_name.strip()

    @property
    def name(self):
        """This will return chapter name only"""
        return self._name

    @property
    def simple_name(self):
        """Return simplified chapter name"""
        return self._simpl_name

    def _make_name(self, chap_name):
        name = ""

        if self.use_group_name:
            name += f'[{sanitize_filename(self.groups_name)}] '

        name += chap_name

        # Chapter title
        if self.title and self.use_chapter_title:
            name += f' - {sanitize_filename(self.title)}'
        
        return name

    def get_name(self):
        """This will return chapter name with group name and title"""
        return self._make_name(self._name)

    def get_simplified_name(self):
        """Return simplified name of :meth:`Chapter.get_name()`"""
        return self._make_name(self._simpl_name)

    @property
    def groups_name(self):
        if not self.groups:
            return f'User - {self.user.name}'

        groups = self.groups.copy()

        first_group = groups.pop(0)
        name = first_group.name

        for group in groups:
            name += f' & {group.name}'

        return name

def iter_chapters_feed(manga_id, lang):
    includes = [
        'scanlation_group',
        'user'
    ]
    content_ratings = [
        'safe',
        'suggestive',
        'erotica',
        'pornographic'
    ]
    offset = 0
    limit = 500
    
    while True:
        params = {
            'includes[]': includes,
            'contentRating[]': content_ratings,
            'limit': limit,
            'offset': offset,
            'order[volume]': 'desc',
            'order[chapter]': 'desc',
            'translatedLanguage[]': [lang]
        }
        r = Net.mangadex.get(f'{base_url}/manga/{manga_id}/feed', params=params)
        d = r.json()

        items = d['data']

        if not items:
            break

        for item in items:
            yield item
        
        offset += len(items)

class IteratorChapter:
    def __init__(
        self,
        volumes,
        manga,
        lang,
        start_chapter=None,
        end_chapter=None,
        start_page=None,
        end_page=None,
        no_oneshot=None,
        group=None,
        _range=None,
        **kwargs
    ):

        legacy_range = (
            start_chapter or
            end_chapter or
            start_page or
            end_page or
            no_oneshot
        )

        if _range and legacy_range:
            raise ValueError("_range and (start_* or end_* or no_oneshot) cannot be together")

        self.volumes = volumes
        self.manga = manga
        self.language = lang
        self.queue = queue.Queue()
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        self.start_page = start_page
        self.end_page = end_page
        self.no_oneshot = no_oneshot
        self.no_group_name = config.no_group_name
        self.use_chapter_title = config.use_chapter_title
        self.group = None
        self.all_group = False
        self.legacy_range = legacy_range
        
        if _range is not None:
            # self.range = range_mod.compile(_range)
            self.range = None
        else:
            self.range = _range

        if group and group == "all":
            self.all_group = True
        elif group:
            self.group = self._parse_group(group)

        log_cache = kwargs.get('log_cache')
        self.log_cache = True if log_cache else False

        self._fill_data()

    def _parse_group(self, _id):
        group = None

        try:
            group = Group(_id)
        except GroupNotFound:
            # It's not a group
            pass

        # Check if it's a user
        try:
            group = User(_id)
        except UserNotFound:
            # It's not a user
            pass

        # It's not a group or user
        # raise error
        if group is None:
            raise GroupNotFound(f"Group or user \"{_id}\" cannot be found")
        
        return group

    def _check_range_chapter_legacy(self, chap):
        num_chap = chap.chapter
        if num_chap != 'none':
            try:
                num_chap = float(num_chap)
            except ValueError:
                pass
            except TypeError:
                # null value
                pass

        is_number = isinstance(num_chap, float)

        # There is a chance that "Chapter 0" is Oneshot or prologue
        # We need to verify that is valid oneshot chapter
        # if it's valid oneshot chapter
        # then we need to skip start_chapter and end_chapter checking
        if is_number and num_chap > 0.0:
            if self.start_chapter is not None and not (num_chap >= self.start_chapter):
                log.info(f"Ignoring chapter {num_chap}, because chapter {num_chap} is in ignored list")
                return False

            if self.end_chapter is not None and not (num_chap <= self.end_chapter):
                log.info(f"Ignoring chapter {num_chap}, because chapter {num_chap} is in ignored list")
                return False

        if chap.oneshot and self.no_oneshot and not self.all_group:
            log.info("Ignoring oneshot chapter since it's in ignored list")
            return False

        # If chapter 0 is prologue or whatever and not oneshot
        # Re-check start_chapter
        elif not chap.oneshot and is_number:
            if self.start_chapter is not None and not (num_chap >= self.start_chapter):
                log.info(f"Ignoring chapter {num_chap}, because chapter {num_chap} is in ignored list")
                return False

        return True

    def _check_range_chapter(self, chap):
        if self.legacy_range:
            return self._check_range_chapter_legacy(chap)
        
        if self.range is not None and not self.range.check_chapter(chap):
            log.info(f"Ignoring chapter {chap.chapter}, because chapter {chap.chapter} is in ignored list")
            return False

        return True

    def _check_chapter(self, chap):
        num_chap = chap.chapter

        # Some manga has chapters where it has no pages / images inside of it.
        # We need to verify it, to prevent error when downloading the manga.
        if chap.pages == 0:
            log.warning("Chapter {0} from group {1} has no images, ignoring...".format(
                chap.chapter,
                chap.groups_name
            ))
            return False

        if self.language == Language.Other and chap.language != Language.Other:
            return False

        if not self._check_range_chapter(chap):
            return False

        # Check blacklisted groups and users
        if chap.groups:
            for group in chap.groups:
                if group.id in env.group_blacklist:
                    log.info(
                        f"Ignoring chapter {chap.chapter}, " \
                        f"because group '{group.name}' is blacklisted"
                    )
                    return False

        if chap.user.id in env.user_blacklist:
            log.info(
                f"Ignoring chapter {chap.chapter}, " \
                f"because user '{chap.user.name}' is blacklisted"
            )
            return False

        # Check if it's same group as self.group
        if not self.all_group and self.group:
            group_check = True

            if isinstance(self.group, Group) and self.group.id not in chap.groups_id:
                group_type = 'scanlator group'
                group_names = chap.groups_name
                group_check = False
            
            elif isinstance(self.group, User) and self.group.id != chap.user.id:
                group_type = 'user'
                group_names = chap.user.name
                group_check = False
            
            if not group_check:
                log.info(
                    f"Ignoring chapter {num_chap}, " \
                    f"{group_type} \"{group_names}\" is not match with \"{self.group.name}\""
                )
                return False

        return True

    def _get_next_chapter(self):
        # Get chapter
        try:
            chap = self.queue.get_nowait()
        except queue.Empty:
            raise StopIteration()

        return chap

    def __iter__(self) -> "IteratorChapter":
        return self

    def __next__(self):
        while True:
            chap = self._get_next_chapter()

            if self.log_cache:
                log.debug(f'Caching Volume. {chap.volume} Chapter. {chap.chapter}')

            if not self._check_chapter(chap):
                continue

            chap_images = ChapterImages(
                chap,
                self.start_page,
                self.end_page,
                self.range,
            )

            return chap, chap_images

    def _get_chapter(self, _id, bulk_data):
        for data in bulk_data:
            if _id == data['id']:
                return Chapter(
                    data=data,
                    use_group_name=not self.no_group_name,
                    use_chapter_title=self.use_chapter_title
                )

    def _fill_data(self):
        chapters_data = {}
        for data in iter_chapters_feed(self.manga.id, self.language.value):
            chapters_data[data['id']] = data
        
        chap_others = []
        for _, chapters in self.volumes.items():
            for chapter in chapters:
                chap_others.append(chapter.id)

                if chapter.others_id and (
                    self.all_group or 
                    self.group or
                    self.language == Language.Other
                ):
                    chap_others.extend(chapter.others_id)

        # Sometimes chapters returned from /manga/{id}/feed are less than
        # /manga/{id}/aggregate
        missing_chapters = []
        for ag_chap in chap_others:
            try:
                chapters_data[ag_chap]
            except KeyError:
                missing_chapters.append(ag_chap)

        # Get the missing chapters
        limit = 100
        while missing_chapters:
            ids = missing_chapters[:limit]
            del missing_chapters[:limit]
            items = get_bulk_chapters(ids)['data']

            for item in items:
                chapters_data[item['id']] = item

        # Begin parsing
        chapters = []
        for ag_chap in chap_others:
            data = chapters_data[ag_chap]

            chap = Chapter(
                data=data,
                use_group_name=not self.no_group_name,
                use_chapter_title=self.use_chapter_title
            )

            chapters.append(chap)

        def sort_chapter(c):
            try:
                return convert_int_or_float(c.chapter)
            except ValueError:
                return float('nan')

        if config.sort_by == 'chapter':
            chapters = sorted(chapters, key=sort_chapter)
        
        for chap in chapters:
            self.queue.put(chap)

class MangaChapter:
    def __init__(self, manga, lang, chapter=None, all_chapters=False):
        if chapter and all_chapters:
            raise ValueError("chapter and all_chapters cannot be together")
        elif chapter is None and not all_chapters:
            raise ValueError("at least provide chapter or set all_chapters to True")

        self._volumes = {}
        self.language = Language(lang)
        self.manga = manga

        if chapter:
            self._parse_volumes_from_chapter(chapter)
        elif all_chapters:
            self._parse_volumes(get_all_chapters(manga.id, self.language.value))

    def iter(self, *args, **kwargs):
        return IteratorChapter(
            self._volumes,
            self.manga,
            self.language,
            *args,
            **kwargs
        )

    def _parse_volumes_from_chapter(self, chapter):
        if not isinstance(chapter, Chapter):
            chap = Chapter(chapter)
        else:
            chap = chapter

        # "api.mangadex.org/{manga-id}/aggregate" data for self._parse_volumes
        aggregate_data = {
            "volumes": {
                str(chap.volume): {
                    "volume": chap.volume,
                    "chapters": {
                        chap.chapter: {
                            "chapter": chap.chapter,
                            "id": chap.id
                        }
                    }
                }
            }
        }

        self._parse_volumes(aggregate_data)

    def _parse_volumes(self, json_data):
        data = json_data.get('volumes')

        # if translated language is not found in selected manga
        # raise error
        if not data:
            raise ChapterNotFound("Manga \"%s\" with %s language has no chapters" % (
                self.manga.title,
                self.language.name
            ))

        # Sorting volumes
        volumes = []

        # Sometimes volumes are in list not in dict
        # wtf
        # Reference: https://api.mangadex.org/manga/d667637e-9e6d-4c5a-89c4-0faba6f96338/aggregate?translatedLanguage[]=en
        if isinstance(data, list):
            for info in data:
                num = info['volume']
                volumes.append(num)
        else:
            for num in data.keys():
                volumes.append(num)

        # Again, sorting issue if manga volumes contain weird name
        # Reference: https://api.mangadex.org/manga/485a777b-e395-4ab1-b262-2a87f53e23c0/aggregate
        # (Take a look volume '3Cxx')
        # We need to sorting numbers first and then the others
        vol_nums = []
        vol_others = []

        for vol in volumes:
            try:
                convert_int_or_float(vol)
            except ValueError:
                vol_others.append(vol)
            else:
                vol_nums.append(vol)

        volumes = vol_nums
        # others volume didn't sorted when combined with numbers volume
        # we need to sort it first and then combined it
        volumes.extend(sorted(vol_others))

        def int_or_nan(val):
            try:
                return int(val)
            except ValueError:
                return float('nan')

        # In v2.0.2 or lower, sorting volumes for manga with leading zeros volumes (ex: 00, 01)
        # is failing. Because the app is converting these string numbers to integer numbers.
        # Which is causing the leading zero numbers is removed (ex: 00 -> 0, 01 -> 1)
        # Reference: https://api.mangadex.org/manga/1784f612-9a81-4ed6-a596-ef3e2d2e814f/aggregate?translatedLanguage[]=en
        volumes = sorted(volumes, key=int_or_nan)
        if volumes[0] == 'none':
            # None volume in beginning of array
            # may caused problem highest chapters get downloaded first
            volumes.append(volumes[0])
            volumes.pop(0)

        for volume in volumes:

            chapters = []

            # As far as i know, if volumes are in list, the list only have 1 data
            if isinstance(data, list):
                value = data[0]
            else:
                value = data[str(volume)]

            # Retrieving chapters
            c = value.get('chapters')

            def append_chapters(value):
                chap = AggregateChapter(value)
                chapters.append(chap)

            # Sometimes chapters are in list not in dict
            # I don't know why
            # Reference: https://api.mangadex.org/manga/433e77d2-5a58-48a3-95b8-e3c02f309255/aggregate?translatedLanguage[]=en
            if isinstance(c, list):
                for value in c:
                    append_chapters(value)
            else:
                for value in c.values():
                    append_chapters(value)

            chapters.reverse()
            self._volumes[volume] = chapters
