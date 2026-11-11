
SELLER_DATA = {
    "seller_name": "Demo Seller",
    "last_month": {
        "sales": 200000,
        "orders": 400,
        "cancellation_rate": 8,
        "average_selling_price": 500,
        "out_of_stock_products": 5
    },
    "this_month": {
        "sales": 135000,
        "orders": 270,
        "cancellation_rate": 14,
        "average_selling_price": 500,
        "out_of_stock_products": 18
    }
}


def percentage_change(previous, current):
    if previous == 0:
        return None

    return round(
        ((current - previous) / previous) * 100, 2
    )


def analyze_seller_performance():
    previous = SELLER_DATA["last_month"]
    current = SELLER_DATA["this_month"]

    analysis = {
        "sales": {
            "previous": previous["sales"],
            "current": current["sales"],
            "change_percent": percentage_change(
                previous["sales"], current["sales"]
            )
        },
        "orders": {
            "previous": previous["orders"],
            "current": current["orders"],
            "change_percent": percentage_change(
                previous["orders"], current["orders"]
            )
        },
        "cancellation_rate": {
            "previous": previous["cancellation_rate"],
            "current": current["cancellation_rate"],
            "change_percentage_points": round(
                current["cancellation_rate"]
                - previous["cancellation_rate"], 2
            )
        },
        "average_selling_price": {
            "previous": previous["average_selling_price"],
            "current": current["average_selling_price"],
            "change_percent": percentage_change(
                previous["average_selling_price"],
                current["average_selling_price"]
            )
        },
        "out_of_stock_products": {
            "previous": previous["out_of_stock_products"],
            "current": current["out_of_stock_products"],
            "change_percent": percentage_change(
                previous["out_of_stock_products"],
                current["out_of_stock_products"]
            )
        }
    }

    return analysis


if __name__ == "__main__":
    import json

    result = analyze_seller_performance()
    print(json.dumps(result, indent=4))
