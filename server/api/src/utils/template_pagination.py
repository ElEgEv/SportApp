from fastapi_pagination import Params

# create or update params for pagination in template
def get_pagination_params(page: int = 1, size: int = 15) -> Params:
    return Params(page=page, size=size)