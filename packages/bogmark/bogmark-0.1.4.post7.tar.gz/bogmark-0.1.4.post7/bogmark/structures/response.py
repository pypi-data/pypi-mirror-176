from typing import Any, Generic, TypeVar
from warnings import warn

import msgpack
import orjson
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse

from bogmark.logger import get_logger
from bogmark.server.mixin import ConfigMixin

ReturnModel = TypeVar("ReturnModel", bound=ConfigMixin)


class BogmarkResponse(ORJSONResponse, Generic[ReturnModel]):
    total_time = None

    def __init__(
        self,
        content: Any,
        status_code: int,
        media_type: str = None,
        headers: dict = None,
        total_time: float = None,
        return_model=None,
    ) -> None:

        super().__init__(
            content=content,
            headers=headers,
            status_code=status_code,
            media_type=media_type,
        )
        self.status_code = status_code
        self.total_time = total_time
        self.logger = get_logger(__name__, type(self))
        self.return_model = return_model

    def render(self, content: Any) -> bytes:
        if isinstance(content, bytes):
            return content
        return orjson.dumps(content)

    @property
    def is_ok(self) -> bool:
        return self.status_code < 400

    @property
    def is_server_error(self) -> bool:
        return self.status_code >= 500

    def pydantic(self) -> ReturnModel:
        self.raise_for_status()

        if self.return_model is None:
            raise ValueError("return_model is None, cannot create model. Perhaps you want to update the connector?")

        return self.return_model.parse_obj(self.json())

    def to_python_object(self) -> Any:
        warn(
            "BogmarkResponse.to_python_object() is deprecated. Use BogmarkResponse.json() instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.json()

    def json(self) -> Any:
        """
        There may be situations when media_type may be returned with an
        explicit indication of encoding like `application/json; charset=utf-8`
        or even language settings, we don't know for sure. In this cases, the
        `==` operator does not work properly. To avoid this in the future we
        should use `in` operator.

        Media Types: https://www.iana.org/assignments/media-types/media-types.xhtml


        """

        # application/json
        if "json" in self.media_type:
            return orjson.loads(self.body)

        # application/x-msgpack
        if "x-msgpack" in self.media_type:
            return msgpack.unpackb(self.body, raw=False)
        self.logger.warning("Use 'body' property to get data.")

    def raise_for_status(self) -> None:
        if not self.is_ok:
            raise HTTPException(status_code=self.status_code, detail=self.json()["error"]["message"])

    def _get_return_model_name(self) -> str:
        return self.return_model.__name__ if self.return_model else "Unknown"

    def __repr__(self) -> str:
        """<BogmarkResponse[PartnerResponse] [200]>"""
        return f"<{type(self).__name__}[{self._get_return_model_name()}] [{self.status_code}]>"

    def __rich__(self) -> str:
        """Colored <BogdamrkResponse[PartnerResponse] [200]>"""
        model_name = self._get_return_model_name()
        return f"<[purple]{type(self).__name__}[/purple][[red]{model_name}[/red]] [{self.status_code}]>"


JsonResponse = BogmarkResponse
