import polars as pl
from pathlib import Path
from icecream import ic

def load_orders(filepath: str) -> pl.DataFrame:
    return pl.read_csv(filepath, try_parse_dates=True)

def load_routing(filepath: str) -> pl.DataFrame:
    return pl.read_csv(filepath)

def generate_schedule_input(orders_df: pl.DataFrame, routing_df: pl.DataFrame) -> pl.DataFrame:
    """
    將訂單與製程路徑依照 product 合併展開為每個工序的排程輸入資料
    """

    # 合併訂單與製程
    expanded_df = orders_df.join(routing_df, on="product", how="inner")

    # 計算總工時
    expanded_df = expanded_df.with_columns([
        (pl.col("quantity") * pl.col("process_time_per_unit")).alias("total_process_time")
    ])

    # 如果 due_date 不是 date 型別，再轉換
    if expanded_df.schema["due_date"] != pl.Date:
        expanded_df = expanded_df.with_columns([
            pl.col("due_date").str.strptime(pl.Date, "%Y-%m-%d")
        ])

    # 排序
    expanded_df = expanded_df.sort(["due_date", "order_id", "step_no"])

    return expanded_df

# 📌 若此檔單獨執行，做測試
if __name__ == "__main__":
    orders_path = Path("./sample_orders.csv")
    routing_path = Path("./sample_routing.csv")

    orders = load_orders(orders_path)
    routing = load_routing(routing_path)
    schedule_input = generate_schedule_input(orders, routing)

    ic(orders)
    ic(routing)
    ic(schedule_input)
    ic(schedule_input.schema)
    

