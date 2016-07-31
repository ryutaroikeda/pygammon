from typing import List, Tuple, Optional, Callable, Union, IO, Any

#hack We inherit List to tell mypy that ndarray is indexable.
class ndarray(List):
	...

def zeros(size: int, dtype: Optional[Any]) -> ndarray: ...
