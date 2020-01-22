import csv
from datetime import date

from pxi.report import ReportWriter


def export_pricelist(filepath, price_region_items):
    """Export pricelist to file."""
    effective_date = date.today().strftime("%d-%b-%Y")
    def price_region_item_to_row(price_region_item):
        inventory_item = price_region_item.inventory_item
        return [
            inventory_item.code,
            price_region_item.code,
            str(price_region_item.price_0),
            str(price_region_item.quantity_1),
            str(price_region_item.quantity_2),
            str(price_region_item.quantity_3),
            str(price_region_item.quantity_4),
            str(price_region_item.price_1),
            str(price_region_item.price_2),
            str(price_region_item.price_3),
            str(price_region_item.price_4),
            str(price_region_item.rrp_excl_tax),
            str(price_region_item.rrp_incl_tax),
            "",
            effective_date,
            "",
        ]
    rows = [price_region_item_to_row(item) for item in price_region_items]
    with open(filepath, "w") as file:
        csv.writer(file).writerows(rows)


def export_price_changes_report(filepath, price_changes):
    """Export report to file."""
    report_writer = ReportWriter(filepath)

    def string_field(name, title, width):
        return {
            "name": name,
            "title": title, 
            "width": width,
            "align": "left",
        }

    def number_field(name, title, number_format="0.0000"):
        return {
            "name": name,
            "title": title,
            "width": 16,
            "align": "right",
            "number_format": number_format,
        }

    fields = [
        string_field("item_code", "Item Code", 20),
        string_field("brand", "Brand", 7),
        string_field("apn", "APN", 20),
        string_field("description", "Description", 20),
        string_field("price_rule", "Price Rule", 7),
    ]
    for i in range(5):
        if i > 0:
            fields.append(number_field(
                "quantity_{}".format(i),
                "Quantity {}".format(i),
                number_format="0"
            ))
        fields.append(number_field(
            "price_{}_was".format(i),
            "Price {} Was".format(i)
        ))
        fields.append(number_field(
            "price_{}_now".format(i),
            "Price {} Now".format(i)
        ))
        fields.append(number_field(
            "price_{}_diff".format(i),
            "Price {} Diff".format(i)
        ))

    def item_to_row(price_change):
        price_region_item = price_change.item_now
        price_region_item_was = price_change.item_was
        price_diffs = price_change.price_diffs()
        inventory_item = price_region_item.inventory_item
        price_rule = price_region_item.price_rule
        row = {
            "item_code": inventory_item.code,
            "brand": inventory_item.brand,
            "apn": inventory_item.apn,
            "description": " ".join([
                inventory_item.description_line_1,
                inventory_item.description_line_2,
                inventory_item.description_line_3
            ]).strip(),
            "price_rule": price_rule.code
        }
        for i in range(5):
            if i > 0:
                row["quantity_{}".format(i)] = getattr(price_region_item, "quantity_{}".format(i))
            row["price_{}_was".format(i)] = getattr(price_region_item_was, "price_{}".format(i))
            row["price_{}_now".format(i)] = getattr(price_region_item, "price_{}".format(i))
            row["price_{}_diff".format(i)] = price_diffs[i]
        return row

    rows = [item_to_row(price_change) for price_change in price_changes]

    report_writer.write_sheet("Price Changes", fields, rows)
    report_writer.save()


def export_product_price_task(filepath, price_region_items):
    """Export product price update task to file."""
    def price_region_item_to_row(price_region_item):
        inventory_item = price_region_item.inventory_item
        row = {
            "item_code": inventory_item.code,
            "region": price_region_item.code,
        }
        for i in range(5):
            fieldname = "price_{}".format(i)
            row[fieldname] = getattr(price_region_item, fieldname)
        return row
    rows = [price_region_item_to_row(item) for item in price_region_items]

    with open(filepath, "w") as file:
        fieldnames = ["item_code", "region"] + [
            "price_{}".format(i) for i in range(5)]
        writer = csv.DictWriter(file, fieldnames, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(rows)


def export_contract_item_task(filepath, contract_items):
    """Export product price update task to file."""
    def contract_item_to_row(contract_item):
        inventory_item = contract_item.inventory_item
        row = {
            "contract": contract_item.code,
            "item_code": inventory_item.code,
        }
        for i in range(1, 7):
            fieldname = "price_{}".format(i)
            row[fieldname] = getattr(contract_item, fieldname)
        return row
    rows = [contract_item_to_row(item) for item in contract_items]

    with open(filepath, "w") as file:
        fieldnames = ["contract", "item_code"]
        for i in range(1, 7):
            fieldnames.append("price_{}".format(i))
            fieldnames.append("quantity_{}".format(i))
        writer = csv.DictWriter(file, fieldnames, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(rows)


def export_tickets_list(filepath, warehouse_stock_items):
    """Export tickets list to file."""
    def stocked_item_codes(warehouse_stock_items):
        for item in warehouse_stock_items:
            item_code = item.inventory_item.code
            if item.bin_location:
                yield item_code
            elif item.on_hand:
                yield item_code
            elif item.minimum:
                yield item_code

    item_codes = stocked_item_codes(warehouse_stock_items)
    lines = ["{}\n".format(item_code) for item_code in item_codes]
    with open(filepath, "w") as file:
        file.writelines(lines)


def sell_price_change(product):
    """Calculates ratio between old and new level 0 sell prices."""
    was_sell_price = product.was_sell_prices[0]
    now_sell_price = product.sell_prices[0]
    diff = now_sell_price - was_sell_price
    return diff / was_sell_price