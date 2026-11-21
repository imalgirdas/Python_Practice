"""Create the sample datasets used by the 150 Python practice problems.

Run once from the project folder:
    python 00_make_data.py
It writes seven CSV files to the data/ folder. A fixed random seed makes
the data identical on every run, so your results match the documented ones.
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)

# ---------------------------------------------------------------- customers
first = ["Rūta", "Tomas", "Ieva", "Mantas", "Greta", "Lukas", "Jonas", "Agnė",
         "Paulius", "Emilija", "Karolis", "Austėja", "Domas", "Gabija", "Matas",
         "Ugnė", "Andris", "Liene", "Mart", "Kadri", "Piotr", "Anna", "Marek",
         "Zofia", "Vytautas", "Eglė", "Darius", "Simona", "Jānis", "Laura",
         "Kristjan", "Maria", "Tadas", "Monika", "Edgars", "Ilze", "Rasmus",
         "Kasia", "Justas", "Neringa"]
last = ["Kazlauskas", "Petrauskas", "Jankauskaitė", "Stankevičius", "Vasiliauskaitė",
        "Žukauskas", "Butkus", "Paulauskaitė", "Urbonas", "Kavaliauskaitė",
        "Kairys", "Navickaitė", "Ramanauskas", "Sakalauskaitė", "Bernotas",
        "Mockutė", "Bērziņš", "Ozola", "Tamm", "Saar", "Nowak", "Kowalska",
        "Wiśniewski", "Wójcik", "Balčiūnas", "Grigaitė", "Lukoševičius", "Žilinskaitė",
        "Kalniņš", "Liepa", "Kask", "Mägi", "Valaitis", "Rimkutė", "Krūmiņš",
        "Siliņa", "Sepp", "Lewandowska", "Adomaitis", "Jurgaitė"]
city_country = {"Vilnius": "Lithuania", "Kaunas": "Lithuania", "Klaipėda": "Lithuania",
                "Riga": "Latvia", "Tallinn": "Estonia", "Warsaw": "Poland"}
n_cust = 40
cities = rng.choice(list(city_country), n_cust, p=[.26, .2, .12, .16, .13, .13])
signup = pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 912, n_cust), "D")
ascii_map = str.maketrans("ąčęėįšųūžĄČĘĖĮŠŲŪŽāēīņļģķōšūĀĒĪŅŪłśćńźżóŁŚĆŃŹŻÓäöõüÄÖÕÜ",
                          "aceeisuuzACEEISUUZaeinlgkosuAEINUlscnzzoLSCNZZOaoouAOOU")
emails = [f"{f}.{l}@mail.com".lower().translate(ascii_map) for f, l in zip(first, last)]
customers = pd.DataFrame({
    "customer_id": range(1, n_cust + 1),
    "first_name": first,
    "last_name": last,
    "city": cities,
    "country": [city_country[c] for c in cities],
    "age": rng.integers(19, 69, n_cust).astype(float),
    "segment": rng.choice(["Consumer", "Corporate", "Small Business"], n_cust, p=[.55, .25, .20]),
    "signup_date": signup.strftime("%Y-%m-%d"),
    "email": emails,
})
customers.loc[[4, 17, 31], "email"] = np.nan
customers.loc[[9, 26], "age"] = np.nan
customers.to_csv(DATA / "customers.csv", index=False)

# ---------------------------------------------------------------- products
products = pd.DataFrame([
    (101, "Laptop Pro 14", "Electronics", 1299.00, 910.00, 25),
    (102, "Wireless Mouse", "Electronics", 24.90, 9.50, 340),
    (103, "4K Monitor 27", "Electronics", 389.00, 255.00, 60),
    (104, "USB-C Hub", "Electronics", 49.90, 21.00, 210),
    (105, "Noise-Cancel Headphones", "Electronics", 229.00, 132.00, 75),
    (106, "Office Chair", "Furniture", 279.00, 150.00, 40),
    (107, "Standing Desk", "Furniture", 549.00, 330.00, 18),
    (108, "Desk Lamp", "Furniture", 39.90, 15.00, 150),
    (109, "Bookshelf", "Furniture", 129.00, 70.00, 35),
    (110, "Notebook A5 (5-pack)", "Office Supplies", 12.50, 4.20, 600),
    (111, "Gel Pens (12-pack)", "Office Supplies", 9.90, 3.10, 800),
    (112, "Paper A4 (500 sheets)", "Office Supplies", 6.90, 3.60, 1200),
    (113, "Yoga Mat", "Sports", 34.90, 14.00, 120),
    (114, "Dumbbell Set 20kg", "Sports", 89.00, 48.00, 45),
    (115, "Fitness Tracker", "Sports", 119.00, 66.00, 0),
], columns=["product_id", "product_name", "category", "price", "cost", "stock"])
products.to_csv(DATA / "products.csv", index=False)

# ---------------------------------------------------------------- orders
n_ord = 240
days = pd.date_range("2023-01-01", "2024-12-31", freq="D")
month_w = np.array([0.8, 0.7, 0.85, 0.9, 0.95, 0.9, 0.85, 0.9, 1.0, 1.05, 1.4, 1.6])
year_w = np.where(days.year == 2024, 1.35, 1.0)
w = month_w[days.month - 1] * year_w
order_dates = np.sort(rng.choice(days, n_ord, p=w / w.sum()))
cust_w = rng.gamma(1.4, 1.0, 38)
orders = pd.DataFrame({
    "order_id": range(1001, 1001 + n_ord),
    "customer_id": rng.choice(np.arange(1, 39), n_ord, p=cust_w / cust_w.sum()),
    "order_date": pd.to_datetime(order_dates).strftime("%Y-%m-%d"),
    "channel": rng.choice(["Web", "App", "Store"], n_ord, p=[.5, .3, .2]),
    "status": rng.choice(["Completed", "Cancelled", "Returned"], n_ord, p=[.85, .10, .05]),
    "discount_pct": rng.choice([0, 0, 0, 5, 10, 15], n_ord),
    "shipping_days": rng.integers(1, 8, n_ord).astype(float),
})
orders.loc[(orders["channel"] == "Store") | (orders["status"] == "Cancelled"), "shipping_days"] = np.nan
orders.to_csv(DATA / "orders.csv", index=False)

# ---------------------------------------------------------------- order_items
pop = np.array([3, 14, 5, 9, 5, 3, 2, 8, 3, 12, 12, 13, 6, 3, 0], dtype=float)
rows, item_id = [], 1
for oid in orders["order_id"]:
    k = rng.choice([1, 2, 3, 4], p=[.4, .3, .2, .1])
    pids = rng.choice(products["product_id"], k, replace=False, p=pop / pop.sum())
    for pid in pids:
        price = products.loc[products["product_id"] == pid, "price"].item()
        qty = int(rng.choice([1, 1, 1, 2, 2, 3])) if price < 100 else 1
        rows.append((item_id, oid, int(pid), qty, price))
        item_id += 1
order_items = pd.DataFrame(rows, columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price"])
order_items.to_csv(DATA / "order_items.csv", index=False)

# ---------------------------------------------------------------- ab_test
n_ab = 2000
group = rng.choice(["A", "B"], n_ab)
device = rng.choice(["mobile", "desktop"], n_ab, p=[.6, .4])
p_conv = np.where(group == "B", 0.125, 0.095) * np.where(device == "desktop", 1.2, 0.87)
converted = (rng.random(n_ab) < p_conv).astype(int)
revenue = np.where(converted == 1, np.round(rng.gamma(2.2, 26, n_ab) * np.where(group == "B", 1.05, 1.0), 2), 0.0)
ab_test = pd.DataFrame({"user_id": range(1, n_ab + 1), "group": group, "device": device,
                        "converted": converted, "revenue": revenue})
ab_test.to_csv(DATA / "ab_test.csv", index=False)

# ---------------------------------------------------------------- churn
n_ch = 800
contract = rng.choice(["Monthly", "One year", "Two year"], n_ch, p=[.55, .27, .18])
tenure = np.clip(np.round(rng.exponential(22, n_ch)) + 1, 1, 72).astype(int)
charges = np.round(rng.uniform(19, 119, n_ch), 2)
tickets = rng.poisson(1.3, n_ch)
logins = np.clip(np.round(rng.normal(18, 8, n_ch)), 0, None).astype(int)
payment = rng.choice(["Card", "Bank transfer", "PayPal"], n_ch, p=[.5, .3, .2])
logit = (-1.0 + 1.3 * (contract == "Monthly") - 0.9 * (contract == "Two year")
         - 0.035 * tenure + 0.012 * (charges - 70) + 0.35 * tickets - 0.06 * (logins - 18)
         + 0.3 * (payment == "Bank transfer"))
churned = (rng.random(n_ch) < 1 / (1 + np.exp(-logit))).astype(int)
churn = pd.DataFrame({"customer_id": range(5001, 5001 + n_ch), "tenure_months": tenure,
                      "contract": contract, "monthly_charges": charges, "support_tickets": tickets,
                      "logins_last_30d": logins, "payment_method": payment, "churned": churned})
churn.to_csv(DATA / "churn.csv", index=False)

# ---------------------------------------------------------------- messy_sales
messy = pd.DataFrame([
    (1, "2024-01-05", "  rūta kazlauskas ", "Laptop Pro 14", "€1,299.00", "1", "VILNIUS"),
    (2, "05/01/2024", "Tomas Petrauskas", "wireless mouse", "24.90", "2", "kaunas"),
    (3, "Jan 7, 2024", "IEVA JANKAUSKAITĖ", "Desk Lamp", "EUR 39.90", "N/A", "Vilnius "),
    (4, "2024/01/09", "Mantas Stankevičius", "USB-C Hub", "49,90", "3", "Klaipėda"),
    (5, "2024-01-10", "Greta Vasiliauskaitė", "Office Chair", "€279", "1", "riga"),
    (6, "2024-01-10", "Greta Vasiliauskaitė", "Office Chair", "€279", "1", "riga"),
    (7, "11-01-2024", "lukas žukauskas", "Yoga Mat", "34.9", "", "TALLINN"),
    (8, "2024-01-12", "Jonas Butkus", "4K MONITOR 27", "389.00 EUR", "1", "Warsaw"),
    (9, "Jan 13 2024", "Agnė Paulauskaitė", "Gel Pens (12-pack)", "9.90", "5", "kaunas "),
    (10, "2024-01-14", "Paulius Urbonas", "standing desk", "€549.00", "1", "Vilnius"),
    (11, "2024-01-15", None, "Desk Lamp", "39.90", "2", "Vilnius"),
    (12, "2024-01-16", "Emilija Kavaliauskaitė", "Bookshelf", "-129.00", "1", "Riga"),
    (13, "not a date", "Karolis Kairys", "Notebook A5 (5-pack)", "12.50", "4", "KAUNAS"),
    (14, "2024-01-18", "Austėja Navickaitė", "Wireless Mouse ", "24.90", "1", "Tallinn"),
    (15, "2024-01-18", "Austėja Navickaitė", "Wireless Mouse ", "24.90", "1", "Tallinn"),
], columns=["record_id", "sale_date", "customer", "product", "price", "quantity", "city"])
messy.to_csv(DATA / "messy_sales.csv", index=False)

for name in ["customers", "products", "orders", "order_items", "ab_test", "churn", "messy_sales"]:
    print(f"{name:12} {len(pd.read_csv(DATA / f'{name}.csv')):>5} rows")
