# Copyright (c) 2022 Mario S. Könz; License: MIT
import dataclasses as dc
import enum
import typing as tp
from pathlib import Path

from django.core.files import File
from django.db import models

from ._create_django_model import InspectDataclass
from ._decorator import BACKEND_LINKER
from ._decorator import django_model
from ._protocols import T


@dc.dataclass
class DjangoStore:
    identifier: str

    def dump(self, dc_obj: tp.Any) -> tuple[models.Model, bool]:
        kwgs, m2m = self.dataclass_to_django(dc_obj)
        identifying, defaults = self._split_of_pk(dc_obj, kwgs)
        dj_obj, created = self.backend_manager(dc_obj).update_or_create(
            **identifying, defaults=defaults
        )

        for key, vals in m2m.items():
            # remove old ones
            if not created:
                getattr(dj_obj, key).clear()
            for val in vals:
                sub_dj_obj, _ = self.dump(val)
                getattr(dj_obj, key).add(sub_dj_obj)

        return dj_obj, created

    def load(self, dataclass: type[T], **filter_kwgs: tp.Any) -> T:
        instance = self.django_load(dataclass, **filter_kwgs)
        return self.django_to_dataclass(instance)  # type: ignore

    def django_load(self, dataclass: type[T], **filter_kwgs: tp.Any) -> models.Model:
        manager = self.backend_manager(dataclass)
        hits = manager.filter(**filter_kwgs).all()
        if len(hits) > 1:
            raise RuntimeError(
                f"found {len(hits)} entries matching filter_kwgs {filter_kwgs}, be more specific!"
            )
        if len(hits) == 0:
            raise RuntimeError(f"found no entries matching filter_kwgs {filter_kwgs}!")
        return hits[0]  # type: ignore

    def dataclass_to_django(self, dc_obj: tp.Any) -> tp.Any:
        model = django_model(dc_obj)
        kwgs = {}
        m2m = {}
        for field in dc.fields(dc_obj):
            key = field.name
            val = getattr(dc_obj, key)
            if type(val) in BACKEND_LINKER.dc_to_backend:
                val, _ = self.dump(val)
            if isinstance(val, enum.Enum):
                val = val.value
            if isinstance(val, Path):
                val = File(
                    open(val, "rb"),  # pylint: disable=consider-using-with
                    name=val.name,
                )

            # pylint: disable=protected-access
            dj_model = model._meta.get_field(key)
            if isinstance(dj_model, models.ManyToManyField):
                m2m[key] = val
            else:
                kwgs[key] = val

        return kwgs, m2m

    def django_to_dataclass(self, dj_obj: models.Model) -> tp.Any:
        dataclass = BACKEND_LINKER.backend_to_dc[type(dj_obj)]
        obj_kwgs = {}
        for field in dc.fields(dataclass):
            key = field.name
            val = getattr(dj_obj, key)
            if type(val) in BACKEND_LINKER.backend_to_dc:
                val = self.django_to_dataclass(val)
            field = [field for field in dc.fields(dataclass) if field.name == key][0]
            if issubclass(field.type, enum.Enum):
                val = field.type(val)
            if issubclass(field.type, Path):
                val = Path(val.url)
            # pylint: disable=protected-access
            if isinstance(dj_obj._meta.get_field(key), models.ManyToManyField):
                val = {self.django_to_dataclass(x) for x in val.all()}

            obj_kwgs[field.name] = val
        return dataclass(**obj_kwgs)

    parse = django_to_dataclass

    def backend_manager(self, dataclass: type[T]) -> tp.Any:
        return django_model(dataclass).objects.using(self.identifier)

    @classmethod
    def _split_of_pk(
        cls, dc_obj: tp.Any, kwgs: dict[str, tp.Any]
    ) -> tuple[dict[str, tp.Any], dict[str, tp.Any]]:
        ident_keys = InspectDataclass(dc_obj).get_identifying_parameter()
        return (
            {key: kwgs[key] for key in kwgs.keys() & ident_keys},
            {key: kwgs[key] for key in kwgs.keys() ^ ident_keys},
        )
