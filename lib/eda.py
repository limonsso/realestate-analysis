from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from IPython.display import display, Markdown
import seaborn as sns
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, RobustScaler


def get_modalities( df: pd.DataFrame, col, display=True):
    """
    Affiche les modalités uniques d'une colonne d'un DataFrame.

    Parameters:
    dataframe (pd.DataFrame): Le DataFrame contenant la colonne.
    col (str): Le nom de la colonne dont les modalités doivent être affichées.

    Returns:
    None
    """
    unique_vals = df[col].unique()
    if display:
        print_Markdown(f'\nLes modalités de la variable {col}:')
        for value in unique_vals:
            print_Markdown(f'* "{value}"')

    return unique_vals


def display_proportions_by_modalities( df: pd.DataFrame, col, width=900, height=800, graph='histogram',
                                      color=None):
    """
    Affiche les proportions uniques d'une colonne.'
    :param have_missing_values:
    :param col:
    :return:
    """
    color = col if color is None else color
    _df = df.copy()
    if df[col].isnull().sum() > 0:
        # Remplacer les nan par unknown
        _df[col] = _df[col].fillna('nan')
    if graph == 'histogram':
        fig = px.histogram(_df, x=col, title=f'Distribution de la Variable "{col}"', color=color, width=width,
                           height=height).update_xaxes(categoryorder='total descending')
    fig.show()


def find_low_frequency_categories( df: pd.DataFrame, col: str, min_count_rows, show=True) -> pd.DataFrame:
    """
    Trouve et imprime les modalités avec une fréquence inférieure à une valeur minimale pour une colonne donnée dans un DataFrame.

    Parameters:
    - df: pd.DataFrame
        Le DataFrame à analyser.
    - col: str
        Le nom de la colonne pour laquelle analyser les modalités.
    - min_count_rows: int
        La fréquence minimale pour une modalité à ne pas être regroupée.
    - should_print: bool, optional (default=True)
        Si True, imprime les modalités avec une fréquence inférieure à min_count_rows.

    Returns:
    - mod_to_regroup: pd.Series
        Les modalités avec une fréquence inférieure à min_count_rows.
    """
    counts_by_mod = df[col].value_counts().sort_values(ascending=True)
    mod_to_regroup = counts_by_mod[counts_by_mod < min_count_rows]
    if show:
        print_Markdown(f'\nles modalités qui ont moins de {min_count_rows} observations pour la variable \'{col}\' :')
        for value in mod_to_regroup.index:
            print_Markdown(f'* {value}')

    return mod_to_regroup


def infos( df: pd.DataFrame, col: str, show=True):
    count = df['ID'].shape[0]
    val_count = df[col].value_counts().sum()
    missing_count = df[col].isnull().sum()
    missing_vals_percent = ((missing_count / count) * 100).round(2)
    unique_count = df[col].nunique()
    if show:
        color = {1: '#EC7063', 0: '#FFC300'}
        str_nbr_ob = f"Nombres d'observations: ***{val_count} ({((val_count / count) * 100).round(2)}%)***"
        str_unique = f"Valeurs distinctes: ***{unique_count}***"
        missing_vals_percent_format = f"<span style='background-color:{color[int(missing_vals_percent / 50)]}'>({missing_vals_percent}%)</span>"
        str_missing = f"Nombres d'observations manquantes : ***{'--' if missing_count <= 0 else f'{missing_count} {missing_vals_percent_format}'}***"
        print_Markdown(f'{str_nbr_ob}<br>{str_unique}<br>{str_missing}')
    return val_count, missing_count, missing_vals_percent, unique_count


def print_Markdown( text: str):
    display(Markdown(text))


