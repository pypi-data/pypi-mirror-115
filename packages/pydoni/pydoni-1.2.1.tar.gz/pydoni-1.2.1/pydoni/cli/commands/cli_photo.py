from posixpath import expanduser
import click
import datetime
import os
import pandas as pd
import pydoni
import random
import re
from .common import Verbose
from .photo.workflow.workflow import workflow
from send2trash import send2trash
from tabulate import tabulate
from tqdm import tqdm


def define_hashtags():
    return {
        'austin': [
            'atx',
            'atxlife',
            'atxphotography',
            'austin',
            'austinphotography',
            'austintexasthings',
            'do512',
            'exploreaustin',
            'igaustin',
            'igaustintexas',
            'igtexas',
            'iloveaustin',
            'instagramtexas',
            'onlyinaustin',
            'texas',
            'texasmonthly',
            'texasphotographer',
            'texastodo',
            'traveltexas',
            'trueaustin',
            'truetexas',
            'visitaustin',
            'yestexas',
            'trueaustin',
            'onlyinaustin',
            'truetexas',
            'igaustintexas',
            '365thingsaustin',
            'austinchronicle',
            'austin_monthly',
            'do512',
            'igtexas',
            'atxtown',
        ],

        'sf': [
            'bayarea',
            'bayshooters',
            'ilovesf',
            'onlyinsf',
            'sanfranciscobay',
            'sanfranciscobayarea',
            'sanfranciscobound',
            'sanfranciscolife',
            'sanfranciscoliving',
            'sf',
            'sfbayarea',
            'sflife'
        ],

        'sony': [
            'sony',
            'sonya7rii',
            'sonyalpha'
        ],

        'landscape': [
            'artofvisuals',
            'beautifuldestinations',
            'depthsofearth',
            'earthfocus',
            'earthofficial',
            'earthpix',
            'ig_escaype',
            'photooftheday',
            'roamtheplanet',
            'travelphotography',
            'visualsoflife',
            'visualtraveler',
        ],

        'long': [
            'longexposure',
            'longexposurephotography',
        ],

        'night': [
            'nightshooters',
            'nightphotography',
        ],

        'dji': [
            'aerial',
            'aerialphotography',
            'dji',
            'djiglobal',
            'drone',
            'droneglobe',
            'droneshots',
            'cloudchasers',
            'newaesthetic',
            'skypixel',
            'djimavicpro',
            'djiphotography',
            'djicreator',
            'dronephotography',
        ]
    }


@click.option('--austin', is_flag=True, default=False,
              help="Enable hashtags in group 'austin'.")
@click.option('--sf', is_flag=True, default=False,
              help="Enable hashtags in group 'sf'.")
@click.option('--sony', is_flag=True, default=False,
              help="Enable hashtags in group 'sony'.")
@click.option('--landscape', is_flag=True, default=False,
              help="Enable hashtags in group 'landscape'.")
@click.option('--long', is_flag=True, default=False,
              help="Enable hashtags in group 'long'.")
@click.option('--night', is_flag=True, default=False,
              help="Enable hashtags in group 'night'.")
@click.option('--dji', is_flag=True, default=False,
              help="Enable hashtags in group 'dji'.")
@click.option('--limit', type=int, default=28,
              help='Maximum number of keywords to return.')
@click.command()
def instagram_hashtags(austin, sf, sony, landscape, long, night, dji, limit=28):
    """
    Create Instagram hashtag comment string given lists of instagram keywords. Allow user
    to choose which keyword groups to use, and to set a limit on the number of hashtags
    returned. Then generate a comment string from those selected keywords.
    """
    params = locals()
    options = {k: v for k, v in params.items() if k not in ['limit']}

    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    if sum([v for k, v in options.items()]) == 0:
        raise Exception('Must select at least one option! Possibilities: {}'.format(
                [k for k, v in options.items()]))

    hashtags = define_hashtags()

    keyword_groups = list({k for k, v in params.items() if v is True})
    keywords = [v for k, v in hashtags.items() if k in keyword_groups]
    keywords = [item for sublist in keywords for item in sublist]
    random.shuffle(keywords)

    if limit < len(keywords):
        keywords = keywords[:limit]

    keywords = ['#' + x for x in keywords]

    spaces = []
    space_chars = ['·', '.', '-', '*', '~']
    for i in range(1, 6):
        spaces.append(''.join(random.choices(space_chars, k=1)) * i)

    keyword_string = '\n'.join(spaces) + '\n' + ' '.join(keywords)

    print('Here are your selected Instagram keywords:')
    print()
    print(keyword_string)

    result = {'keyword_groups': keyword_groups, 'keyword_string': keyword_string}
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='photo.instagram_hashtags'))


