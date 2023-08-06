from __future__ import annotations

from typing import Optional, Union

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables
from django_tables2.utils import A, Accessor

from .models import LessonPeriod, Supervision


def _css_class_from_lesson_or_supervision_state(
    record: Optional[Union[LessonPeriod, Supervision]] = None,
    table: Optional[Union[LessonsTable, SupervisionsTable]] = None,
) -> str:
    """Return CSS class depending on lesson or supervision state."""
    if record.get_substitution():
        if hasattr(record.get_substitution(), "cancelled") and record.get_substitution().cancelled:
            return "success"
        else:
            return "warning"
    else:
        return ""


class SubstitutionColumn(tables.Column):
    def render(self, value, record: Optional[Union[LessonPeriod, Supervision]] = None):
        if record.get_substitution():
            return format_html(
                "<s>{}</s> → {}",
                value,
                self.substitution_accessor.resolve(record.get_substitution()),
            )
        return value

    def __init__(self, *args, **kwargs):
        self.substitution_accessor = Accessor(kwargs.pop("substitution_accessor"))
        super().__init__(*args, **kwargs)


class LessonsTable(tables.Table):
    """Table for daily lessons and management of substitutions."""

    class Meta:
        attrs = {"class": "highlight"}
        row_attrs = {"class": _css_class_from_lesson_or_supervision_state}

    period__period = tables.Column(accessor="period__period")
    lesson__groups = tables.Column(accessor="lesson__group_names", verbose_name=_("Groups"))
    lesson__teachers = SubstitutionColumn(
        accessor="lesson__teacher_names",
        substitution_accessor="teacher_names",
        verbose_name=_("Teachers"),
    )
    lesson__subject = SubstitutionColumn(
        accessor="lesson__subject", substitution_accessor="subject"
    )
    room = SubstitutionColumn(accessor="room", substitution_accessor="room")
    edit_substitution = tables.LinkColumn(
        "edit_substitution",
        args=[A("id"), A("_week")],
        text=_("Substitution"),
        attrs={"a": {"class": "btn-flat waves-effect waves-orange"}},
        verbose_name=_("Manage substitution"),
    )


class SupervisionsTable(tables.Table):
    """Table for daily supervisions and management of substitutions."""

    class Meta:
        attrs = {"class": "highlight"}
        row_attrs = {"class": _css_class_from_lesson_or_supervision_state}

    break_item = tables.Column(accessor="break_item")
    area = tables.Column(accessor="area")
    teacher = SubstitutionColumn(
        accessor="teacher",
        substitution_accessor="teacher",
        verbose_name=_("Teachers"),
    )
    edit_substitution = tables.LinkColumn(
        "edit_supervision_substitution",
        args=[A("id"), A("_week")],
        text=_("Substitution"),
        attrs={"a": {"class": "btn-flat waves-effect waves-orange"}},
        verbose_name=_("Manage substitution"),
    )
