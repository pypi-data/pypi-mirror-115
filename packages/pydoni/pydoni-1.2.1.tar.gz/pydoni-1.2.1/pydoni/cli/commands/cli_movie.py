import click
import datetime
import numpy as np
import omdb
import pydoni
from tqdm import tqdm


def parse_omdb_ratings(ratings_object):
    """
    Extract IMDB, Rotten Tomatoes and Metacritic rating out of a ratings list of dictionaries
    queried directly from OMDB.

    ratings_object {list}: list of dictionaries containing retrieved OMDB rating values
    returns {dict}: cleaned ratings dictionary
    """
    import re

    movie_source_map = {
        'internet movie database': 'rating_imdb',
        'rotten tomatoes': 'rating_rt',
        'metacritic': 'rating_mc',
    }

    res = {
        'rating_imdb': None,
        'rating_rt': None,
        'rating_mc': None,
    }

    valid_sources = ['internet movie database', 'rotten tomatoes', 'metacritic']
    for rating in ratings_object:
        value = int(rating['value'].split('/')[0].replace('.', '').replace('%', '').replace(',', ''))
        res[movie_source_map[rating['source'].lower()]] = value

    return res


def clean_omdb_response(omdb_response_object):
    """
    Clean OMDB API response.

    omdb_response_object {dict}: raw response from OMDB API
    returns {dict}: dictionary of cleaned OMDB reponse
    """
    data = omdb_response_object
    ratings = parse_omdb_ratings(data['ratings'])

    keep_cols = ['imdb_votes', 'runtime', 'director', 'awards', 'imdb_id', 'country',
        'omdb_populated', 'genre', 'production', 'writer', 'type', 'box_office', 'dvd',
        'language', 'actors', 'response', 'rated', 'poster', 'website', 'plot']
    addtl_cols = ['rating_imdb', 'rating_rt', 'rating_mc']

    res = {col: None for col in keep_cols + addtl_cols}
    res['omdb_populated'] = True if len(data) else False

    for k, v in data.items():
        if k in res.keys():
            res[k] = v

    for k, v in ratings.items():
        if k in res.keys():
            res[k] = v

    none_values = ['N/A']
    for k, v in res.items():
        if v in none_values:
            res[k] = None

    date_items = ['dvd']
    for item in date_items:
        if res[item] is not None:
            res[item] = datetime.datetime.strptime(res[item], '%d %b %Y').date()

    bool_items = ['response']
    for item in bool_items:
        if res[item] is not None:
            res[item] = True if res[item].lower() in ['t', 'true'] else False

    num_items = ['imdb_votes', 'runtime', 'box_office']
    for item in num_items:
        if res[item] is not None:
            rm_str = [',', '.', 'min', ' ', '$']
            for string in rm_str:
                res[item] = res[item].replace(string, '')
            res[item] = int(res[item].strip())

    return res


def query_omdb(title, release_year, omdbapikey):
    """
    Query OMDB and return a dictionary. Will return empty if not found.

    title {str}: movie title to query for
    release_year {int}: release year of movie
    omdbapikey {str}: OMDB API key
    returns {dict}: dictionary of cleaned OMDB API response
    """
    omdb.set_default('apikey', omdbapikey)

    data = omdb.get(title=title, year=release_year, fullplot=False, tomatoes=False)
    data = clean_omdb_response(data) if len(data) else {}

    return data


def replace_null(val):
    """
    Replace given value with 'NULL' if it's an equivalent of NULL.

    val {any}: value to check
    returns {str}: 'NULL' or `val`
    """
    if isinstance(val, float):
        if np.isnan(val):
            return 'NULL'

    if val is None:
        return 'NULL'

    if isinstance(val, str):
        if val in ['nan', 'None']:
            return 'NULL'

    return val