class Convention(object):
    """
    Store allowable media file convention regular expressions.
    """
    def __init__(self):
        self.photo = ''
        self.video = ''

        conv_base = '' +\
            r'(?P<year>\d{4})' +\
            r'(?P<month>\d{2})' +\
            r'(?P<day>\d{2})' +\
            '' +\
            r'(?P<hours>\d{2})' +\
            r'(?P<minutes>\d{2})' +\
            r'(?P<seconds>\d{2})' +\
            '' +\
            r'(?P<initials>[A-Za-z]{2,3})'

        self.photo = conv_base +\
            '_' +\
            r'(?P<camera>.*?)' +\
            '_' +\
            r'(?P<seqnum>(\d{4,}|\d+-\d|-\d|))' +\
            r'(?P<affix>(-HDR-*\d*|-Pano-*\d*|-Edit-*\d*|-Stack-*\d*|)*)' +\
            r'(?P<ext>\.[a-z0-9]{3})'

        self.video = conv_base +\
            '_' +\
            r'(?P<camera>.*?)' +\
            '_' +\
            r'(?P<seqnum>.*(\d+))' +\
            '_' +\
            r'(?P<quality>Q\d+(K|P))' +\
            r'(?P<fps>\d{2,3}FPS)' +\
            r'(?P<ext>\.[a-z0-9]{3})'


class Extension(object):
    """
    Store allowable file extension lists.
    """
    def __init__(self):
        self.photo = ['.jpg', '.jpeg', '.dng', '.arw', '.cr2']
        self.video = ['.mov', '.mp4', '.mts', '.m4v', '.avi']
        self.rm = ['.thm']


