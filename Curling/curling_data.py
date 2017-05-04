import pandas as pd


def read_roster():
    df = pd.read_csv('roster.csv')
    df.fillna(0, inplace=True)
    for col in df.columns[2:]:
        df[col] = map(int, df[col])
    return df


def write_roster(df):
    print "Saving Roster"
    df.sort_values(by=['Last Name', 'First Name'], inplace=True)
    df.index = range(len(df))
    df.to_csv('roster.csv', index=False)


def read_ratings():
    df = pd.read_csv('ratings.csv')
    return df


def write_ratings(df):
    print "Saving ratings"
    df.sort_values(by=['Last Name', 'First Name'], inplace=True)
    df.index = range(len(df))
    df.to_csv('ratings.csv', index=False)


def read_sheet_count():
    df = pd.read_csv('sheet_count.csv')
    return df


def write_sheet_count(df):
    print "Saving sheet count"
    df.sort_values(by=['Last Name', 'First Name'], inplace=True)
    df.index = range(len(df))
    df.to_csv('sheet_count.csv', index=False)


def read_snacks():
    snacks_df = pd.read_csv('snack_list.csv')
    snacks_df.fillna(0, inplace=True)
    return snacks_df


def write_snacks(snacks_df):
    snacks_df.sort_values(by=['Last Name', 'First Name'], inplace=True)
    snacks_df.index = range(len(snacks_df))
    snacks_df.write_csv(index=False)
