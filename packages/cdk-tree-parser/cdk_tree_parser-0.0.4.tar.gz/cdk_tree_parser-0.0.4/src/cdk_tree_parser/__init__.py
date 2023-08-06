'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class ConstructTreeParser(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-utilities.ConstructTreeParser",
):
    def __init__(self, node: aws_cdk.core.App) -> None:
        '''
        :param node: -
        '''
        jsii.create(ConstructTreeParser, self, [node])

    @jsii.member(jsii_name="generateParseTree")
    def generate_parse_tree(self) -> "ParseTree":
        return typing.cast("ParseTree", jsii.invoke(self, "generateParseTree", []))

    @jsii.member(jsii_name="generateTreeStructure")
    def generate_tree_structure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "generateTreeStructure", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rootNode")
    def root_node(self) -> aws_cdk.core.App:
        return typing.cast(aws_cdk.core.App, jsii.get(self, "rootNode"))


@jsii.interface(jsii_type="cdk-utilities.IVisitor")
class IVisitor(typing_extensions.Protocol):
    @jsii.member(jsii_name="postVisit")
    def post_visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        ...

    @jsii.member(jsii_name="preVisit")
    def pre_visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        ...

    @jsii.member(jsii_name="visit")
    def visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        ...


class _IVisitorProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-utilities.IVisitor"

    @jsii.member(jsii_name="postVisit")
    def post_visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "postVisit", [node]))

    @jsii.member(jsii_name="preVisit")
    def pre_visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "preVisit", [node]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVisitor).__jsii_proxy_class__ = lambda : _IVisitorProxy


@jsii.data_type(
    jsii_type="cdk-utilities.KvMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class KvMap:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KvMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Node(metaclass=jsii.JSIIMeta, jsii_type="cdk-utilities.Node"):
    def __init__(
        self,
        node: aws_cdk.core.ConstructNode,
        parent: typing.Optional["Node"] = None,
        children: typing.Optional[typing.Sequence["Node"]] = None,
    ) -> None:
        '''
        :param node: -
        :param parent: -
        :param children: -
        '''
        jsii.create(Node, self, [node, parent, children])

    @jsii.member(jsii_name="accept")
    def accept(self, visitor: IVisitor) -> None:
        '''
        :param visitor: -
        '''
        return typing.cast(None, jsii.invoke(self, "accept", [visitor]))

    @jsii.member(jsii_name="addChild")
    def add_child(self, node: "Node") -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "addChild", [node]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodePath")
    def node_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodePath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="originalNode")
    def original_node(self) -> aws_cdk.core.ConstructNode:
        return typing.cast(aws_cdk.core.ConstructNode, jsii.get(self, "originalNode"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="childrenNodes")
    def children_nodes(self) -> typing.List["Node"]:
        return typing.cast(typing.List["Node"], jsii.get(self, "childrenNodes"))

    @children_nodes.setter
    def children_nodes(self, value: typing.List["Node"]) -> None:
        jsii.set(self, "childrenNodes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parentNode")
    def parent_node(self) -> "Node":
        return typing.cast("Node", jsii.get(self, "parentNode"))

    @parent_node.setter
    def parent_node(self, value: "Node") -> None:
        jsii.set(self, "parentNode", value)


class ParseTree(metaclass=jsii.JSIIMeta, jsii_type="cdk-utilities.ParseTree"):
    def __init__(self, app: aws_cdk.core.App) -> None:
        '''
        :param app: -
        '''
        jsii.create(ParseTree, self, [app])

    @jsii.member(jsii_name="createTree")
    def create_tree(
        self,
        construct_node: aws_cdk.core.ConstructNode,
        parent: typing.Optional[Node] = None,
    ) -> None:
        '''Create The Tree.

        :param construct_node: -
        :param parent: -
        '''
        return typing.cast(None, jsii.invoke(self, "createTree", [construct_node, parent]))

    @jsii.member(jsii_name="findPaths")
    def find_paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "findPaths", []))

    @jsii.member(jsii_name="genTreeStructure")
    def gen_tree_structure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "genTreeStructure", []))


@jsii.implements(IVisitor)
class PrintTreeStructureVisitor(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-utilities.PrintTreeStructureVisitor",
):
    def __init__(self) -> None:
        jsii.create(PrintTreeStructureVisitor, self, [])

    @jsii.member(jsii_name="makeIndent")
    def make_indent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "makeIndent", []))

    @jsii.member(jsii_name="postVisit")
    def post_visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "postVisit", [node]))

    @jsii.member(jsii_name="preVisit")
    def pre_visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "preVisit", [node]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="indent")
    def indent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indent"))

    @indent.setter
    def indent(self, value: builtins.str) -> None:
        jsii.set(self, "indent", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="indentLevel")
    def indent_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "indentLevel"))

    @indent_level.setter
    def indent_level(self, value: jsii.Number) -> None:
        jsii.set(self, "indentLevel", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="knownChildrenSeen")
    def known_children_seen(self) -> KvMap:
        return typing.cast(KvMap, jsii.get(self, "knownChildrenSeen"))

    @known_children_seen.setter
    def known_children_seen(self, value: KvMap) -> None:
        jsii.set(self, "knownChildrenSeen", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lastIndentLevel")
    def last_indent_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastIndentLevel"))

    @last_indent_level.setter
    def last_indent_level(self, value: jsii.Number) -> None:
        jsii.set(self, "lastIndentLevel", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="output")
    def output(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "output"))

    @output.setter
    def output(self, value: builtins.str) -> None:
        jsii.set(self, "output", value)


@jsii.implements(IVisitor)
class PrintVisitor(metaclass=jsii.JSIIMeta, jsii_type="cdk-utilities.PrintVisitor"):
    def __init__(self) -> None:
        jsii.create(PrintVisitor, self, [])

    @jsii.member(jsii_name="postVisit")
    def post_visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "postVisit", [node]))

    @jsii.member(jsii_name="preVisit")
    def pre_visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "preVisit", [node]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: Node) -> None:
        '''
        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="paths")
    def paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "paths"))


__all__ = [
    "ConstructTreeParser",
    "IVisitor",
    "KvMap",
    "Node",
    "ParseTree",
    "PrintTreeStructureVisitor",
    "PrintVisitor",
]

publication.publish()
