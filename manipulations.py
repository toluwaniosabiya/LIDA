import pandas as pd  # type: ignore

from datasets import Datasets

datasets = Datasets()


class BarChartBuilder:

    def __init__(
        self,
        dataset: pd.DataFrame = datasets.extract_data_for_national_effectiveness(),
    ) -> None:
        self.dataset = dataset

    def get_dropdown_options(self) -> list[dict]:
        dropdown_list = self.dataset.columns[-4:].tolist()
        dropdown_options = [{"label": f"{item}", "value": f"{item}"} for item in dropdown_list]

        return dropdown_options

    def supply_bar_chart_info(self, column: str) -> pd.Series:
        series = self.dataset[column].value_counts(normalize=True) * 100

        return series
