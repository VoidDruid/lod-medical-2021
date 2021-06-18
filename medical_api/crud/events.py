# pylint: disable=C0413

from functools import partial
from typing import Iterable, Optional, Type

from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from database import *
from database.base import Base


def get_events_query(
    model: Type[Base],
    period_number: Optional[int] = None,
    run_number: Optional[int] = None,
    track_number: Optional[int] = None,
    load_joins: bool = False,
) -> Iterable[File]:
    query = select(model)
    if load_joins:
        query = query.options(joinedload(model.file), joinedload(model.software))

    if period_number is not None:
        query = query.where(model.period_number == period_number)
    if run_number is not None:
        query = query.where(model.run_number == run_number)
    if track_number is not None:
        query = query.where(model.track_number == track_number)

    return query


get_bmn_events_query = partial(get_events_query, BMNEvent)


def get_src_events_query(
    period_number: Optional[int] = None,
    run_number: Optional[int] = None,
    track_number: Optional[int] = None,
    input_charge: Optional[float] = None,
    input_charge_min: Optional[float] = None,
    input_charge_max: Optional[float] = None,
    output_charge: Optional[float] = None,
    output_charge_min: Optional[float] = None,
    output_charge_max: Optional[float] = None,
    load_joins: bool = False,
) -> Iterable[File]:
    query = get_events_query(SRCEvent, period_number, run_number, track_number, load_joins)

    def _(arg, check):
        nonlocal query
        if arg is not None:
            query = query.where(check(arg))
    
    _(input_charge, lambda i: SRCEvent.input_charge == i)
    _(output_charge, lambda i: SRCEvent.output_charge == i)

    _(input_charge_min, lambda i: SRCEvent.input_charge >= i)
    _(output_charge_min, lambda i: SRCEvent.output_charge >= i)

    _(input_charge_max, lambda i: SRCEvent.input_charge <= i)
    _(output_charge_max, lambda i: SRCEvent.output_charge <= i)

    return query