def filter_updated_values(omdbresp, row):
    """
    Check each value queried from OMDB and that already in the database, and only add
    to a new dictionary, `upd` if it has changed. Therefore we only updated changed values.
    """
    import re

    upd = dict()
    for k, v in omdbresp.items():
        dbval = row[k]
        if v != dbval:
            if isinstance(dbval, date):
                dbval = str(dbval)
            else:
                # Attempt to compare integers/floats, may be
                # stored as int/float/str
                try:
                    v = re.sub(r'\..*', '', str(v))
                    dbval = re.sub(r'\..*', '', str(dbval))
                except:
                    pass

            if v != replace_null(dbval):
                upd[k] = v

    return upd


@click.option('-s', '--schema-name', type=str, required=True,
              help='IMDB table schema name.')
@click.option('-t', '--table-name', type=str, required=True,
              help='IMDB table name.')
@click.option('-o', '--omdbapikey', type=str, required=True,
              help='OMDB API key.')
@click.option('-v', '--verbose', is_flag=True,
              help='Print output to console.')
@click.command()
def refresh_imdb_table(schema_name, table_name, omdbapikey, verbose=False):
    """
    Query Postgres table containing IMDB metadata and refresh any values that need updating.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    # 'result' will be a dictionary where the movie names are the keys, and the values are
    # dictionaries with items: 'status', 'message', 'updated_values' (dictionary of
    # updated values, if any).
    result_items = ['status', 'message', 'updated_values']

    pg = pydoni.Postgres()
    pkey_name = 'movie_id'
    df = pg.read_table(schema_name, table_name).sort_values(pkey_name)
    cols = pg.col_names(schema_name, table_name)

    if verbose:
        pbar = tqdm(total=len(df), unit='movie')

    for i, row in df.iterrows():
        movie_name = f"{row['title']} ({str(row['release_year'])})"

        try:
            omdbresp = query_omdb(title=row['title'],
                                  release_year=row['release_year'],
                                  omdbapikey=omdbapikey)

        except Exception as e:
            err_str = f"{click.style('ERROR', fg='red')} in {movie_name}: {str(e)}"
            tqdm.write(err_str)

            result[movie_name] = {k: v for k, v in zip(result_items, ['Error', str(e), None])}

            if verbose:
                pbar.update(1)

            continue


        omdbresp = {k: v for k, v in omdbresp.items() if k in cols}
        omdbresp = {k: replace_null(v) for k, v in omdbresp.items()}

        color_map = {'No change': 'yellow', 'Updated': 'green', 'Not found': 'red'}
        change = 'Not found' if not len(omdbresp) else 'No change'

        # Filter out columns and values that do not require an update
        if change != 'Not found':
            upd = filter_updated_values(omdbresp, row)
            change = 'Updated' if len(upd) else change
            upd['imdb_update_ts'] = datetime.datetime.now()

            stmt = pg.build_update(schema_name,
                                   table_name,
                                   pkey_name=pkey_name,
                                   pkey_value=row[pkey_name],
                                   columns=[k for k, v in upd.items()],
                                   values=[v for k, v in upd.items()],
                                   validate=True)
            pg.execute(stmt)

            upd_backend = {k: v for k, v in upd.items() if k != 'imdb_update_ts'}
            upd_backend = upd_backend if len(upd_backend) else None
            result[movie_name] = {k: v for k, v in zip(result_items, [change, None, upd_backend])}

        else:
            result[movie_name] = {k: v for k, v in zip(result_items, [change, None, None])}

        if verbose:
            pbar.update(1)
            space = '  ' if change == 'Updated' else ''
            tqdm.write(click.style(change, fg=color_map[change]) + space + ': ' + movie_name)

    if verbose:
        pbar.close()
        pydoni.program_complete('Movie refresh complete!')

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='movie.refresh_imdb_table'))


@click.group(name='movie')
def cli_movie():
    """Doni movie-based CLI tools."""
    pass


cli_movie.add_command(refresh_imdb_table)
