import pandas as pd  # type: ignore


class Datasets:
    def __init__(
        self,
        filepath: str = "data/Childrens_social_care_in_England_2022_underlying_data.xlsx",
    ) -> None:
        self.filepath = filepath

    def extract_data_for_bar_charts(self):
        df = pd.read_excel(
            self.filepath,
            "LA_level_at_31_Mar_2022",
            header=2,
        )

        return df
