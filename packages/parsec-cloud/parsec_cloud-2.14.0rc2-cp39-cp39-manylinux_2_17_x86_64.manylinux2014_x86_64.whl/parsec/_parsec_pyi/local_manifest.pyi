from __future__ import annotations
from typing import Any, Dict, FrozenSet, Optional, Set, Tuple, Union

from parsec.crypto import SecretKey
from parsec._parsec_pyi.ids import ChunkID, DeviceID, EntryID
from parsec._parsec_pyi.manifest import (
    BlockAccess,
    EntryName,
    FileManifest,
    FolderManifest,
    UserManifest,
    WorkspaceEntry,
    WorkspaceManifest,
)
from parsec._parsec_pyi.time import DateTime
from parsec._parsec_pyi.regex import Regex

AnyLocalManifest = Union[
    LocalFileManifest,
    LocalFolderManifest,
    LocalWorkspaceManifest,
    LocalUserManifest,
]

class Chunk:
    def __init__(
        self,
        id: ChunkID,
        start: int,
        stop: int,
        raw_offset: int,
        raw_size: int,
        access: Optional[BlockAccess],
    ) -> None: ...
    def __lt__(self, other: int) -> bool: ...
    def __gt__(self, other: int) -> bool: ...
    def __le__(self, other: int) -> bool: ...
    def __ge__(self, other: int) -> bool: ...
    @property
    def id(self) -> ChunkID: ...
    @property
    def start(self) -> int: ...
    @property
    def stop(self) -> int: ...
    @property
    def raw_offset(self) -> int: ...
    @property
    def raw_size(self) -> int: ...
    @property
    def access(self) -> Optional[BlockAccess]: ...
    def evolve(
        self,
        id: Optional[ChunkID] = None,
        start: Optional[int] = None,
        stop: Optional[int] = None,
        raw_offset: Optional[int] = None,
        raw_size: Optional[int] = None,
        access: Optional[BlockAccess] = None,
    ) -> Chunk: ...
    def evolve_as_block(self, data: bytes) -> Chunk: ...
    def is_block(self) -> bool: ...
    def is_pseudo_block(self) -> bool: ...
    def get_block_access(self) -> BlockAccess: ...
    @classmethod
    def from_block_access(cls, block_access: BlockAccess) -> Chunk: ...
    @classmethod
    def new(cls, start: int, stop: int) -> Chunk: ...

Chunks = Tuple[Chunk, ...]

class LocalFileManifest:
    def __init__(
        self,
        base: FileManifest,
        need_sync: bool,
        updated: DateTime,
        size: int,
        blocksize: int,
        blocks: Tuple[Chunks, ...],
    ) -> None: ...
    @property
    def base_version(self) -> int: ...
    @property
    def id(self) -> EntryID: ...
    @property
    def created(self) -> DateTime: ...
    @property
    def is_placeholder(self) -> bool: ...
    @property
    def parent(self) -> EntryID: ...
    @property
    def base(self) -> FileManifest: ...
    @property
    def need_sync(self) -> bool: ...
    @property
    def updated(self) -> DateTime: ...
    @property
    def size(self) -> int: ...
    @property
    def blocksize(self) -> int: ...
    @property
    def blocks(self) -> Tuple[Chunks, ...]: ...
    def evolve(
        self,
        base: Optional[FileManifest] = None,
        need_sync: Optional[bool] = None,
        updated: Optional[DateTime] = None,
        size: Optional[int] = None,
        blocksize: Optional[int] = None,
        blocks: Optional[Tuple[Chunks, ...]] = None,
    ) -> LocalFileManifest: ...
    def evolve_single_block(self, block: int, new_chunk: Chunk) -> LocalFileManifest: ...
    def evolve_and_mark_updated(
        self,
        timestamp: DateTime,
        base: Optional[FileManifest] = None,
        updated: Optional[DateTime] = None,
        size: Optional[int] = None,
        blocksize: Optional[int] = None,
        blocks: Optional[Tuple[Chunks, ...]] = None,
        **kwargs: Any,
    ) -> LocalFileManifest: ...
    def get_chunks(self, block: int) -> Tuple[Chunk, ...]: ...
    def is_reshaped(self) -> bool: ...
    def assert_integrity(self) -> None: ...
    def to_remote(self, author: DeviceID, timestamp: DateTime) -> FileManifest: ...
    def match_remote(self, remote_manifest: FileManifest) -> bool: ...
    def to_stats(self) -> Dict[str, Any]: ...
    def asdict(self) -> Dict[str, Any]: ...
    def dump_and_encrypt(self, key: SecretKey) -> bytes: ...
    @classmethod
    def decrypt_and_load(self, encrypted: bytes, key: SecretKey) -> LocalFileManifest: ...
    @classmethod
    def from_remote(cls, remote: FileManifest) -> LocalFileManifest: ...
    @classmethod
    def from_remote_with_local_context(
        cls,
        remote: FileManifest,
        prevent_sync_pattern: Regex,
        local_manifest: LocalFileManifest,
        timestamp: DateTime,
    ) -> LocalFileManifest: ...
    @classmethod
    def new_placeholder(
        cls,
        author: DeviceID,
        parent: EntryID,
        timestamp: DateTime,
        blocksize: int = 512 * 1024,
    ) -> LocalFileManifest: ...

