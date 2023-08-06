"""Package to downloade content from NB. For personal use.

=======================

Written by Eirik Berger
"""


def ListNB(from_year, to_year, search_string, doctype):
    """Get list of books from NB."""
    # setup
    import dhlab.module_update as mu
    mu.update('dhlab_v2')
    import dhlab_v2 as d2
    mu.css()

    import pandas as pd

    import warnings
    warnings.filterwarnings("ignore")

    # main content
    paper_list = d2.document_corpus(doctype=doctype,
                                    from_year=from_year,
                                    to_year=to_year,
                                    limit=9999999)

    paper_list.timestamp = paper_list.timestamp.astype(str)
    paper_list.year = paper_list.year.astype(int)
    paper_list.timestamp = pd.pandas.to_datetime(paper_list.timestamp,
                                                 format='%Y%m%d',
                                                 errors='coerce')

    selected_list = paper_list[paper_list.title.str.contains(search_string)]
    selected_list = selected_list.sort_values(by='year',
                                              ascending=True,
                                              na_position='first')

    selected_list = selected_list.drop_duplicates(subset=['urn'])
    selected_list = selected_list.reset_index(drop=True)

    selected_list.to_csv('nb_search.csv', sep=';', encoding='utf-8')

    return selected_list


def DownloadeNB(selected_list):
    """Download remaining books from list."""
    import tqdm
    import os
    import pathlib
    import requests

    # setup
    try:
        os.mkdir('downloads_folder')
    except:
        pass

    selected_list['download_log'] = 'TBC'

    for u in tqdm.tqdm(range(len(selected_list)), position=0, leave=True, desc='Downloading items'):

        if selected_list['urn'][u] not in os.listdir('downloads_folder/'):
            filename = pathlib.Path('downloads_folder/' + selected_list['urn'][u] + '.pdf')
            url = 'https://www.nb.no/services/downloader?urn='+selected_list['urn'][u]+'&resolutionlevel=6'

            print("Trying to downloade ", url)

            try:
                response = requests.get(url)

                filename.write_bytes(response.content)

                selected_list['download_log'][u] = 'Done'
                selected_list.to_csv('nb_search.csv', sep=';', encoding='utf-8')

                print('Success.')

            except RuntimeError:
                selected_list['download_log'][u] = 'Error'
                selected_list.to_csv('nb_search.csv', sep=';', encoding='utf-8')

                print('Failed.')
