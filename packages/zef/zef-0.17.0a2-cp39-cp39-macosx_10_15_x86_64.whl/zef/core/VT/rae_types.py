# Copyright 2022 Synchronous Technologies Pte Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import make_VT, insert_VT, ValueType, SetOf, BlobPtr
from .value_type import is_empty_, is_type_name_
from .helpers import remove_names, absorbed, type_name, names_of
from .. import internals

# These pop up a lot as special cases
AET_QFloat = make_VT('AET_QFloat', pytype=internals.AttributeEntityTypeStruct_QuantityFloat)
AET_QInt = make_VT('AET_QInt', pytype=internals.AttributeEntityTypeStruct_QuantityInt)
AET_Enum = make_VT('AET_Enum', pytype=internals.AttributeEntityTypeStruct_Enum)

VRT_QFloat = make_VT('VRT_QFloat', pytype=internals.ValueRepTypeStruct_QuantityFloat)
VRT_QInt = make_VT('VRT_QInt', pytype=internals.ValueRepTypeStruct_QuantityInt)
VRT_Enum = make_VT('VRT_Enum', pytype=internals.ValueRepTypeStruct_Enum)

# Helpers

def get_token(typ):
    abs = remove_names(absorbed(typ))
    if len(abs) >= 2:
        raise Exception(f"Token type has more than one absorbed token: {abs}")
    if len(abs) == 0:
        return None
    return abs[0]
def has_token(typ):
    return get_token(typ) is not None

def wrap_attr_readonly_token(orig):
    def this_get_attr(self, name):
        token = get_token(self)
        if token is None:
            out = getattr(orig, name)
        else:
            # This is just for AETs
            if isinstance(token, AET_QFloat):
                out = getattr(orig.QuantityFloat, name)
            elif isinstance(token, AET_QInt):
                out = getattr(orig.QuantityInt, name)
            elif isinstance(token, AET_Enum):
                out = getattr(orig.Enum, name)
            else:
                raise AttributeError(name)
        assert len(names_of(self)) == 0, "Going to lose names"
        base_token_type = self._replace(absorbed=())
        return base_token_type[out]
    def this_dir(self):
        token = get_token(self)
        if token is not None:
            # This is just for AETs
            if isinstance(token, AET_QFloat):
                return dir(orig.QuantityFloat)
            elif isinstance(token, AET_QInt):
                return dir(orig.QuantityInt)
            elif isinstance(token, AET_Enum):
                return dir(orig.Enum)
            else:
                return []
        return dir(orig)
    return (this_get_attr, None, this_dir)

def token_subtype(other, this):
    if type_name(other) != type_name(this):
        return False
    other_token = get_token(other)
    this_token = get_token(this)
    if other_token is None:
        return this_token is None
    if this_token is None:
        return True
    if isinstance(this_token, ValueType):
        if isinstance(other_token, ValueType):
            return issubclass(other_token, this_token)
        return isinstance(other_token, this_token)
    return other_token == this_token

def token_validation(self, token_type):
    my_name = type_name(self)

    abs = remove_names(absorbed(self))
    if len(abs) == 0:
        return True
    if len(abs) >= 2:
        raise Exception(f"Should only have one token absorbed into a {my_name}")
    thing = abs[0]

    if not isinstance(thing, token_type):
        raise Exception(f"A {my_name} doesn't contain a {token_type} but has a {thing} instead")

def token_str(self):
    my_name = self._d["type_name"]
    s = my_name
    token = get_token(self)
    if token is not None:
        if isinstance(token, (EntityTypeToken, RelationTypeToken, AttributeEntityTypeToken)):
            s += "." + token.name
        elif isinstance(token, BlobTypeToken):
            s += "." + str(token)
        else:
            s += "[" + str(token) + "]"

    names = names_of(self)
    for name in names:
        s += f"['{self._d['absorbed'][0]}']"
    return s

def ET_is_a(x, typ):
    from . import DelegateRef
    token = get_token(typ)
    if token is None:
        if isinstance(x, DelegateRef):
            return isinstance(x.item, EntityTypeToken)
        elif isinstance(x, BlobPtr):
            return internals.BT(x) == internals.BT.ENTITY_NODE
        return isinstance(x, ValueType) and type_name(x) == "ET"
    else:
        if isinstance(x, DelegateRef):
            return x.item == token
        elif isinstance(x, BlobPtr):
            if internals.BT(x) != internals.BT.ENTITY_NODE:
                return False
            if isinstance(token, ValueType):
                return isinstance(internals.ET(x), token)
            return internals.ET(x) == token
        else:
            return False
