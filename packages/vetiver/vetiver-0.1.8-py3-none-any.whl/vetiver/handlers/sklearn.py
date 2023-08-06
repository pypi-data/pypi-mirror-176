import pandas as pd
import sklearn

from ..meta import _model_meta
from .base import BaseHandler


class SKLearnHandler(BaseHandler):
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        a trained sklearn model
    """

    model_class = staticmethod(lambda: sklearn.base.BaseEstimator)

    def describe(self):
        """Create description for sklearn model"""
        desc = f"Scikit-learn {self.model.__class__} model"
        return desc

    def create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
        required_pkgs = required_pkgs + ["scikit-learn"]
        meta = _model_meta(user, version, url, required_pkgs)

        return meta

    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """

        if not check_ptype or isinstance(input_data, pd.DataFrame):
            prediction = self.model.predict(input_data)
        else:
            prediction = self.model.predict([input_data])

        return prediction
