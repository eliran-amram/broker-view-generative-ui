from typing import Any, Dict, Optional

from fastapi import HTTPException


class ServiceBaseException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        status_code: int = 500,
        message=None,
        headers: Optional[Dict[str, str]] = None,
        should_log_exception=True,
    ):
        self.should_log_exception = getattr(
            self, 'should_log_exception', should_log_exception
        )
        self.message = getattr(self, 'message', message)
        super().__init__(status_code, detail=detail, headers=headers)