class LocalFolderManifest:
    def __init__(
        self,
        base: FolderManifest,
        need_sync: bool,
        updated: DateTime,
        children: Dict[EntryName, EntryID],
        local: FrozenSet[EntryID],
        remote: FrozenSet[EntryID],
    ) -> None: ...
    @property
    def base_version(self) -> int: ...
    @property
    def id(self) -> EntryID: ...
    @property
    def created(self) -> DateTime: ...
    @property
    def is_placeholder(self) -> bool: ...
    @property
    def parent(self) -> EntryID: ...
    @property
    def base(self) -> FolderManifest: ...
    @property
    def need_sync(self) -> bool: ...
    @property
    def updated(self) -> DateTime: ...
    @property
    def children(self) -> Dict[EntryName, EntryID]: ...
    @property
    def local_confinement_points(self) -> Set[EntryID]: ...
    @property
    def remote_confinement_points(self) -> Set[EntryID]: ...
    def match_remote(self, remote_manifest: FolderManifest) -> bool: ...
    def evolve(
        self,
        base: Optional[FolderManifest] = None,
        need_sync: Optional[bool] = None,
        updated: Optional[DateTime] = None,
        children: Optional[Dict[EntryName, EntryID]] = None,
        local: Optional[FrozenSet[EntryID]] = None,
        remote: Optional[FrozenSet[EntryID]] = None,
    ) -> LocalFolderManifest: ...
    def evolve_and_mark_updated(
        self,
        timestamp: DateTime,
        base: Optional[FolderManifest] = None,
        updated: Optional[DateTime] = None,
        children: Optional[Dict[EntryName, EntryID]] = None,
        local: Optional[FrozenSet[EntryID]] = None,
        remote: Optional[FrozenSet[EntryID]] = None,
    ) -> LocalFolderManifest: ...
    def evolve_children_and_mark_updated(
        self,
        data: Dict[EntryName, Optional[EntryID]],
        prevent_sync_pattern: Regex,
        timestamp: DateTime,
    ) -> LocalFolderManifest: ...
    def apply_prevent_sync_pattern(
        self, prevent_sync_pattern: Regex, timestamp: DateTime
    ) -> LocalFolderManifest: ...
    def to_remote(self, author: DeviceID, timestamp: DateTime) -> FolderManifest: ...
    def to_stats(self) -> Dict[str, Any]: ...
    def asdict(self) -> Dict[str, Any]: ...
    def dump_and_encrypt(self, key: SecretKey) -> bytes: ...
    @classmethod
    def decrypt_and_load(self, encrypted: bytes, key: SecretKey) -> LocalFolderManifest: ...
    @classmethod
    def new_placeholder(
        cls, author: DeviceID, parent: EntryID, timestamp: DateTime
    ) -> LocalFolderManifest: ...
    @classmethod
    def from_remote(
        cls, remote: FolderManifest, prevent_sync_pattern: Regex
    ) -> LocalFolderManifest: ...
    @classmethod
    def from_remote_with_local_context(
        cls,
        remote: FolderManifest,
        prevent_sync_pattern: Regex,
        local_manifest: AnyLocalManifest,
        timestamp: DateTime,
    ) -> LocalFolderManifest: ...

