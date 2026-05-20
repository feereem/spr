import pandas as pd

s, c, p = map(pd.read_csv, ["sales_transactions.csv", "customers.csv", "products.csv"])
for n, d in zip(["sales", "customers", "products"], [s, c, p]):
    print(f"\n=== {n} ==="); display(d.head())

# ยุบฟังก์ชันช่วยเช็ค (แปลงเป็นเลขเพื่อเช็คติดลบ / เช็ควันที่)
_n = lambda d, cl: sum((pd.to_numeric(d[x].astype(str).str.replace("$", "", regex=False), errors="coerce") < 0).sum() for x in cl if x in d.columns)
_d = lambda d, cl: sum((pd.to_datetime(d[x], errors="coerce").dt.year.between(2010, 2025) == False).sum() for x in cl)

# รวบ Array เงื่อนไขการเช็คให้สั้นลง
ch = [
    ("sales_transactions.csv", s, [_d(s, ["date"]), _n(s, ["quantity", "price", "discount_amount"]), (~s.customer_id.isin(c.customer_id) | ~s.product_id.isin(p.product_id)).sum(), 0, 0]),
    ("customers.csv", c, [_d(c, ["join_date", "last_purchase_date"]), _n(c, ["total_spending", "average_order_value"]), 0, (~c.gender.isin(["M", "F"]) & c.gender.notna()).sum(), (c.email.str.upper() == c.email).sum()]),  # เช็คตัวพิมพ์ใหญ่แบบไม่ต้องพึ่ง Regex
    ("products.csv", p, [_d(p, ["introduced_date"]), _n(p, ["price", "cost"]), 0, (~p.category.isin(["Pastries", "Bread", "Tarte"]) & p.category.notna()).sum(), p[["price", "cost"]].astype(str).apply(lambda x: x.str.contains("$", regex=False)).sum().sum()]),  # เอา r'\$' ออก ใช้ regex=False แทน
]

# ยุบ String Formatting ตอนเขียนไฟล์
lbl = ["Invalid Dates", "Negative Values", "Invalid IDs", "Unexpected Values", "Formatting Issues"]
out = [f"### File: {n}\nData Types:\n" + "".join(f" - {k}: {v}\n" for k, v in df.dtypes.items()) + "\nInconsistencies:\n" + "".join(f" - {k}: {v}\n" for k, v in zip(lbl, v)) for n, df, v in ch]

open("Session1_DataExploration_short.txt", "w", encoding="utf-8").write(f"\n{'-'*30}\n".join(out) + f"\n{'-'*30}\n")