def one_hot_encoded( df: pd.DataFrame, col: str, drop_first=False):
    # créer un objet de la classe LabelEncoder
    encode_1 = LabelEncoder()
    _df = df

    # créer un objet de la classe OneHotEncoder
    encode_2 = OneHotEncoder()

    # combiner l'application des deux classes
    encode_result_array = encode_2.fit_transform(encode_1.fit_transform(_df[col]).reshape(-1, 1))
    modalites = _df[col].unique()
    if drop_first:
        modalites = modalites[1:]
        encode_result_array = encode_result_array[:, 1:]
    # transformer la sortie en dataframe
    encode_result_df = pd.DataFrame(encode_result_array.toarray(), columns=[f'{col}_{x}' for x in modalites])

    return encode_result_df


def one_hot_encode_multiple( df: pd.DataFrame, cols: list, drop_first=False):
    """
    Effectue un encodage one-hot sur plusieurs colonnes d'un DataFrame pandas.

    Arguments:
    df -- DataFrame pandas
    cols -- Liste des colonnes à encoder
    drop_first -- Booléen, si True supprime la première modalité pour chaque colonne pour éviter la colinéarité

    Retourne:
    - df_combined -- DataFrame avec les colonnes encodées
    """
    # Vérifier si les colonnes existent
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' n'existe pas dans le DataFrame.")

    # Initialiser l'encodeur
    encoder = OneHotEncoder(drop='first' if drop_first else None, sparse_output=False)

    # Appliquer l'encodage
    encoded_array = encoder.fit_transform(df[cols])

    # Créer les noms des colonnes encodées
    encoded_columns = []
    for i, col in enumerate(cols):
        encoded_columns.extend([f"{col}_{category}" for category in encoder.categories_[i]])
    if drop_first:
        encoded_columns = [
            f"{col}_{category}"
            for i, col in enumerate(cols)
            for category in encoder.categories_[i][1:]
        ]

    # Convertir en DataFrame
    df_encoded = pd.DataFrame(encoded_array, columns=encoded_columns, index=df.index)

    # Combiner avec le DataFrame original
    df_combined = pd.concat([df.drop(columns=cols), df_encoded], axis=1)

    return df_combined


def ordinal_encoded( df: pd.DataFrame, col: str):
    """
    Fonction pour effectuer un encodage ordinal sur une colonne d'un DataFrame pandas.

    Arguments:
    df -- DataFrame pandas
    column -- Nom de la colonne à encoder

    Retourne:
    df -- DataFrame avec la colonne encodée
    encoder -- L'encodeur utilisé pour l'encodage
    """
    encoder = OrdinalEncoder()
    df[col] = encoder.fit_transform(df[[col]])
    return df[col].to_frame()


def ordinal_encode_multiple( df: pd.DataFrame, cols: list):
    """
    Effectue un encodage ordinal sur plusieurs colonnes d'un DataFrame pandas.

    Arguments:
    df -- DataFrame pandas
    cols -- Liste des colonnes à encoder

    Retourne:
    - df_enc -- DataFrame avec les colonnes encodées
    - encoders -- Dictionnaire des encodeurs utilisés, clé = colonne
    """
    # Vérifier si les colonnes existent
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' n'existe pas dans le DataFrame.")

    # Créer une copie du DataFrame pour éviter de modifier l'original
    df_enc = df.copy()
    encoders = {}

    # Appliquer l'encodage pour chaque colonne
    for col in cols:
        encoder = OrdinalEncoder()
        df_enc[col] = encoder.fit_transform(df_enc[[col]])
        encoders[col] = encoder

    return df_enc, encoders


def scaling_data( X_train, X_val, X_test):
    all_cols = list(X_train.columns)
    # X
    Transformer = RobustScaler().fit(X_train)
    # Application de la standardisation sur tous les ensembles
    X_train = Transformer.transform(X_train)
    X_val = Transformer.transform(X_val)
    X_test = Transformer.transform(X_test)
    # Conversion en dataframe
    X_train = pd.DataFrame(X_train, columns=all_cols)
    X_val = pd.DataFrame(X_val, columns=all_cols)
    X_test = pd.DataFrame(X_test, columns=all_cols)

    return X_train, X_val, X_test


