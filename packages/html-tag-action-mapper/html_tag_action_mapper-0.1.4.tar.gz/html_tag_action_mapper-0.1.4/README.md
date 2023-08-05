# html tag action mapper
A small demo library for mapping html tags to their possible actions.

### Installation
```
pip install htm_tag_action_mapper
```

### Get started
How to get actions given a html tag:

```Python
from htm_tag_action_mapper import ActionMapper

# Instantiate a Multiplication object
actionmapper = ActionMapper()

# Call the multiply method
actions = actionmapper.getactions("input")
```