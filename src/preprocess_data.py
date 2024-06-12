"""Transform raw data to train / val datasets """
import argparse
import logging
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/preprocess_data.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')


IN_FILES = ['data/raw/1_2024-05-14_20-14.csv',
            'data/raw/2_2024-05-14_20-31.csv',
            'data/raw/3_2024-05-14_20-49.csv',
            'data/raw/1_2024-06-05_21-35.csv',
            'data/raw/2_2024-06-05_21-39.csv',
            'data/raw/3_2024-06-05_21-48.csv']

OUT_TRAIN = 'data/proc/train.csv'
OUT_VAL = 'data/proc/val.csv'

TRAIN_SIZE = 0.9


def main(args):
    main_dataframe = pd.read_csv(args.input[0], delimiter=',')
    for i in range(1, len(args.input)):
        data = pd.read_csv(args.input[i], delimiter=',')
        df = pd.DataFrame(data)
        main_dataframe = pd.concat([main_dataframe, df], axis=0)

    main_dataframe['url_id'] = main_dataframe['url'].map(lambda x: x.split('/')[-2])
    new_dataframe = main_dataframe[['url_id', 'total_meters', 'floor','floors_count','rooms_count', 'underground', 'price']].set_index('url_id')

    new_df = new_dataframe[new_dataframe['price'] < 30_000_000].sample(frac=1)

    new_df['first_floor'] = new_df['floor'] == 1
    new_df['last_floor'] = new_df['floor'] == new_df['floors_count']
    le = LabelEncoder()
    le.fit(new_df["underground"])
    le_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
    le_mapping = {k : int(val) for k, val in le_mapping.items()}
    new_df["underground"] = le.transform(new_df["underground"])
    #new_df['underground'] = new_df['underground'] is not None

    out_file = open("data/dicts/underground.json", "w", encoding='utf8')
    json.dump(le_mapping, out_file, ensure_ascii=False)
    out_file.close()

    df = new_df[['total_meters',
                        'first_floor',
                        'last_floor',
                        'floors_count',
                        'rooms_count',
                        'underground',
                        'price']]

    border = int(args.split * len(df))
    train_df, val_df = df[0:border], df[border:-1]
    train_df.to_csv(OUT_TRAIN)
    val_df.to_csv(OUT_VAL)
    logger.info(f'Write {args.input} to train.csv and val.csv. Train set size: {args.split}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--split', type=float,
                        help='Split test size',
                        default=TRAIN_SIZE)
    parser.add_argument('-i', '--input', nargs='+',
                        help='List of input files',
                        default=IN_FILES)
    args = parser.parse_args()
    main(args)