class MediaFile(Convention, Extension):
    """
    Gather information for a photo or video file.
    """
    def __init__(self, fpath):
        # Inherit naming conventions and extensions
        Convention.__init__(self)
        Extension.__init__(self)

        # Assign filename and directory name attributes to `self`
        self.fpath_abs = os.path.abspath(fpath)
        self.fname = os.path.basename(self.fpath_abs)
        self.dname = os.path.dirname(self.fpath_abs)
        assert self.fname != self.fpath_abs
        assert self.dname > ''

        # Define extensions
        self.ext = os.path.splitext(self.fname)[1].lower()
        self.valid_ext = Extension()

        # Parse media type from extension
        self.mtype = self.parse_media_type()
        self.remove_flag = True if self.mtype == 'remove' else False

        self.exif = pydoni.EXIF(self.fpath_abs).extract(clean_keys=True)


    def parse_media_type(self):
        """
        Given a file extension, get the type of media
        One of 'photo', 'video' or 'remove'
        """

        if self.ext in self.valid_ext.photo:
            return 'photo'
        elif self.ext in self.valid_ext.video:
            return 'video'
        elif self.ext in self.valid_ext.rm:
            return 'remove'
        else:
            e = "Invalid extension: '%s'" % self.ext
            raise Exception(e)

    def build_fname(self, initials, tz_adjust=0):
        """
        Build new filename from EXIF metadata.

        initials {str} two character initials string
        tz_adjust {int} alter 'hours' by set number to account for timezone adjust (default: {0})
        returns {str} new file basename according to convention
        """
        assert isinstance(initials, str)
        assert len(initials) in [2, 3]
        req_attrs = ['exif', 'mtype', 'dname', 'fname']
        for ra in req_attrs:
            assert hasattr(self, ra)
        assert self.mtype in ['photo', 'video']
        assert isinstance(tz_adjust, int)
        assert tz_adjust in range(-24, 24)

        def search_exif(exif, attrs, def_str):
            """
            Search exif dictionary for name attributes in the order specified. For example
            if `attrs` argument is ['image_width', 'video_size'], first search `exif` for
            the attribute 'image_width'. If it exists and is a valid value, return this
            value. If not, search for 'video_size' and return that value if it exists and
            is valid. If neither value exists, return an arbitrary string.

            attrs {str} or {list} attribute name(s) to search exif dictionary for
            def_str {str} return this string if attributes not found
            """
            assert isinstance(exif, dict)
            assert isinstance(attrs, str) or isinstance(attrs, list)
            assert isinstance(def_str, str)

            attrs = [attrs] if isinstance(attrs, str) else attrs
            bogus = ['0000:00:00 00:00:00']

            # `exif` is in format {FILENAME: {'exif_attr1': 'exif_val1', ...}}
            # Subset `exif` at FILENAME
            exif_items = exif[list(exif.keys())[0]]

            for attr in attrs:
                if attr in exif_items.keys():
                    val = exif_items[attr]
                    if val not in bogus:
                        return val

            return def_str

        def extract_video_quality(exif, def_str):
            """
            Given EXIF dictionary, extract video quality.

            exif {dict} EXIF dictionary
            def_str {str} return this string if value is not not found
            returns {str} video quality string
            """
            assert isinstance(exif, dict)
            assert isinstance(def_str, str)

            image_width = search_exif(
                exif=exif,
                attrs=['image_width', 'video_size'],
                def_str=def_str)

            if image_width == def_str:
                return def_str

            try:
                image_width_int = int(image_width)
                if image_width_int == 3840:
                    return '4K'
                elif image_width_int == 2704:
                    return '1520P'
                elif image_width_int == 1920:
                    return '1080P'
                elif image_width_int == 1280:
                    return '720P'
            except:
                pass

            return image_width

        def extract_video_framerate(exif, def_str):
            """
            Given EXIF dictionary, extract video frame rate.

            exif {dict} EXIF dictionary
            def_str {str} return this string if value is not not found
            returns {str} video framerate string
            """
            assert isinstance(exif, dict)
            assert isinstance(def_str, str)

            framerate = search_exif(
                exif    = exif,
                attrs=['video_avg_frame_rate', 'video_frame_rate'],
                def_str = def_str)

            if framerate == def_str:
                return def_str
            else:
                try:
                    return round(float(framerate))
                except:
                    return framerate

        def extract_capture_date_and_time(exif, def_str, mtype, tz_adjust=None):
            """
            Given EXIF dictionary, extract file capture date and time.

            exif {dict} EXIF dictionary
            def_str {str} return this string if value is not not found
            mtype {str} `MediaFile.mtype` (media type string)
            tz_adjust {int} alter 'hours' by set number to account for timezone adjust
            returns {tuple} (capture date string, capture time string)
            """

            assert isinstance(exif, dict)
            assert isinstance(def_str, str)
            assert mtype in ['photo', 'video']

            if mtype == 'photo':
                attrs = ['create_date', 'file_modify_date']
            elif mtype == 'video':
                attrs = ['file_modify_date', 'create_date']

            # Get capture date
            raw_dt = str(search_exif(exif=exif, attrs=attrs, def_str=def_str))
            capture_date = re.sub(r'(.*?)(\s+)(.*)', r'\1', raw_dt)
            capture_date = capture_date.replace(':', '').replace('-', '')

            # Get capture time
            capture_time = raw_dt.replace(':', '')
            capture_time = re.sub(r'(.*?)(\s+)(.*)', r'\3', capture_time)[0:6]

            # Adjust hours by timezone if specified. May also need to alter day if timezone
            # adjust makes the day spill over into the next/previous day
            if tz_adjust is not None and tz_adjust != 0:

                dt = datetime.datetime.strptime(capture_date + capture_time, '%Y%m%d%H%M%S')
                dt = dt + datetime.timedelta(hours=tz_adjust)
                capture_date = dt.strftime('%Y%m%d')
                capture_time = dt.strftime('%H%M%S')

            return (capture_date, capture_time)

        def extract_sequence_number(fname, def_str):
            """
            Given filename, extract file sequence number as the final occurrence of 4 or 5
            digits in a filename.

            fname {str} filename to extract sequence number from
            def_str {str} return this string if value is not not found
            returns {str} sequence number
            """



            assert isinstance(fname, str)
            assert isinstance(def_str, str)

            # Extract sequence number. Search first for 5 digits at the end of the filename.
            # If not found, search for 4 digits.

            # Clean up searchable area of filename by removing YYYYMMDDASHHMMSS and the string
            # for video files QXXXXFPS
            fname_ = os.path.basename(fname)
            fname_ = re.sub('_Q.*?FPS', '', fname_)
            fname_ = re.sub(r'^\d{8}\w{2}\d{6}_', '', fname_)

            # Search for 5 or 4 digits
            ptn = r'^(.*)(\d{5})(.*)$'
            if re.search(ptn, fname_):
                return re.sub(ptn, r'\2', fname_)
            else:
                ptn = r'^(.*)(\d{4})(.*)$'
                if re.search(ptn, fname_):
                    return re.sub(ptn, r'\2', fname_)
                else:
                    return def_str

        def extract_camera_model(exif, def_str, dname):
            """
            Given EXIF dictionary, extract camera model.

            exif {dict} EXIF dictionary
            def_str {str} return this string if value is not not found
            dname {str} directory name of photo, only used in parsing camera model if all else fails
            returns {str} camera model string
            """

            assert isinstance(exif, dict)
            assert isinstance(def_str, str)
            assert isinstance(dname, str)
            assert os.path.isdir(dname)

            # Get camera model from raw exif
            cm_raw = search_exif(
                exif=exif,
                attrs=['camera_model_name', 'device_model_name', 'model'],
                def_str=def_str
            )

            # If no camera model found, apply manual corrections
            if cm_raw == def_str:
                # Get make
                make_raw = search_exif(
                    exif=exif,
                    attrs=['make', 'device_manufacturer', 'compressor_name'],
                    def_str='{}'
                )

                make = make_raw
                valid_makes = ['Sony', 'Canon', 'DJI', 'Gopro', 'Gopro AVC Encoder', '{}']
                for vm in valid_makes:
                    if vm.lower() in make_raw.lower():
                        make = vm

                # Manual corrections
                if make.lower() == 'dji' or os.path.basename(dname).lower() == 'drone':
                    return 'L1D-20c'  # DJI Mavic 2 Pro
                elif make.lower() == 'gopro' or os.path.basename(dname).lower() == 'gopro':
                    return 'HERO5 Black'
                elif make != def_str:
                    return make
                else:
                    return def_str

            else:
                return cm_raw

        exif = self.exif
        fname = self.fname
        self.initials = initials

        # Default string to be returned by any of the extract* functions if that
        # attribute is unable to be found
        def_str = '{}'

        # Extract attributes from EXIF used regardless of photo or video
        self.cd, self.ct = extract_capture_date_and_time(exif, def_str, self.mtype, tz_adjust)
        self.sn = extract_sequence_number(fname, def_str)
        self.cm = extract_camera_model(exif, def_str, self.dname)

        # Build new filename
        if self.mtype == 'photo':
            newfname = "{}_{}_{}_{}_{}{}".format(
                self.cd, self.ct, self.initials, self.cm, self.sn, self.ext.lower())

        elif self.mtype == 'video':
            self.vq = extract_video_quality(exif, def_str)
            self.vfr = extract_video_framerate(exif, def_str)
            newfname = "{}_{}_{}_{}_{}_Q{}{}FPS{}".format(
                self.cd, self.ct, self.initials, self.cm, self.sn, self.vq, self.vfr, self.ext.lower())

        return newfname

    def convert_dng(self, remove_original=False):
        """
        Convert a photo file to dng.

        remove_original {bool}: if True, remove original raw file (default: {True})
        """
        assert self.ext in self.valid_ext.photo
        pydoni.adobe_dng_converter(self.fpath_abs)

        if remove_original:
            send2trash(self.fpath_abs)


