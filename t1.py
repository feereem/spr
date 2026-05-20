import pandas as pd

# 1. โหลดข้อมูลและแสดงข้อมูลเบื้องต้น
dfs = {f: pd.read_csv(f) for f in ["sales_transactions.csv", "customers.csv", "products.csv"]}
sales, customers, products = dfs.values()

for name, df in dfs.items():
    display(df.head(5))
    print(f"--- {name} ---\n{df.dtypes}\nMissing:\n{df.isnull().sum()}\n")

# 2. ฟังก์ชัน Helper สำหรับตรวจสอบความผิดปกติ (ใช้ .str.replace ธรรมดา)
def clean_num(df, c):
    return pd.to_numeric(df[c].astype(str).str.replace("$", "", encoding=None), errors="coerce")

def check_dates(df, cols):
    return sum((pd.to_datetime(df[c], errors="coerce").dt.year.between(2010, 2025) == False).sum() for c in cols)

# 3. ประมวลผลและเขียน Report
report = ""
for name, df in dfs.items():
    # ตรวจหาค่าติดลบในคอลัมน์ที่เป็นตัวเลขทั้งหมด
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.union(["price", "cost", "discount_amount"])
    neg_count = sum((clean_num(df, c) < 0).sum() for c in num_cols if c in df.columns)

    # ตรวจสอบเงื่อนไขเฉพาะของแต่ละไฟล์ (เปลี่ยนวิธีเช็คไม่ให้ใช้ RegEx)
    invalid_ids = (~sales.customer_id.isin(customers.customer_id) | ~sales.product_id.isin(products.product_id)).sum() if name == "sales_transactions.csv" else 0
    unexp = (~df["gender"].isin(["M", "F"])).sum() if name == "customers.csv" else (~df["category"].isin(["Pastries", "Bread", "Tarte"])).sum() if name == "products.csv" else 0
    
    # 💡 จุดที่เปลี่ยน: 
    # - เช็คอีเมล: ใช้ .str.isupper() หรือใช้การเช็คความต่างถ้าแปลงเป็นตัวพิมพ์เล็ก
    # - เช็คเครื่องหมาย $: ใช้ .str.contains() แบบปิดโหมด regex (regex=False)
    if name == "customers.csv":
        format_issues = (df["email"].astype(str).apply(lambda x: any(c.isupper() for c in x))).sum()
    elif name == "products.csv":
        format_issues = df[["price", "cost"]].astype(str).apply(lambda s: s.str.contains("$", regex=False)).sum().sum()
    else:
        format_issues = 0

    # สร้าง Text Block
    date_cols = [c for c in df.columns if "date" in c]
    block = f"### File: {name}\nData Types:\n" + "".join(f"  - {k}: {v}\n" for k, v in df.dtypes.items())
    block += f"\nInconsistencies:\n"
    block += f"  - Invalid Dates: {check_dates(df, date_cols)}\n"
    block += f"  - Negative Values: {neg_count}\n"
    block += f"  - Invalid IDs: {int(invalid_ids)}\n"
    block += f"  - Unexpected Values: {int(unexp)}\n"
    block += f"  - Formatting Issues: {int(format_issues)}\n"
    block += "-" * 40 + "\n"
    
    print(block)
    report += block

open("Session1_DataExploration.txt", "w", encoding="utf-8").write(report.strip())
print("✅ Saved Session1_DataExploration.txt")
