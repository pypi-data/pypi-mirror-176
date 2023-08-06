import re
import pyreadstat
import pandas as pd


class MetaTable:
    def __init__(self, df: pd.DataFrame, meta: pyreadstat._readstat_parser.metadata_container) -> None:
        self.df = df
        self.meta = meta

    def select_columns(self, columns: list):
        column_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]
        column_labels = [v for i, v in enumerate(self.meta.column_labels) if i in column_indexes]

        self.meta.column_labels = column_labels
        self.meta.column_names = columns
        self.meta.column_names_to_labels = {key: value for key, value in zip(columns, column_labels)}
        self.meta.original_variable_types = {
            key: value for key, value in self.meta.original_variable_types.items() if key in columns}
        self.meta.readstat_variable_types = {
            key: value for key, value in self.meta.readstat_variable_types.items() if key in columns}
        self.meta.variable_alignment = {
            key: value for key, value in self.meta.variable_alignment.items() if key in columns}
        self.meta.variable_display_width = {
            key: value for key, value in self.meta.variable_display_width.items() if key in columns}
        self.meta.variable_measure = {
            key: value for key, value in self.meta.variable_measure.items() if key in columns}
        self.meta.variable_storage_width = {
            key: value for key, value in self.meta.variable_storage_width.items() if key in columns}
        self.meta.variable_to_label = {
            key: value for key, value in self.meta.variable_to_label.items() if key in columns}
        self.meta.variable_value_labels = {
            key: value for key, value in self.meta.variable_value_labels.items() if key in columns}

        labels = set(self.meta.variable_to_label.values())
        self.meta.value_labels = {
            key: value for key, value in self.meta.value_labels.items() if key in labels}

        self.meta.number_columns = len(columns)
        self.df = self.df[columns]

    def val_lab(self, columns: list[str], labels: dict[int, str]):
        # my_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]

        # find correct label name
        used = set([int(re.findall(r'\d+', v)[-1]) for v in list(self.meta.variable_to_label.values())])
        all = range(len(used) + 1)
        label_name = f'labels{min(set(all) - used)}'

        for column in columns:
            self.meta.original_variable_types[column] = 'F10.0'
            self.meta.readstat_variable_types[column] = 'double'
            self.meta.variable_measure[column] = 'nominal'
            self.meta.variable_to_label[column] = label_name
            self.meta.variable_value_labels[column] = labels

        self.meta.value_labels[label_name] = labels

    def var_lab(self, columns: list[str], text: str):
        my_indexes = [i for i, v in enumerate(self.meta.column_names) if v in columns]

        for column in columns:
            self.meta.column_names_to_labels[column] = text

        for i in my_indexes:
            self.meta.column_labels[i] = text

    def show(self, variable):
        print(self.meta.column_names_to_labels[variable])

        print('')
        value_labels = self.meta.variable_value_labels['F5_01']
        for key, value in value_labels.items():
            print(f'{key: >12}   {value}')

        print('')
        print(list(value_labels.keys()))
        print(list(value_labels.values()))

    def write_sav(self, path: str):
        pyreadstat.write_sav(
            df=self.df,
            dst_path=path,
            column_labels=self.meta.column_labels,
            variable_value_labels=dict(self.meta.variable_value_labels),
            variable_measure=self.meta.variable_measure,
        )


if __name__ == '__main__':
    df1, meta1 = pyreadstat.read_sav('./data/fertig_R.sav')

    print(meta1.column_names_to_labels['F5_01'])
    print(meta1.variable_value_labels['F5_01'])

    x = MetaTable(df1, meta1)
    x.val_lab(['F5_01', 'F5_02'], {1: 'Fish', 2: 'Chips'})
    x.var_lab(['F5_01', 'F5_02'], 'New Label')
    x.select_columns(['F5_01', 'F5_02'])
    x.show('F5_01')
    x.write_sav('./data/fertig_test.sav')
