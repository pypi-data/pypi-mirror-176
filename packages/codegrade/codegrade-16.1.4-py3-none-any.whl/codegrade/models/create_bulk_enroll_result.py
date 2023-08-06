"""The module that defines the ``CreateBulkEnrollResult`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .job import Job
from .user_info_with_role import UserInfoWithRole


@dataclass
class CreateBulkEnrollResult:
    """Processed users in a bulk enroll request."""

    #: The job sending out the mails.
    task: "Job"
    #: List of user not created because of incompatibility with SSO
    sso_incompatible_users: "t.Sequence[UserInfoWithRole]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "task",
                parsers.ParserFor.make(Job),
                doc="The job sending out the mails.",
            ),
            rqa.RequiredArgument(
                "sso_incompatible_users",
                rqa.List(parsers.ParserFor.make(UserInfoWithRole)),
                doc=(
                    "List of user not created because of incompatibility"
                    " with SSO"
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "task": to_dict(self.task),
            "sso_incompatible_users": to_dict(self.sso_incompatible_users),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["CreateBulkEnrollResult"], d: t.Dict[str, t.Any]
    ) -> "CreateBulkEnrollResult":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            task=parsed.task,
            sso_incompatible_users=parsed.sso_incompatible_users,
        )
        res.raw_data = d
        return res
