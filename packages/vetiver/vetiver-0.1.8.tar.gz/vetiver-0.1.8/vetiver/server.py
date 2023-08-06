from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from fastapi import testclient

import uvicorn
import requests
import pandas as pd
from typing import Callable, Union, List

from .vetiver_model import VetiverModel
from .utils import _jupyter_nb


class VetiverAPI:
    """Create model aware API

    Parameters
    ----------
    model :  VetiverModel
        Model to be deployed in API
    check_ptype : bool
        Determine if data prototype should be enforced
    app_factory :
        Type of API to be deployed

    Example
    -------
    >>> import vetiver
    >>> X, y = vetiver.get_mock_data()
    >>> model = vetiver.get_mock_model().fit(X, y)
    >>> v = vetiver.VetiverModel(model = model, model_name = "my_model", ptype_data = X)
    >>> v_api = vetiver.VetiverAPI(model = v, check_ptype = True)
    """

    app = None

    def __init__(
        self,
        model: VetiverModel,
        check_ptype: bool = True,
        app_factory=FastAPI,
    ) -> None:
        self.model = model
        self.check_ptype = check_ptype
        self.app_factory = app_factory
        self.app = self._init_app()

    def _init_app(self):
        app = self.app_factory()
        app.openapi = self._custom_openapi

        @app.get("/", include_in_schema=False)
        def docs_redirect():

            redirect = "__docs__"

            return RedirectResponse(redirect)

        if self.model.metadata.get("url") is not None:

            @app.get("/pin-url")
            def pin_url():
                return repr(self.model.metadata.get("url"))

        @app.get("/ping", include_in_schema=True)
        async def ping():
            return {"ping": "pong"}

        if self.check_ptype is True:

            @app.post("/predict")
            async def prediction(
                input_data: Union[self.model.ptype, List[self.model.ptype]]
            ):
                if isinstance(input_data, List):
                    served_data = _batch_data(input_data)
                else:
                    served_data = _prepare_data(input_data)

                y = self.model.handler_predict(
                    served_data, check_ptype=self.check_ptype
                )

                return {"prediction": y.tolist()}

        elif self.check_ptype is False:

            @app.post("/predict")
            async def prediction(input_data: Request):
                y = await input_data.json()

                prediction = self.model.handler_predict(y, check_ptype=self.check_ptype)

                return {"prediction": prediction.tolist()}

        else:
            raise ValueError("cannot determine `check_ptype`")

        @app.get("/__docs__", response_class=HTMLResponse, include_in_schema=False)
        async def rapidoc():
            return f"""
                    <!doctype html>
                    <html>
                        <head>
                        <meta name="viewport"
                        content="width=device-width,minimum-scale=1,initial-scale=1,user-scalable=yes">
                        <title>RapiDoc</title>
                        <script type="module"
                        src="https://unpkg.com/rapidoc@9.3.3/dist/rapidoc-min.js"></script>
                        </script></head>
                        <body>
                            <rapi-doc spec-url="{self.app.openapi_url[1:]}"
                            id="thedoc"
                            render-style="read"
                            schema-style="tree"
                            show-components="true"
                            show-info="true"
                            show-header="true"
                            allow-search="true"
                            show-side-nav="false"
                            allow-authentication="false"
                            update-route="false"
                            match-type="regex"
                            theme="light"
                            header-color="#F2C6AC"
                            primary-color = "#8C2D2D">
                            <img
                            slot="logo"
                            width="55"
                            src="https://raw.githubusercontent.com/rstudio/hex-stickers/master/SVG/vetiver.svg"
                            </rapi-doc>
                        </body>
                    </html>
            """

        return app

    def vetiver_post(
        self, endpoint_fx: Callable, endpoint_name: str = "custom_endpoint"
    ):
        """Create new POST endpoint that is aware of model input data

        Parameters
        ----------
        endpoint_fx : typing.Callable
            Custom function to be run at endpoint
        endpoint_name : str
            Name of endpoint

        Example
        -------
        >>> import vetiver
        >>> X, y = vetiver.get_mock_data()
        >>> model = vetiver.get_mock_model().fit(X, y)
        >>> v = vetiver.VetiverModel(model = model, model_name = "model", ptype_data = X)
        >>> v_api = vetiver.VetiverAPI(model = v, check_ptype = True)
        >>> def sum_values(x):
        ...     return x.sum()
        >>> v_api.vetiver_post(sum_values, "sums")
        """
        if self.check_ptype is True:

            @self.app.post("/" + endpoint_name)
            async def custom_endpoint(input_data: self.model.ptype):
                y = _prepare_data(input_data)
                new = endpoint_fx(pd.DataFrame(y))
                return {endpoint_name: new.tolist()}

        else:

            @self.app.post("/" + endpoint_name)
            async def custom_endpoint(input_data: Request):
                y = await input_data.json()
                new = endpoint_fx(pd.DataFrame(y))

                return {endpoint_name: new.tolist()}

    def run(self, port: int = 8000, host: str = "127.0.0.1", **kw):
        """
        Start API

        Parameters
        ----------
        port : int
            An integer that indicates the server port that should be listened on.
        host : str
            A valid IPv4 or IPv6 address, which the application will listen on.

        Example
        -------
        >>> import vetiver
        >>> X, y = vetiver.get_mock_data()
        >>> model = vetiver.get_mock_model().fit(X, y)
        >>> v = vetiver.VetiverModel(model = model, model_name = "model", ptype_data = X)
        >>> v_api = vetiver.VetiverAPI(model = v, check_ptype = True)
        >>> v_api.run()     # doctest: +SKIP
        """
        _jupyter_nb()
        uvicorn.run(self.app, port=port, host=host, **kw)

    def _custom_openapi(self):
        import vetiver

        if self.app.openapi_schema:
            return self.app.openapi_schema
        openapi_schema = get_openapi(
            title=self.model.model_name + " model API",
            version=vetiver.__version__,
            description=self.model.description,
            routes=self.app.routes,
            servers=self.app.servers,
        )
        openapi_schema["info"]["x-logo"] = {"url": "../docs/figures/logo.svg"}
        self.app.openapi_schema = openapi_schema
        return self.app.openapi_schema


