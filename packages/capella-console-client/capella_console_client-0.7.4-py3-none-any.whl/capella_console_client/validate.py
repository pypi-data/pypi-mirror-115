import uuid

from typing import no_type_check, Optional, List, Dict, Any

from capella_console_client.enumerations import ProductType


@no_type_check
def _validate_uuid(uuid_str: str) -> None:
    try:
        uuid.UUID(uuid_str)
    except ValueError as e:
        raise ValueError(f"{uuid_str} is not a valid uuid: {e}")


def _validate_stac_id_or_stac_items(
    stac_ids: Optional[List[str]] = None, items: Optional[List[Dict[str, Any]]] = None
) -> List[str]:
    if not stac_ids and not items:
        raise ValueError("Please provide stac_ids or items")

    if not stac_ids:
        stac_ids = [f["id"] for f in items]  # type: ignore

    return stac_ids


def _validate_and_filter_product_types(product_types: List[str]) -> List[str]:
    return [p.upper() for p in product_types if p.upper() in ProductType]
