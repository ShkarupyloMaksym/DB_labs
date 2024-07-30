import pandas as pd


class DataImporter:
    def __init__(self, data_path='./../data/GlobalWeatherRepository.csv'):
        self.data_path = data_path
        self.selected_columns = ['country', 'wind_degree', 'wind_kph', 'wind_direction', 'last_updated', 'sunrise']
        # 23 == 3 == осади
        self.variant_chosen = ['pressure_mb', 'pressure_in', 'precip_mm', 'precip_in', 'humidity', 'cloud']
        self.chosen_columns = self.selected_columns + self.variant_chosen

    def get_data(self):
        df = pd.read_csv(self.data_path)
        df = df[self.chosen_columns]
        df.index.name = 'id'
        df.index += 1
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df['sunrise'] = pd.to_datetime(df['sunrise'], format='%I:%M %p').dt.time
        return df

    def get_data_columns(self):
        df = self.get_data()
        return df.columns


if __name__ == '__main__':
    importer = DataImporter()
    columns = importer.get_data_columns()
    print(columns)
    print(importer.get_data().info())
