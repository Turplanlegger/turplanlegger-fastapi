from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from starlette.exceptions import HTTPException as StarletteHTTPException

class ApiProblem(Exception):
    def __init__(
        self,
        title: Optional[str] = None,
        detail: Optional[str] = None,
        status: Optional[int] = None,
        type: Optional[str] = None,
        instance: Optional[str] = None,
        **kwargs
    ) -> None:
        self.title: str = title
        self.detail: Optional[str] = detail
        self.status: int = status or 500
        self.type: str = type or 'about:blank'
        self.instance: str = instance or request.url
        self.kwargs: Dict = kwargs


def register_problem_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(ApiProblem)
    async def problem_exception_handler(request: Request, problem: ApiProblem):
        return JSONResponse(
            content={
                'type': problem.type,
                'status': problem.status,
                'title': problem.title,
                'detail': problem.detail,
                'instance': problem.instance
            },
            status_code=problem.status,
            media_type='application/problem+json'
        )


    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        print('#################')
        print('#################')
        print('#################')
        print(exc.detail)
        problem = ApiProblem(
            title=exc.detail[0].type,
            detail=exc.detail[0].msg,
            status=exc.detail[0].status,
            instance=request.url,
        )
        return JSONResponse(
            content={
                'type': problem.type,
                'status': problem.status,
                'title': problem.title,
                'detail': problem.detail,
                'instance': problem.instance
            },
            status_code=problem.status,
            media_type='application/problem+json'
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        problem = ApiProblem(
            title=exc.type,
            detail=exc.msg,
            status=exc.status,
            instance=request.url,
            **exc
        )
        return JSONResponse(
            content={
                'type': problem.type,
                'status': problem.status,
                'title': problem.title,
                'detail': problem.detail,
                'instance': problem.instance
            },
            status_code=problem.status,
            media_type='application/problem+json'
        )