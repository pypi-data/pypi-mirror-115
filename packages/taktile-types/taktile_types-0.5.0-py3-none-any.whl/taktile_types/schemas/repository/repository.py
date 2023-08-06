"""Repository related datastructures"""
import typing as t

from pydantic import UUID4, BaseModel

from taktile_types.enums.repository.access import AccessKind
from taktile_types.schemas.repository.pull_request import PullRequest


class Repository(BaseModel):
    """A repository"""

    id: UUID4
    name: str
    full_name: str
    private: bool
    installation_id: UUID4
    description: t.Optional[str] = None


class RepositoryExtended(Repository):
    """Repository with access and PR information"""

    access: AccessKind
    pull_requests: t.List[PullRequest]
