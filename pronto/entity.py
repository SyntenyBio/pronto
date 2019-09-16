
import weakref
import typing
from typing import Callable, Optional, FrozenSet

from .definition import Definition
from .synonym import Synonym
from .pv import PropertyValue
from .xref import Xref

from .utils.repr import make_repr

if typing.TYPE_CHECKING:
    from .ontology import Ontology


class EntityData():
    pass


class Entity():

    _ontology: Callable[[], 'Ontology']
    _data: Callable[[], EntityData]

    __slots__ = ("__weakref__", "_ontology", "_data")

    def __init__(self, ontology: 'Ontology', data):
        self._ontology = weakref.ref(ontology)
        self._data = weakref.ref(data)

    # --- Magic Methods ------------------------------------------------------

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id < other.id

    def __le__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id <= other.id

    def __gt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id > other.id

    def __ge__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id >= other.id

    def __hash__(self):
        return hash((self.id))

    def __repr__(self):
        return make_repr(type(self).__name__, self.id, name=(self.name, None))

    # --- Data descriptors ---------------------------------------------------

    @property
    def alternate_ids(self) -> FrozenSet[str]:
        return frozenset(self._data().alternate_ids)

    @alternate_ids.setter
    def alternate_ids(self, ids: FrozenSet[str]):
        if __debug__:
            msg = "'alternate_ids' must be a set of str, not {}"
            if not isinstance(ids, (set, frozenset)):
                raise TypeError(msg.format(type(ids).__name__))
            for x in (x for x in ids if isinstance(x, str)):
                raise TypeError(msg.format(type(x).__name__))
        self._data().alternate_ids = set(ids)

    @property
    def annotations(self) -> FrozenSet[PropertyValue]:
        return frozenset(self._data().annotations)

    @property
    def anonymous(self) -> bool:
        return self._data().anonymous

    @anonymous.setter
    def anonymous(self, value: bool):
        if __debug__:
            if not isinstance(value, bool):
                msg = "'anonymous' must be bool, not {}"
                raise TypeError(msg.format(type(value).__name__))
        self._data().anonymous = value

    @property
    def builtin(self) -> bool:
        return self._data().builtin

    @builtin.setter
    def builtin(self, value: bool):
        if __debug__:
            if not isinstance(value, bool):
                msg = "'builtin' must be bool, not {}"
                raise TypeError(msg.format(type(value).__name__))
        self._data().builtin = value

    @property
    def comment(self) -> Optional[str]:
        return self._data().comment

    @comment.setter
    def comment(self, value: Optional[str]):
        if __debug__:
            if value is not None and not isinstance(value, str):
                msg = "'comment' must be str or None, not {}"
                raise TypeError(msg.format(type(value).__name__))
        self._data().comment = value

    @property
    def definition(self) -> Optional[Definition]:
        return self._data().definition

    @definition.setter
    def definition(self, definition: Optional[Definition]):
        if __debug__:
            if definition is not None and not isinstance(definition, Definition):
                msg = "'definition' must be a Definition, not {}"
                raise TypeError(msg.format(type(definition).__name__))
        self._data().definition = definition

    @property
    def id(self):
        return self._data().id

    @id.setter
    def id(self, value):
        raise RuntimeError("cannot set `id` of entities directly")

    @property
    def name(self) -> Optional[str]:
        return self._data().name

    @name.setter
    def name(self, value: Optional[str]):
        if __debug__:
            if value is not None and not isinstance(value, str):
                msg = "'name' must be str or None, not {}"
                raise TypeError(msg.format(type(value).__name__))
        self._data().name = value

    @property
    def namespace(self) -> Optional[str]:
        return self._data().namespace

    @namespace.setter
    def namespace(self, ns: Optional[str]):
        if __debug__:
            if ns is not None and not isinstance(ns, str):
                msg = "'namespace' must be str or None, not {}"
                raise TypeError(msg.format(type(ns).__name__))
        self._data().namespace = ns

    @property
    def obsolete(self) -> bool:
        return self._data().obsolete

    @obsolete.setter
    def obsolete(self, value: bool):
        if __debug__:
            if not isinstance(value, bool):
                msg = "'obsolete' must be bool, not {}"
                raise TypeError(msg.format(type(value).__name__))
        self._data().obsolete = value

    @property
    def subsets(self) -> FrozenSet[str]:
        return frozenset(self._data().subsets)

    @subsets.setter
    def subsets(self, subsets: FrozenSet[str]):
        if __debug__:
            msg = "'subsets' must be a set of str, not {}"
            if not isinstance(subsets, (set, frozenset)):
                raise TypeError(msg.format(type(subsets).__name__))
            for x in (x for x in subsets if not isinstance(x, str)):
                raise TypeError(msg.format(type(x).__name__))
        for subset in subsets:
            subsetdefs = self._ontology().metadata.subsetdefs
            if not any(subset == subsetdef.id for subsetdef in subsetdefs):
                raise ValueError(f"undeclared subset: {subset!r}")
        self._data().subsets = set(subsets)

    @property
    def synonyms(self) -> FrozenSet[Synonym]:
        ontology, termdata = self._ontology(), self._data()
        return frozenset(Synonym(ontology, s) for s in termdata.synonyms)

    @synonyms.setter
    def synonyms(self, synonyms: FrozenSet[Synonym]):
        if __debug__:
            msg = "'synonyms' must be a set of Synonym, not {}"
            if not isinstance(synonyms, (set, frozenset)):
                raise TypeError(msg.format(type(synonyms).__name__))
            for x in (x for x in synonyms if not isinstance(x, Synonym)):
                raise TypeError(msg.format(type(x).__name__))
        self._data().synonyms = set(synonyms)

    @property
    def xrefs(self) -> FrozenSet[Xref]:
        return frozenset(self._data().xrefs)

    @xrefs.setter
    def xrefs(self, xrefs: FrozenSet[Xref]):
        if __debug__:
            msg = "'xrefs' must be a set of Xref, not {}"
            if not isinstance(xrefs, (set, frozenset)):
                raise TypeError(msg.format(type(xrefs).__name__))
            for x in (x for x in synonyms if not isinstance(x, Xref)):
                raise TypeError(msg.format(type(x).__name__))
        self._data().xrefs = set(xrefs)