def AET_is_a(x, typ):
    from . import DelegateRef
    token = get_token(typ)
    if token is None:
        if isinstance(x, DelegateRef):
            return isinstance(x.item, AttributeEntityTypeToken)
        elif isinstance(x, BlobPtr):
            return internals.BT(x) == internals.BT.ATTRIBUTE_ENTITY_NODE
        return is_type_name_(x, "AET")
    else:
        if isinstance(x, DelegateRef):
            x_aet = x.item
        elif isinstance(x, BlobPtr):
            if internals.BT(x) != internals.BT.ATTRIBUTE_ENTITY_NODE:
                return False
            x_aet = internals.AET(x)
        elif isinstance(x, ValueType) and type_name(x) == "AET":
            x_aet = get_token(x)
            if x_aet is None:
                return False
        elif isinstance(x, (AttributeEntityTypeToken, AET_QFloat, AET_QInt, AET_Enum)):
            x_aet = x
        else:
            return False

        if isinstance(token, ValueType):
            return isinstance(x_aet, token)

        if token == x_aet:
            return True

        if isinstance(token, AttributeEntityTypeToken) and token.complex_value is not None:
            raise Exception(f"Checking isinstance on complex AETs (got {typ}) is not yet implemented. Coming soon!")
        if isinstance(x_aet, AttributeEntityTypeToken) and x_aet.complex_value is not None:
            raise Exception(f"Checking isinstance on complex AETs (got {x_aet}) is not yet implemented. Coming soon!")

        if isinstance(token, (AET_QFloat, AET_QInt, AET_Enum)):
            if isinstance(x_aet, AttributeEntityTypeToken):
                if isinstance(token, AET_QFloat):
                    return internals.is_vrt_a_quantity_float(x_aet.rep_type)
                if isinstance(token, AET_QInt):
                    return internals.is_vrt_a_quantity_int(x_aet.rep_type)
                if isinstance(token, AET_QEnum):
                    return internals.is_vrt_a_enum(x_aet.rep_type)
        return False
def RT_is_a(x, typ):
    from . import DelegateRef
    token = get_token(typ)
    if token is None:
        if isinstance(x, DelegateRef):
            if type(x.item) == internals.DelegateRelationTriple:
                return isinstance(x.item.rt, RelationTypeToken)
            return isinstance(x.item, RelationTypeToken)
        elif isinstance(x, BlobPtr):
            # TODO: not was removed from the second part of this condition. In case something breaks check here!
            return internals.BT(x) == internals.BT.RELATION_EDGE
        return isinstance(x, ValueType) and type_name(x) == "RT"
    else:
        if isinstance(x, DelegateRef):
            if type(x.item) == internals.DelegateRelationTriple:
                return x.item.rt == token
            else:
                return x.item == token
        elif isinstance(x, BlobPtr):
            if internals.BT(x) != internals.BT.RELATION_EDGE:
                return False
            # TODO: EntityTypeToken
            if isinstance(token, ValueType):
                return isinstance(internals.RT(x), token)
            return internals.RT(x) == token
        else:
            return False
def BT_is_a(x, typ):
    token = get_token(typ)
    if token is None:
        if isinstance(x, BlobPtr):
            return True
        return isinstance(x, ValueType) and type_name(x) == "BT"
    else:
        c_bt = token
        if not isinstance(c_bt, BlobTypeToken):
            raise Exception("TODO")
        if isinstance(x, BlobPtr):
            return c_bt == internals.BT(x)
        if c_bt == internals.BT.RELATION_EDGE:
            if isinstance(x, RT):
                return True
        if c_bt == internals.BT.ENTITY_NODE:
            if isinstance(x, ET):
                return True
        if c_bt == internals.BT.ATTRIBUTE_ENTITY_NODE:
            if isinstance(x, AET):
                return True
        return False
