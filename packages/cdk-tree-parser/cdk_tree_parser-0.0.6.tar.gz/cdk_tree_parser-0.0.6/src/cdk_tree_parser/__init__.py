'''
# CDK Utilities

## **Please Advise**

This project is currently in development... all releases pre 0.1.0 are to be considered experimental

### Purpose

Creating some interesting CDK Utility classes to provide deeper insights into deployable resources and construct trees

# API Reference <a name="API Reference"></a>

## Structs <a name="Structs"></a>

### KvMap <a name="cdk-utilities.KvMap"></a>

#### Initializer <a name="[object Object].Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import KvMap

kv_map = {...}
```

## Classes <a name="Classes"></a>

### ConstructTreeParser <a name="cdk-utilities.ConstructTreeParser"></a>

#### Initializer <a name="cdk-utilities.ConstructTreeParser.Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import ConstructTreeParser

ConstructTreeParser(node, App)
```

##### `node`<sup>Required</sup> <a name="cdk-utilities.ConstructTreeParser.parameter.node"></a>

* *Type:* [`@aws-cdk/core.App`](#@aws-cdk/core.App)

---


#### Methods <a name="Methods"></a>

##### `generateParseTree` <a name="cdk-utilities.ConstructTreeParser.generateParseTree"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
generate_parse_tree()
```

##### `generateTreeStructure` <a name="cdk-utilities.ConstructTreeParser.generateTreeStructure"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
generate_tree_structure()
```

#### Properties <a name="Properties"></a>

##### `rootNode`<sup>Required</sup> <a name="cdk-utilities.ConstructTreeParser.property.rootNode"></a>

* *Type:* [`@aws-cdk/core.App`](#@aws-cdk/core.App)

---


### Node <a name="cdk-utilities.Node"></a>

#### Initializer <a name="cdk-utilities.Node.Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import Node

Node(node, ConstructNode, parent?: Node, children?: Node[])
```

##### `node`<sup>Required</sup> <a name="cdk-utilities.Node.parameter.node"></a>

* *Type:* [`@aws-cdk/core.ConstructNode`](#@aws-cdk/core.ConstructNode)

---


##### `parent`<sup>Optional</sup> <a name="cdk-utilities.Node.parameter.parent"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `children`<sup>Optional</sup> <a name="cdk-utilities.Node.parameter.children"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)[]

---


#### Methods <a name="Methods"></a>

##### `accept` <a name="cdk-utilities.Node.accept"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
accept(visitor, IVisitor)
```

###### `visitor`<sup>Required</sup> <a name="cdk-utilities.Node.parameter.visitor"></a>

* *Type:* [`cdk-utilities.IVisitor`](#cdk-utilities.IVisitor)

---


##### `addChild` <a name="cdk-utilities.Node.addChild"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
add_child(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.Node.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


#### Properties <a name="Properties"></a>

##### `nodeId`<sup>Required</sup> <a name="cdk-utilities.Node.property.nodeId"></a>

* *Type:* `string`

---


##### `nodePath`<sup>Required</sup> <a name="cdk-utilities.Node.property.nodePath"></a>

* *Type:* `string`

---


##### `originalNode`<sup>Required</sup> <a name="cdk-utilities.Node.property.originalNode"></a>

* *Type:* [`@aws-cdk/core.ConstructNode`](#@aws-cdk/core.ConstructNode)

---


##### `childrenNodes`<sup>Required</sup> <a name="cdk-utilities.Node.property.childrenNodes"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)[]

---


##### `parentNode`<sup>Required</sup> <a name="cdk-utilities.Node.property.parentNode"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


### ParseTree <a name="cdk-utilities.ParseTree"></a>

#### Initializer <a name="cdk-utilities.ParseTree.Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import ParseTree

ParseTree(app, App)
```

##### `app`<sup>Required</sup> <a name="cdk-utilities.ParseTree.parameter.app"></a>

* *Type:* [`@aws-cdk/core.App`](#@aws-cdk/core.App)

---


#### Methods <a name="Methods"></a>

##### `createTree` <a name="cdk-utilities.ParseTree.createTree"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
create_tree(construct_node, ConstructNode, parent?: Node)
```

###### `constructNode`<sup>Required</sup> <a name="cdk-utilities.ParseTree.parameter.constructNode"></a>

* *Type:* [`@aws-cdk/core.ConstructNode`](#@aws-cdk/core.ConstructNode)

---


###### `parent`<sup>Optional</sup> <a name="cdk-utilities.ParseTree.parameter.parent"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `findPaths` <a name="cdk-utilities.ParseTree.findPaths"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
find_paths()
```

##### `genTreeStructure` <a name="cdk-utilities.ParseTree.genTreeStructure"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
gen_tree_structure()
```

### PrintTreeStructureVisitor <a name="cdk-utilities.PrintTreeStructureVisitor"></a>

* *Implements:* [`cdk-utilities.IVisitor`](#cdk-utilities.IVisitor)

#### Initializer <a name="cdk-utilities.PrintTreeStructureVisitor.Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import PrintTreeStructureVisitor

PrintTreeStructureVisitor()
```

#### Methods <a name="Methods"></a>

##### `makeIndent` <a name="cdk-utilities.PrintTreeStructureVisitor.makeIndent"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
make_indent()
```

##### `postVisit` <a name="cdk-utilities.PrintTreeStructureVisitor.postVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
post_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `preVisit` <a name="cdk-utilities.PrintTreeStructureVisitor.preVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pre_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `visit` <a name="cdk-utilities.PrintTreeStructureVisitor.visit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


#### Properties <a name="Properties"></a>

##### `indent`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.property.indent"></a>

* *Type:* `string`

---


##### `indentLevel`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.property.indentLevel"></a>

* *Type:* `number`

---


##### `knownChildrenSeen`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.property.knownChildrenSeen"></a>

* *Type:* [`cdk-utilities.KvMap`](#cdk-utilities.KvMap)

---


##### `lastIndentLevel`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.property.lastIndentLevel"></a>

* *Type:* `number`

---


##### `output`<sup>Required</sup> <a name="cdk-utilities.PrintTreeStructureVisitor.property.output"></a>

* *Type:* `string`

---


### PrintVisitor <a name="cdk-utilities.PrintVisitor"></a>

* *Implements:* [`cdk-utilities.IVisitor`](#cdk-utilities.IVisitor)

#### Initializer <a name="cdk-utilities.PrintVisitor.Initializer"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_utilities import PrintVisitor

PrintVisitor()
```

#### Methods <a name="Methods"></a>

##### `postVisit` <a name="cdk-utilities.PrintVisitor.postVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
post_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `preVisit` <a name="cdk-utilities.PrintVisitor.preVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pre_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `visit` <a name="cdk-utilities.PrintVisitor.visit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.PrintVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


#### Properties <a name="Properties"></a>

##### `paths`<sup>Required</sup> <a name="cdk-utilities.PrintVisitor.property.paths"></a>

* *Type:* `string`

---


## Protocols <a name="Protocols"></a>

### IVisitor <a name="cdk-utilities.IVisitor"></a>

* *Implemented By:* [`cdk-utilities.PrintTreeStructureVisitor`](#cdk-utilities.PrintTreeStructureVisitor), [`cdk-utilities.PrintVisitor`](#cdk-utilities.PrintVisitor), [`cdk-utilities.IVisitor`](#cdk-utilities.IVisitor)

#### Methods <a name="Methods"></a>

##### `postVisit` <a name="cdk-utilities.IVisitor.postVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
post_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.IVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `preVisit` <a name="cdk-utilities.IVisitor.preVisit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
pre_visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.IVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---


##### `visit` <a name="cdk-utilities.IVisitor.visit"></a>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
visit(node, Node)
```

###### `node`<sup>Required</sup> <a name="cdk-utilities.IVisitor.parameter.node"></a>

* *Type:* [`cdk-utilities.Node`](#cdk-utilities.Node)

---
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
