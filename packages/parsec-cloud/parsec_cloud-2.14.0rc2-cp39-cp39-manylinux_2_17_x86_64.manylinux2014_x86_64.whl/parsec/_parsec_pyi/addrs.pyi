from __future__ import annotations
from typing import Any, Optional, Union
from parsec._parsec import (
    DateTime,
    OrganizationID,
    VerifyKey,
    EntryID,
    InvitationToken,
    InvitationType,
)

class BackendAddr:
    def __init__(self, hostname: str, port: Optional[int], use_ssl: bool) -> None: ...
    def __lt__(self, other: BackendAddr) -> bool: ...
    def __gt__(self, other: BackendAddr) -> bool: ...
    def __le__(self, other: BackendAddr) -> bool: ...
    def __ge__(self, other: BackendAddr) -> bool: ...
    def __hash__(self) -> int: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    def to_url(self) -> str: ...
    def to_http_domain_url(self, path: str = "") -> str: ...
    def to_http_redirection_url(self) -> str: ...
    @classmethod
    def from_url(cls, url: str, allow_http_redirection: bool = False) -> BackendAddr: ...

class BackendOrganizationAddr(BackendAddr):
    def __init__(
        self,
        organization_id: OrganizationID,
        root_verify_key: VerifyKey,
        hostname: str,
        port: Optional[int],
        use_ssl: bool = True,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def organization_id(self) -> OrganizationID: ...
    @property
    def root_verify_key(self) -> VerifyKey: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    def get_backend_addr(self) -> BackendAddr: ...
    def to_url(self) -> str: ...
    def to_http_redirection_url(self) -> str: ...
    @classmethod
    def from_url(
        cls, url: str, allow_http_redirection: bool = False
    ) -> BackendOrganizationAddr: ...
    @classmethod
    def build(
        cls,
        backend_addr: BackendAddr,
        organization_id: OrganizationID,
        root_verify_key: VerifyKey,
    ) -> BackendOrganizationAddr: ...

class BackendActionAddr:
    @classmethod
    def from_url(
        cls, url: str, allow_http_redirection: bool = False
    ) -> Union[
        BackendOrganizationBootstrapAddr,
        BackendOrganizationFileLinkAddr,
        BackendInvitationAddr,
        BackendPkiEnrollmentAddr,
    ]: ...

class BackendOrganizationBootstrapAddr(BackendAddr):
    def __init__(
        self,
        organization_id: OrganizationID,
        token: Optional[str],
        hostname: str,
        port: Optional[int],
        use_ssl: bool = True,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def organization_id(self) -> OrganizationID: ...
    @property
    def token(self) -> Optional[str]: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    def generate_organization_addr(self, root_verify_key: VerifyKey) -> BackendOrganizationAddr: ...
    def get_backend_addr(self) -> BackendAddr: ...
    def to_url(self) -> str: ...
    def to_http_domain_url(self, path: str = "") -> str: ...
    def to_http_redirection_url(self) -> str: ...
    @classmethod
    def from_url(
        cls, url: str, allow_http_redirection: bool = False
    ) -> BackendOrganizationBootstrapAddr: ...
    @classmethod
    def build(
        cls,
        backend_addr: BackendAddr,
        organization_id: OrganizationID,
        token: Optional[str],
    ) -> BackendOrganizationBootstrapAddr: ...

class BackendOrganizationFileLinkAddr(BackendAddr):
    def __init__(
        self,
        organization_id: OrganizationID,
        workspace_id: EntryID,
        encrypted_path: bytes,
        hostname: str,
        port: Optional[int],
        use_ssl: bool = True,
        encrypted_timestamp: Optional[bytes] = None,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    @property
    def organization_id(self) -> OrganizationID: ...
    @property
    def workspace_id(self) -> EntryID: ...
    @property
    def encrypted_path(self) -> bytes: ...
    @property
    def encrypted_timestamp(self) -> Optional[bytes]: ...
    def get_backend_addr(self) -> BackendAddr: ...
    def to_url(self) -> str: ...
    def to_http_redirection_url(self) -> str: ...
    @classmethod
    def from_url(
        cls, url: str, allow_http_redirection: bool = False
    ) -> BackendOrganizationFileLinkAddr: ...
    @classmethod
    def build(
        cls,
        organization_addr: BackendOrganizationAddr,
        workspace_id: EntryID,
        encrypted_path: bytes,
        encrypted_timestamp: Optional[bytes] = None,
    ) -> BackendOrganizationFileLinkAddr: ...

class BackendInvitationAddr(BackendAddr):
    def __init__(
        self,
        organization_id: OrganizationID,
        invitation_type: Any,  # TODO: find correct type
        token: InvitationToken,
        hostname: str,
        port: Optional[int],
        use_ssl: bool = True,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    @property
    def organization_id(self) -> OrganizationID: ...
    @property
    def invitation_type(self) -> Any: ...
    @property
    def token(self) -> InvitationToken: ...
    def get_backend_addr(self) -> BackendAddr: ...
    def to_url(self) -> str: ...
    def to_http_redirection_url(self) -> str: ...
    def generate_organization_addr(self, root_verify_key: VerifyKey) -> BackendOrganizationAddr: ...
    @classmethod
    def from_url(cls, url: str, allow_http_redirection: bool = False) -> BackendInvitationAddr: ...
    @classmethod
    def build(
        cls,
        backend_addr: BackendAddr,
        organization_id: OrganizationID,
        invitation_type: InvitationType,
        token: InvitationToken,
    ) -> BackendInvitationAddr: ...

class BackendPkiEnrollmentAddr(BackendAddr):
    def __init__(
        self,
        organization_id: OrganizationID,
        hostname: str,
        port: Optional[int],
        use_ssl: bool = True,
    ) -> None: ...
    def __hash__(self) -> int: ...
    @property
    def hostname(self) -> str: ...
    @property
    def port(self) -> int: ...
    @property
    def use_ssl(self) -> bool: ...
    @property
    def netloc(self) -> str: ...
    @property
    def organization_id(self) -> OrganizationID: ...
    def get_backend_addr(self) -> BackendAddr: ...
    def to_url(self) -> str: ...
    def to_http_redirection_url(self) -> str: ...
    def to_http_domain_url(self, path: str = "") -> str: ...
    def generate_organization_addr(self, root_verify_key: VerifyKey) -> BackendOrganizationAddr: ...
    @classmethod
    def from_url(
        cls, url: str, allow_http_redirection: bool = False
    ) -> BackendPkiEnrollmentAddr: ...
    @classmethod
    def build(
        cls, backend_addr: BackendAddr, organization_id: OrganizationID
    ) -> BackendPkiEnrollmentAddr: ...