def parse_media_type(file_ext, EXT):
    """
    Given a file extension, get the type of media
    One of 'photo', 'video' or 'remove'

    file_ext {str}: file extension to parse
    EXT {Extension}: Extension object
    type of media {str}
    """
    for attr_name in [x for x in dir(EXT) if not x.startswith('__')]:
        if file_ext in getattr(EXT, attr_name):
            return attr_name

    raise Exception(f'Invalid extension: {file_ext}')


@click.option('-f', '--fpath', required=True, type=click.Path(exists=True), multiple=True,
              help='Path or paths to file(s) to rename.')
@click.option('--initials', default=None, type=str, required=True,
              help='2 or 3 letter initials string.')
@click.option('--tz-adjust', default=0, type=int,
              help='Execute `pydoni.opsys.macos_notify()` on program completion.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print output to console.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def rename_mediafile(fpath, initials, tz_adjust, verbose, notify):
    """
    Rename a photo or video file according to a specified file naming convention.

    fpath {str} or {list}: filename or list of filenames to rename
    initials {str}: 2 or 3 letter initials string
    notify {bool}: execute `pydoni.opsys.macos_notify()` on program completion
    tz_adjust {int}: adjust file creation times by a set number of hours
    verbose {bool}: print messages and progress bar to console
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    assert len(initials) in [2, 3], 'Initials must be a 2- or 3-character string'

    vb = Verbose(verbose)
    mediafiles = list(fpath)

    assert len(mediafiles), 'No mediafiles to rename!'
    assert isinstance(mediafiles[0], str), \
        f'First element of variable `mediafiles` is of type {type(mediafiles[0]).__name__}, expected string'

    CONV = Convention()
    EXT = Extension()

    mediafiles = [os.path.abspath(x) for x in mediafiles \
        if not re.match(CONV.photo, os.path.basename(x)) \
        and not re.match(CONV.video, os.path.basename(x))]

    msg = f'Renaming {len(mediafiles)} media files'
    if verbose:
        vb.section_header(msg)
        pbar = tqdm(total=len(mediafiles), unit='mediafile')

    if not len(mediafiles):
        if verbose:
            pydoni.echo('No files to rename!', fg='green')

    for mfile in mediafiles:
        if verbose:
            vb.stabilize_postfix(mfile, max_len=15)

        mf = MediaFile(mfile)
        newfname = mf.build_fname(initials=initials, tz_adjust=tz_adjust)
        newfname = os.path.join(os.path.dirname(mfile), os.path.basename(newfname))

        if os.path.basename(mfile) != os.path.basename(newfname):
            os.rename(mfile, newfname)
            result[os.path.basename(mfile)] = os.path.basename(newfname)
            if verbose:
                tqdm.write('{}: {} -> {}'.format(
                    click.style('Renamed', fg='green'),
                    os.path.basename(mfile),
                    os.path.basename(newfname)))
        else:
            result[os.path.basename(mfile)] = '<not renamed, new filename identical>'
            if verbose:
                tqdm.write('{}: {}'.format(
                    click.style('Not renamed', fg='red'),
                    os.path.basename(mfile)))

        if verbose:
            pbar.update(1)

    if verbose:
        pbar.close()
        pydoni.echo(f'Renamed media files: {len(mediafiles)}', indent=2)

    if verbose or notify:
        pydoni.macos_notify(title='Mediafile Rename', message='Completed successfully!')

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='photo.rename_mediafile'))


@click.option('-d', '--dpath', type=click.Path(exists=True), required=True,
              help='Directory to look for timelapse stills in.')
@click.command()
def split_batch_exported_timelapse(dpath):
    """
    Split a directory of exported timelapse stills into their respective folders.

    Accept a directory of exported timelapse stills from Lightroom following Andoni's
    photo file naming convention. Those timelapse files will be in sequences numbered
    from 1 to the final # of the timelapse series, then will reset to 1 for the next
    timelapse. There could be an arbitrary number of timelapse stills in this directory.

    This program will take all the files in that directory and split them into folders
    for easy categorization.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    os.chdir(dpath)

    files = pydoni.listfiles(ext='jpg')
    assert len(files), "No timelapse stills found!"

    seqnums = [int(os.path.splitext(f.split('_')[4])[0]) for f in files]
    differences = []
    for i, num in enumerate(seqnums):
        last_idx = i - 1
        last_idx = last_idx if last_idx >= 0 else 0
        last_num = seqnums[last_idx]
        differences.append(num - last_num)

    delimiters = [i for i, x in enumerate(differences) if x not in [0, 1]]
    files_list_of_lists = pydoni.split_at(files, delimiters)

    for i, list_of_files in enumerate(files_list_of_lists):
        dname = 'timelapse_%s_of_%s' % (str(i+1), str(len(files_list_of_lists)))
        if not os.path.isdir(dname):
            os.mkdir(dname)
        for fname in list_of_files:
            newfname = os.path.join(dname, fname)
            os.rename(fname, newfname)

    result['directories_created'] = len(files_list_of_lists)
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='photo.split_batch_exported_timelapse'))