def VRT_is_a(x, typ):
    from . import DelegateRef
    token = get_token(typ)
    if token is None:
        if isinstance(x, DelegateRef):
            return isinstance(x.item, ValueRepTypeToken)
        elif isinstance(x, BlobPtr):
            return internals.BT(x) in [internals.BT.ATTRIBUTE_ENTITY_NODE,
                                       internals.BT.VALUE_NODE]
        return is_type_name_(x, "VRT")
    else:
        if isinstance(x, DelegateRef):
            x_vrt = x.item
        elif isinstance(x, BlobPtr):
            if internals.BT(x) not in [internals.BT.ATTRIBUTE_ENTITY_NODE,
                                       internals.BT.VALUE_NODE]:
                return False
            x_vrt = internals.VRT(x)
        elif isinstance(x, ValueType) and type_name(x) == "VRT":
            x_vrt = get_token(x)
            if x_vrt is None:
                return False
        elif isinstance(x, (ValueRepTypeToken, VRT_QFloat, VRT_QInt, VRT_Enum)):
            x_vrt = x
        else:
            return False

        if isinstance(token, ValueType):
            return isinstance(x_vrt, token)

        if token == x_vrt:
            return True

        if isinstance(token, (VRT_QFloat, VRT_QInt, VRT_Enum)):
            if isinstance(x_aet, AttributeEntityTypeToken):
                if isinstance(token, VRT_QFloat):
                    return internals.is_vrt_a_quantity_float(x_vrt)
                if isinstance(token, VRT_QInt):
                    return internals.is_vrt_a_quantity_int(x_vrt)
                if isinstance(token, VRT_QEnum):
                    return internals.is_vrt_a_enum(x_vrt)
        return False


def ET_ctor(self, *args, **kwargs):
    if get_token(self) is None:
        return ET[internals.ET(*args, **kwargs)]
    else:
        return EntityValueInstance(self, *args, **kwargs)
    
# TODO: Move this somewhere
from ..patching import EntityValueInstance_
EntityValueInstance = make_VT('EntityValueInstance', pytype=EntityValueInstance_)
EntityTypeToken = make_VT('EntityTypeToken', pytype=internals.EntityType)

ET = make_VT('ET',
             constructor_func=ET_ctor,
             pass_self=True,
             attr_funcs=wrap_attr_readonly_token(internals.ET),
             is_a_func=ET_is_a,
             is_subtype_func=token_subtype,
             str_func=token_str)

AttributeEntityTypeToken = make_VT('AttributeEntityTypeToken', pytype=internals.AttributeEntityType)
def AET_ctor(self, x):
    if type(x) == str:
        return getattr(self, x)
    token = get_token(self)
    if token is not None:
        return NotImplemented
    return AET[internals.AET(x)]

AET = make_VT('AET',
              constructor_func=AET_ctor,
              pass_self=True,
              attr_funcs=wrap_attr_readonly_token(internals.AET),
              is_a_func=AET_is_a,
              is_subtype_func=token_subtype,
              str_func=token_str)

RelationTypeToken = make_VT('RelationTypeToken', pytype=internals.RelationType)
RT = make_VT('RT',
             constructor_func=lambda x: RT[internals.RT(x)],
             attr_funcs=wrap_attr_readonly_token(internals.RT),
             is_a_func=RT_is_a,
             is_subtype_func=token_subtype,
             str_func=token_str)


BlobTypeToken = make_VT('BlobTypeToken', pytype=internals.BlobType)
BT = make_VT('BT',
             constructor_func=lambda x: BT[internals.BT(x)],
             attr_funcs=wrap_attr_readonly_token(internals.BT),
             is_a_func=BT_is_a,
             is_subtype_func=token_subtype,
             str_func=token_str)

# BT         = ValueType_(type_name='BT',   constructor_func=pyzef.internals.BT, attr_funcs=wrap_attr_readonly(internals.BT, None), pytype=internals.BlobType)

ValueRepTypeToken = make_VT('ValueRepTypeToken', pytype=internals.ValueRepType)
def VRT_ctor(self, x):
    if type(x) == str:
        return getattr(self, x)
    token = get_token(self)
    if token is not None:
        return NotImplemented
    return VRT[internals.VRT(x)]
VRT = make_VT('VRT',
              constructor_func=VRT_ctor,
              pass_self=True,
              attr_funcs=wrap_attr_readonly_token(internals.VRT),
              is_a_func=VRT_is_a,
              is_subtype_func=token_subtype,
              str_func=token_str)


def tx_is_a(x, typ):
    return isinstance(x, BT.TX_EVENT_NODE)

TX = make_VT("TX", is_a_func=tx_is_a)

RAET = insert_VT("RAET", ET | RT | AET)