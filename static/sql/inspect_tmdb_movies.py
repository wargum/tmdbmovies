import logging
import os
import pandas as pd
import sys as sys
import json

def main(argv=None):
    """
    Utilize Pandas library to read in both UNSD M49 country and area .csv file
    (tab delimited) as well as the UNESCO heritage site .csv file (tab delimited).
    Extract regions, sub-regions, intermediate regions, country and areas, and
    other column data.  Filter out duplicate values and NaN values and sort the
    series in alphabetical order. Write out each series to a .csv file for inspection.
    """
    if argv is None:
        argv = sys.argv

    msg = [
        'Source file read {0}',
        'cast written to file {0}',
        'movie written to file {0}',
        'movie_cast written to file {0}'
    ]

    # Setting logging format and default level
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    # Read in tmdb_5000_movies data set (comma separator)
    movie_csv = './input/csv/tmdb_5000_movies.csv'
    movie_data_frame = read_csv(movie_csv, ',')
    logging.info(msg[0].format(os.path.abspath(movie_csv)))


    # Read in tmdb_5000_movies data set (comma separator)
    credit_csv = './input/csv/tmdb_5000_credits.csv'
    credit_data_frame = read_csv(credit_csv, ',').drop(['title'], axis = 1)
    logging.info(msg[0].format(os.path.abspath(credit_csv)))

    data_frame = pd.merge(movie_data_frame, credit_data_frame, left_on='id', right_on='movie_id', how='inner').drop(['id','spoken_languages','keywords','production_companies', 'production_countries', 'crew'], axis = 1).drop_duplicates(subset='movie_id')[0:1000]
    data_frame['genres'] = data_frame['genres'].apply(json.loads)
    data_frame['genres'] = data_frame['genres'].apply(pipe_flatten_names)

    # Write casts to a .csv file.
    cast = extract_filtered_series(data_frame, 'cast')
    cast = cast.drop_duplicates(subset='id').drop(['order','character', 'cast_id', 'credit_id'], axis = 1)
    cast_csv = './output/cast.csv'
    write_series_to_csv(cast, cast_csv , '\t', False)
    logging.info(msg[1].format(os.path.abspath(cast_csv)))

    # # # Write movie to a .csv file.
    movie = data_frame.drop(['cast'], axis = 1)
    movie_csv = './output/movie.csv'
    write_series_to_csv(movie, movie_csv , '\t', False)
    logging.info(msg[2].format(os.path.abspath(movie_csv)))

    # # Write countries or areas to a .csv file.
    movie_cast = pd.DataFrame(columns = ['cast_id', 'character', 'credit_id', 'gender', 'id', 'name', 'order', 'movie_id'])
    for i in range(0, len(data_frame['cast'])):
        temp_dict = json.loads(data_frame['cast'][i])
        temp_dict_data_frame = pd.DataFrame.from_dict(temp_dict)
        temp_dict_data_frame['movie_id'] = data_frame['movie_id'][i]
        movie_cast = movie_cast.append(temp_dict_data_frame[0:3])
    movie_cast = movie_cast.drop(['cast_id', 'credit_id','gender', 'order', 'name'], axis = 1)  
    movie_cast_csv = './output/movie_cast.csv'
    write_series_to_csv(movie_cast, movie_cast_csv, '\t', False)
    logging.info(msg[3].format(os.path.abspath(movie_cast_csv)))

def extract_filtered_series(data_frame, column_name):
    """
    Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
    Duplicate values and NaN or blank values are dropped from the result set which is
    returned sorted (ascending).
    :param data_frame: Pandas DataFrame
    :param column_name: column name string
    :return: Panda Series one-dimensional ndarray
    """
    column = data_frame[column_name]
    final_dict = []
    for i in range(0, len(column)):
        temp_dict = json.loads(column[i])
        final_dict.extend(temp_dict[0:3])
    final_data_frame = pd.DataFrame.from_dict(final_dict)
    return final_data_frame


def read_csv(path, delimiter=','):
    """
    Utilize Pandas to read in *.csv file.
    :param path: file path
    :param delimiter: field delimiter
    :return: Pandas DataFrame
    """
    return pd.read_csv(path, sep=delimiter, engine='python')


def write_series_to_csv(series, path, delimiter=',', row_name=True):
    """
    Write Pandas DataFrame to a *.csv file.
    :param series: Pandas one dimensional ndarray
    :param path: file path
    :param delimiter: field delimiter
    :param row_name: include row name boolean
    """
    series.to_csv(path, sep=delimiter, index=row_name)

def pipe_flatten_names(keywords):
    return ','.join([x['name'] for x in keywords])
    
if __name__ == '__main__':
    sys.exit(main())
    