def predict(endpoint, data: Union[dict, pd.DataFrame, pd.Series], **kw):
    """Make a prediction from model endpoint

    Parameters
    ----------
    endpoint :
        URI path to endpoint
    data : Union[dict, pd.DataFrame, pd.Series]
        Name of endpoint

    Returns
    -------
    dict
        Endpoint_name and list of endpoint_fx output

    Example
    -------
    >>> import vetiver
    >>> X, y = vetiver.get_mock_data()
    >>> endpoint = vetiver.vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    >>> vetiver.predict(endpoint, X)     # doctest: +SKIP
    """
    if isinstance(endpoint, testclient.TestClient):
        requester = endpoint
        endpoint = "/predict"
    else:
        requester = requests

    # TO DO: arrow format

    if isinstance(data, pd.DataFrame):
        data_json = data.to_json(orient="records")
        response = requester.post(endpoint, data=data_json, **kw)
    elif isinstance(data, pd.Series):
        data_dict = data.to_json()
        response = requester.post(endpoint, data=data_dict, **kw)
    elif isinstance(data, dict):
        response = requester.post(endpoint, json=data, **kw)
    else:
        try:
            response = requester.post(endpoint, json=data, **kw)
        except TypeError:
            raise TypeError(
                f"Predict expects a DataFrame or dict. Given type is {type(data)}"
            )

    response_df = pd.DataFrame.from_dict(response.json())

    if isinstance(response_df.iloc[0, 0], dict):
        if "type_error.dict" in response_df.iloc[0, 0].values():
            raise TypeError(
                f"Predict expects a DataFrame or dict. Given type is {type(data)}"
            )

    return response_df


def _prepare_data(pred_data):
    served_data = []
    for key, value in pred_data:
        served_data.append(value)
    return served_data


def _batch_data(pred_data):
    columns = pred_data[0].dict().keys()

    data = [line.dict() for line in pred_data]

    served_data = pd.DataFrame(data, columns=columns)
    return served_data


def vetiver_endpoint(url="http://127.0.0.1:8000/predict"):
    """Wrap url where VetiverModel will be deployed

    Parameters
    ----------
    url : str
        URI path to endpoint

    Returns
    -------
    url : str
        URI path to endpoint

    Example
    -------
    >>> import vetiver
    >>> endpoint = vetiver.vetiver_endpoint(url='http://127.0.0.1:8000/predict')
    """
    return url