@click.option('--website-export-dpath', required=True, type=click.Path(exists=True),
              help='Directory that andonisooklaris.com mediafiles are exported to.')
@click.option('--outfile', default='auto', type=click.Path(),
              help='Filename or list of filenames to rename.')
@click.option('-v', '--verbose', is_flag=True,
              help='Print output to console.')
@click.command()
def website_extract_image_titles(website_export_dpath, outfile, verbose):
    """
    Scan photo files exported for andonisooklaris.com and construct list of image filenames
    and titles, separated by collection.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()


    def echo(*args, **kwargs):
        kwargs['timestamp'] = True
        pydoni.echo(*args, **kwargs)


    website_export_dpath = expanduser(website_export_dpath)
    if outfile == 'auto':
        outfile = os.path.join(website_export_dpath, 'Image Titles %s.txt' % pydoni.sysdate(stripchars=True))
    elif outfile is not None:
        assert not os.path.isfile(outfile)

    files = pydoni.listfiles(path=website_export_dpath, recursive=True, full_names=True)
    files = [f for f in files if os.path.splitext(f)[1].lower() != '.txt']

    if verbose:
        echo('Files found: ' + str(len(files)))
        echo('Extracting EXIF metadata...')
        exifd = pydoni.EXIF(files).extract()
        echo('EXIF metadata successfully extracted')

        if outfile is not None:
            echo('Writing output datafile: ' + outfile)
    else:
        exifd = pydoni.EXIF(files).extract()

    i = 0
    tracker = pd.DataFrame(columns=['collection', 'file', 'title'])
    for file in files:
        elements = file.replace(website_export_dpath, '').lstrip('/').split('/')
        subcollection = None
        collection = elements[0]
        fname = elements[-1]

        if len(elements) == 3:
            subcollection = elements[1]
            collection += ' - ' + subcollection

        exif = exifd[os.path.join(website_export_dpath, file)]
        title = exif['Title'] if 'Title' in exif.keys() else ''
        year = fname[0:4]
        title = str(year) + ' ' + str(title)

        tracker.loc[i] = [collection, fname, title]
        i += 1


    print_lst = []
    for collection in tracker['collection'].unique():
        print_lst.append('\nCollection: %s\n' % collection)
        df_print = tracker.loc[tracker['collection'] == collection].drop('collection', axis=1)
        print_lst.append(tabulate(df_print, showindex=False, headers=df_print.columns))

    print_str = '\n'.join(print_lst).strip()
    if outfile is None:
        print(print_str)
    else:
        with open(outfile, 'w') as f:
            f.write(print_str)

    if verbose:
        pydoni.program_complete()

    result['n_collections'] = len(tracker['collection'].unique())
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='photo.website_extract_image_titles'))


@click.group(name='photo')
def cli_photo():
    """Doni photo-based CLI tools."""
    pass


cli_photo.add_command(instagram_hashtags)
cli_photo.add_command(rename_mediafile)
cli_photo.add_command(website_extract_image_titles)
cli_photo.add_command(workflow)
