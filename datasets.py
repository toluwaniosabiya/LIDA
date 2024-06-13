import pandas as pd  # type: ignore

filepath: str = "data/Childrens_social_care_in_England_2022_underlying_data.xlsx"


class Datasets:

    def __init__(
        self,
    ) -> None:
        self.filepath = filepath

    def extract_data_for_national_effectiveness(self):
        df = pd.read_excel(
            self.filepath,
            "LA_level_at_31_Mar_2022",
            header=2,
        )

        return df

    def extract_data_for_provision_types_and_places(self):
        df = pd.read_excel(
            self.filepath,
            "Provider_level_at_31_Mar_2022",
            header=4,
        )

        return df
