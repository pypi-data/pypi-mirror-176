from typing import Union

import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from pathlib import Path


SUPPORTED_RESOURCES = [
        "Patient",
        "Procedure",
        "Condition",
        "Observation",
        "Immunization",
        # "AllergyIntolerance", getting erros on synthrea
    ]

# could be an abstraction
class DQIModel:
    def __init__(self, context="systolic") -> None:
        """Does stuff"""
        self.context = context

    @property
    def weights(self):
        package_dir = Path(__file__).parent
        dimension_weights = pd.read_csv(
            f"{package_dir}/weights/{self.context}/dimension_weights.csv")
        feature_weights = pd.read_csv(
            f"{package_dir}/weights/{self.context}/feature_weights.csv")
        weights = pd.concat([feature_weights, dimension_weights])[
            ['feature', 'dimension', 'weight']]
        return weights

    def fit_transform(self, bundles: Union[pd.DataFrame, list]) -> pd.DataFrame:
        """Extends sklearn syntax"""
        if type(bundles) == list:
            bundles = pd.DataFrame(bundles)

        if self.context == "systolic":
            return self._base_transform(bundles)
        else:
            return self._alt_transform(bundles)

    @staticmethod
    def _base_transform(bundles, tolerance = 7):
        """ "
            MinMx, then parse to 0-100 int
        """

        bundles["y"] = bundles["entry"].apply(lambda x: len(x))
        bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
        bundles["score"] = bundles["y"].apply(lambda x: int(x * 100))
        bundles["group"] = bundles["score"].apply(
            lambda x: "pass" if x > tolerance else "fail")

        bundles = bundles.sort_values(['group','score']).reset_index(drop=True)
        print(bundles['group'].value_counts())
        return bundles

    @staticmethod
    def _alt_transform(bundles):
        """ "
        StandardScaler, capped, with minmax, then parse to 0-100 int
        """

        bundles["y"] = bundles["entry"].apply(lambda x: len(x))
        bundles[["y"]] = StandardScaler().fit_transform(bundles[["y"]])

        def _cap_z(x, sigma=3):
            if x > sigma:
                return sigma
            elif x < (-1 * sigma):
                return -1 * sigma
            else:
                return x

        bundles["y"] = bundles["y"].apply(_cap_z)
        bundles[["y"]] = MinMaxScaler().fit_transform(bundles[["y"]])
        bundles["score"] = bundles["y"].apply(lambda x: int(x * 100))
        bundles["group"] = bundles["score"].apply(
            lambda x: "pass" if x > 7 else "fail")

        bundles = bundles.sort_values(['group','score']).reset_index(drop=True)
        print(bundles['group'].value_counts())
        return bundles

    

    def visualize(self, scored_bundles: pd.DataFrame) -> None:
        scored_bundles = self.fit_transform(scored_bundles)
        px.histogram(
            scored_bundles.sort_values("group"),
            x="score",
            facet_col="group",
            title=f'{dict(scored_bundles["group"].value_counts())}',
        ).show()
