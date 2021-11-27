from typing import Any, Dict, Iterable, List


def items_without_meta(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """`
    Returns all items contained in a response, excluding all metadata fields.
    """

    def item_without_meta(item_with_meta: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: value
            for key, value in item_with_meta.items()
            if not key.startswith("_")
        }

    return [item_without_meta(i) for i in items]
