import click
import emoji
import emoji
import enchant
import enchant
import langid
import langid
import nltk
import string
from nltk.corpus import stopwords
from tqdm import tqdm


def is_punctuation(token):
    """
    Determine whether a token is punctuation.
    """
    return token in string.punctuation + '’‘“”``'


def detect_token_language(pg, token):
    """
    Given a token string, determine the language of a token either as a natural, human
    language, as an emoji character, or a punctuation mark.
    """
    if is_punctuation(token):
        return 'punct'

    emoji_lst = [k for k, v in emoji.UNICODE_EMOJI.items()]
    if token in emoji_lst:
        return 'emoji'

    d = enchant.Dict('en_US')
    if d.check(token):
        # Token is English word
        return 'en'


    # Attempt to classify token using `langid`
    lang_code = langid.classify(token)[0]
    if lang_code in ['nl', 'de', 'el', 'fr']:
        d = enchant.Dict(lang_code)
        if d.check(token):
            # Token is in the language's dictionary
            return lang_code

        # Token is not in language's dictionary, but could still be a token
        # in the language parsed by `langid`
        if lang_code == 'el':
            uniquely_greek_chars = [
                'α', 'β', 'Γ', 'γ', 'Δ', 'δ', 'ε', 'ζ', 'η', 'Θ', 'θ', 'ι', 'κ', 'Λ', 'λ', 'μ',
                'ν', 'Ξ', 'ξ', 'Ο', 'ο', 'Π', 'π', 'Ρ', 'ρ', 'Σ', 'σ', 'ς', 'Τ', 'τ', 'Υ', 'υ',
                'Φ', 'φ', 'Χ', 'χ', 'Ψ', 'ψ', 'Ω', 'ω',
            ]
            if any([x in token for x in uniquely_greek_chars]):
                return lang_code

    # Token unable to be classified, assign English as default
    return 'en'


def refresh_tokens(pg, vb, tag, dry_run, table_schema, table_name, limit, message_tokens_table):
    """
    Map each unique token to descriptor columns (stem, lemma, length, language, etc.).
    """
    result = {}

    trigger_name = table_schema + '_' + table_name + '_rmod'
    if not pg.trigger_exists(table_schema, trigger_name):
        pg.execute(f"""
        create or replace trigger {trigger_name}
        before update on "{table_schema}"."{table_name}"
        for each row execute procedure set_rmod()""")

    vb.info(f"Created the database trigger {click.style(table_schema + '.' + trigger_name, fg='black')}", tag=tag)

    new_tokens = pg.read_sql(f"""
    select distinct lower(t1.token) as "token"
    from {message_tokens_table.table_schema}.{message_tokens_table.table_name} t1
    left join {table_schema}.{table_name} t2
           on lower(t1.token) = lower(t2.token)
    where t2.token is null
    """, simplify=False)
    vb.info(f'Total new unique tokens: {len(new_tokens)}', tag=tag)

    if len(new_tokens) > 0:
        if isinstance(limit, int):
            new_tokens = new_tokens.head(limit)
            vb.info(f'Limited to {limit} new tokens', tag=tag)

        stops = stopwords.words('english')
        lemmatizer = nltk.stem.WordNetLemmatizer()
        stemmer = nltk.stem.PorterStemmer()

        def detect_token_language_(token):
            detect_token_language(pg, token)

        column_apply_function_map = {
            'length': len,
            'stem': stemmer.stem,
            'lemma': lemmatizer.lemmatize,
            'is_english_stopword': lambda tok: tok in stops,
            'is_punct': is_punctuation,
            'language': detect_token_language_,
        }

        if vb.verbose:
            tqdm.pandas()

        for col, fun in column_apply_function_map.items():
            vb.info(f'Computing column: `{col}`', tag=tag)
            if vb.verbose:
                new_tokens[col] = new_tokens['token'].progress_apply(fun)
            else:
                new_tokens[col] = new_tokens['token'].apply(fun)

        vb.info(f'Finished computing additional columns', tag=tag)

    if dry_run:
        tag.add('dry-run')

    vb.info(f'Appending tokens to {table_schema}.{table_name}', tag=tag)
    n_new_tokens_str = len(new_tokens) if len(new_tokens) > 0 else 'no'

    if not dry_run:
        new_tokens.to_sql(table_name, pg.dbcon, schema=table_schema, index=False, if_exists='append')

    vb.info(f'Appended {n_new_tokens_str} new tokens to {table_schema}.{table_name}', tag=tag)

    result['new_tokens'] = len(new_tokens)

    return result
