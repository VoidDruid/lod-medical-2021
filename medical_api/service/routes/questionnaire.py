# pylint: disable=C0413

from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

import crud
from service.api import Api
from service.dependencies import get_postgres


api: Api = Api(tags=["Questions"])