class LocalWorkspaceManifest:
    def __init__(
        self,
        base: WorkspaceManifest,
        need_sync: bool,
        updated: DateTime,
        children: Dict[EntryName, EntryID],
        local: FrozenSet[EntryID],
        remote: FrozenSet[EntryID],
        speculative: bool,
    ) -> None: ...
    @property
    def base_version(self) -> int: ...
    @property
    def id(self) -> EntryID: ...
    @property
    def created(self) -> DateTime: ...
    @property
    def is_placeholder(self) -> bool: ...
    @property
    def base(self) -> WorkspaceManifest: ...
    @property
    def need_sync(self) -> bool: ...
    @property
    def updated(self) -> DateTime: ...
    @property
    def children(self) -> Dict[EntryName, EntryID]: ...
    @property
    def local_confinement_points(self) -> Set[EntryID]: ...
    @property
    def remote_confinement_points(self) -> Set[EntryID]: ...
    @property
    def speculative(self) -> bool: ...
    def match_remote(self, remote_manifest: WorkspaceManifest) -> bool: ...
    def evolve(
        self,
        base: Optional[WorkspaceManifest] = None,
        need_sync: Optional[bool] = None,
        updated: Optional[DateTime] = None,
        children: Optional[Dict[EntryName, EntryID]] = None,
        local: Optional[FrozenSet[EntryID]] = None,
        remote: Optional[FrozenSet[EntryID]] = None,
        speculative: Optional[bool] = None,
    ) -> LocalWorkspaceManifest: ...
    def evolve_and_mark_updated(
        self,
        timestamp: DateTime,
        base: Optional[WorkspaceManifest] = None,
        updated: Optional[DateTime] = None,
        children: Optional[Dict[EntryName, EntryID]] = None,
        local: Optional[FrozenSet[EntryID]] = None,
        remote: Optional[FrozenSet[EntryID]] = None,
        speculative: Optional[bool] = None,
    ) -> LocalWorkspaceManifest: ...
    def evolve_children_and_mark_updated(
        self,
        data: Dict[EntryName, Optional[EntryID]],
        prevent_sync_pattern: Regex,
        timestamp: DateTime,
    ) -> LocalWorkspaceManifest: ...
    def apply_prevent_sync_pattern(
        self, prevent_sync_pattern: Regex, timestamp: DateTime
    ) -> LocalWorkspaceManifest: ...
    def to_remote(self, author: DeviceID, timestamp: DateTime) -> WorkspaceManifest: ...
    def to_stats(self) -> Dict[str, Any]: ...
    def asdict(self) -> Dict[str, Any]: ...
    def dump_and_encrypt(self, key: SecretKey) -> bytes: ...
    @classmethod
    def decrypt_and_load(cls, encrypted: bytes, key: SecretKey) -> LocalWorkspaceManifest: ...
    @classmethod
    def new_placeholder(
        cls,
        author: DeviceID,
        timestamp: DateTime,
        id: Optional[EntryID],
        speculative: bool,
    ) -> LocalWorkspaceManifest: ...
    @classmethod
    def from_remote(
        cls, remote: WorkspaceManifest, prevent_sync_pattern: Regex
    ) -> LocalWorkspaceManifest: ...
    @classmethod
    def from_remote_with_local_context(
        cls,
        remote: WorkspaceManifest,
        prevent_sync_pattern: Regex,
        local_manifest: AnyLocalManifest,
        timestamp: DateTime,
    ) -> LocalWorkspaceManifest: ...

class LocalUserManifest:
    def __init__(
        self,
        base: UserManifest,
        need_sync: bool,
        updated: DateTime,
        last_processed_message: int,
        workspaces: Tuple[WorkspaceEntry, ...],
        speculative: bool,
    ) -> None: ...
    @property
    def base_version(self) -> int: ...
    @property
    def id(self) -> EntryID: ...
    @property
    def created(self) -> DateTime: ...
    @property
    def is_placeholder(self) -> bool: ...
    @property
    def base(self) -> UserManifest: ...
    @property
    def need_sync(self) -> bool: ...
    @property
    def updated(self) -> DateTime: ...
    @property
    def last_processed_message(self) -> int: ...
    @property
    def workspaces(self) -> Tuple[WorkspaceEntry, ...]: ...
    @property
    def speculative(self) -> bool: ...
    def evolve(
        self,
        base: Optional[UserManifest] = None,
        need_sync: Optional[bool] = None,
        updated: Optional[DateTime] = None,
        last_processed_message: Optional[int] = None,
        workspaces: Optional[Tuple[WorkspaceEntry, ...]] = None,
        speculative: Optional[bool] = None,
    ) -> LocalUserManifest: ...
    def evolve_and_mark_updated(
        self,
        timestamp: DateTime,
        base: Optional[UserManifest] = None,
        last_processed_message: Optional[int] = None,
        workspaces: Optional[Tuple[WorkspaceEntry, ...]] = None,
        speculative: Optional[bool] = None,
        **kwargs: Any,
    ) -> LocalUserManifest: ...
    def evolve_workspaces_and_mark_updated(
        self, timestamp: DateTime, workspace: WorkspaceEntry
    ) -> LocalUserManifest: ...
    def evolve_workspaces(self, workspace: WorkspaceEntry) -> LocalUserManifest: ...
    def get_workspace_entry(self, workspace_id: EntryID) -> Optional[WorkspaceEntry]: ...
    def to_remote(self, author: DeviceID, timestamp: DateTime) -> UserManifest: ...
    def match_remote(self, remote_manifest: UserManifest) -> bool: ...
    def to_stats(self) -> Dict[str, Any]: ...
    def asdict(self) -> Dict[str, Any]: ...
    def dump_and_encrypt(self, key: SecretKey) -> bytes: ...
    @classmethod
    def decrypt_and_load(cls, encrypted: bytes, key: SecretKey) -> LocalUserManifest: ...
    @classmethod
    def new_placeholder(
        cls,
        author: DeviceID,
        timestamp: DateTime,
        id: Optional[EntryID],
        speculative: bool,
    ) -> LocalUserManifest: ...
    @classmethod
    def from_remote(cls, remote: UserManifest) -> LocalUserManifest: ...
    @classmethod
    def from_remote_with_local_context(
        cls,
        remote: UserManifest,
        prevent_sync_pattern: Regex,
        local_manifest: LocalUserManifest,
        timestamp: DateTime,
    ) -> LocalUserManifest: ...

def local_manifest_decrypt_and_load(encrypted: bytes, key: SecretKey) -> AnyLocalManifest: ...
