# SQLAlchemy Ltree Model Mixins

## Synopsis

```python
import ltree
from sqlalchemy import (
  Column,
  Integer,
  Text,
)
from sqlalchemy.orm import (
    Session,
)

class UnorderedNode(Base, ltree.LtreeMixin):
    __tablename__ = 'ltree_nodes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

class OrderedNode(Base, ltree.OLtreeMixin):
    __tablename__ = 'oltree_nodes'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
```
