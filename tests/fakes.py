
from datetime import datetime
from decimal import Decimal
from random import randint, choice as random_choice
import string
import time
from pxi.enum import ItemCondition, ItemType

from pxi.models import ContractItem, InventoryItem, WarehouseStockItem


def random_description(length=30):
    """
    Generates a random description.
    """
    return random_string(30)


def random_datetime(start=None, end=None):
    """
    Generates a random datetime between two given datetimes.
    """
    if start is None:
        start = datetime.fromtimestamp(0)
    if end is None:
        end = datetime.now()
    return datetime.fromtimestamp(randint(
        int(time.mktime(start.timetuple())),
        int(time.mktime(end.timetuple()))))


def random_item_code():
    """
    Generates a random item code.
    """
    return random_string(16)


def random_price():
    """
    Generates a random price.
    """
    return Decimal(random_price_string())


def random_price_factor():
    """
    Generates a random price multiplication factor with format '0.00'.
    """
    return f"{randint(1, 5)}.{(randint(0, 19) * 5):02d}"


def random_price_string():
    """
    Generates a random price string with format '0.00'.
    """
    return f"{randint(1, 100)}.{randint(0, 99):02d}"


def random_quantity():
    """
    Generates a random quantity between 0 and 999999, inclusive.
    """
    return str(randint(0, 999999))


def random_string(length):
    """
    Generates a random string of uppercase ASCII letters.
    """
    return "".join([
        random_choice(string.ascii_uppercase) for x in range(length)])


def random_uom(length=4):
    """
    Generates a random unit of measure.
    """
    return random_string(length)


def fake_inventory_item(values={}):
    """
    Generates a fake InventoryItem.
    """
    return InventoryItem(
        code=values.get("code", random_item_code()),
        description_line_1=values.get(
            "description_line_1", random_description()),
        description_line_2=values.get(
            "description_line_2", random_description()),
        description_line_3=values.get(
            "description_line_3", random_description()),
        uom=values.get("uom", random_uom()),
        brand=values.get("brand", random_string(3)),
        apn=values.get("apn", random_string(20)),
        group=values.get("group", random_string(2)),
        item_type=values.get("item_type", ItemType.STOCKED_ITEM),
        condition=values.get("condition", ItemCondition.NONE),
        created=values.get("created", random_datetime()),
        replacement_cost=values.get("replacement_cost", random_price()))


def fake_contract_item(inventory_item, values={}):
    """
    Generates a fake ContractItem.
    """
    return ContractItem(
        inventory_item=inventory_item,
        code=values.get("code", random_string(6)),
        price_1=values.get("price_1", random_price()),
        price_2=values.get("price_2", random_price()),
        price_3=values.get("price_3", random_price()),
        price_4=values.get("price_4", random_price()),
        price_5=values.get("price_5", random_price()),
        price_6=values.get("price_6", random_price()))


def fake_warehouse_stock_item(inventory_item, values={}):
    """
    Generates a fake WarehouseStockItem.
    """
    return WarehouseStockItem(
        inventory_item=inventory_item,
        code=values.get("code", random_string(4)),
        on_hand=values.get("on_hand", random_quantity()),
        minimum=values.get("minimum", random_quantity()),
        maximum=values.get("maximum", random_quantity()),
        bin_location=values.get("bin_location", random_string(8)),
        bulk_location=values.get("bulk_location", random_string(8)))