def missing_data_proportion( df: pd.DataFrame, in_percente=False, show=True):
    """
        Analyzes and displays missing data in a DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to analyze.
        in_percente (bool): If True, shows missing data as percentages. Defaults to False.
        show (bool): If True, prints the missing data summary. Defaults to True.

        Returns:
        pd.DataFrame: A DataFrame with columns 'Column' (names) and 'Missing' (counts or percentages).
        """
    missing_data = (
        (df.isnull().sum() * 100 / df.shape[0]).round(2)
        if in_percente
        else df.isnull().sum()
    ).sort_values(ascending=False)

    # Filter columns with missing data
    #missing_data = missing_data[missing_data > 0]

    # Convert to DataFrame for clarity
    missing_df = missing_data.reset_index()
    missing_df.columns = ['Column', 'Missing']

    # Display if required
    if show:
        msg = f"Les colonnes avec des données manquantes {'en pourcentage' if in_percente else ''}:"
        print(msg)
        print(missing_df)

    return missing_df


def get_wisker_outlier( col):
    q1, q3 = np.percentile(col, [25, 75])
    iqr = q3 - q1
    lw = q1 - 1.5 * iqr
    uw = q3 + 1.5 * iqr
    return lw, uw


def correlation( dataset: pd.DataFrame, threshold):
    col_corr = set()
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                colname = corr_matrix.columns[i]
                col_corr.add(colname)
    return col_corr


def display_matrix_corr( df: pd.DataFrame, y_col, annot=True, cmap="rainbow"):
    print_Markdown(f"Visualisons la corrélation entre les variables explicatives et notre variable cible ({y_col})")

    corr_matrix = df.corr().abs()
    #print(corr_matrix[y_col].sort_values(ascending=False).head(30))
    # Pour le traitement subséquent, on commence par mettre temporairement la diagonale de la matrice à 0
    for col in corr_matrix:
        corr_matrix.at[col, col] = 0
    print_Markdown('Visualisons la matrice de corrélation')
    #correlation map
    f, ax = plt.subplots(figsize=(18, 18))
    sns.heatmap(df.drop([y_col], axis=1).corr(), annot=annot, fmt='.1f', ax=ax, cmap=cmap)
    #sns.heatmap(X_train.corr(),ax=ax)


def get_features_corr( df: pd.DataFrame, seuil_to_corr=0.5, annot=True, show=True, cmap="rainbow"):
    corr_matrix = df.corr().abs()
    for col in corr_matrix:
        corr_matrix.at[col, col] = 0
    # Trouver les colonnes des variables explicatives avec corrélation élevée
    to_drop = [column for column in corr_matrix.columns if any(corr_matrix[column] > seuil_to_corr)]
    corr_matrix2 = df[to_drop].corr().abs()
    if show:
        print_Markdown('***{0}*** Variables explicatives avec corrélation supérieure à {1}: '.format(len(to_drop),
                                                                                                 seuil_to_corr))
        print_Markdown(to_drop)
        print_Markdown("Voici la matrice de corrélation des varibales explicatives.")
        #correlation map
        f, ax = plt.subplots(figsize=(18, 18))
        sns.heatmap(corr_matrix2.corr(), annot=annot, fmt='.1f', ax=ax, cmap=cmap)
        plt.show()

    return to_drop


def get_features_moins_corr( df: pd.DataFrame, X_cols, y_col, seuil_min_with_y=0.005, show=True):
    cols = X_cols
    cols.append(y_col)
    corr_matrix3 = df[cols].corr().abs()
    if show:
        print_Markdown("Corrélation avec notre variable cible")
        print_Markdown(corr_matrix3[y_col].sort_values(ascending=False))

    X_cols = [x for x in corr_matrix3[y_col].index if corr_matrix3[y_col].loc[x] < seuil_min_with_y]
    return X_cols
