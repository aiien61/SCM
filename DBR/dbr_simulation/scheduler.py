from typing import List, Dict
from datetime import datetime, timedelta
from icecream import ic
import polars as pl


def schedule_fifo(df: pl.DataFrame, start_time: datetime) -> pl.DataFrame:
    """
    使用 FIFO 排程演算法模擬廢墟建立：
    - 同一訂單工序需依 step_no 順序執行
    - 每個資源一次只能處理一件事
    - 單機無重工、無平行
    """
    ic(start_time)

    # 儲存每台資源的可用時間
    resource_available: Dict[str, datetime] = {}

    # 儲存每個 order_id 對應 step_no 的完工時間
    order_step_end: Dict[str, Dict[int, datetime]] = {}

    results = []

    for row in df.iter_rows(named=True):
        ic(resource_available)
        ic(order_step_end)
        ic(results)
        ic(row)
        order_id = row["order_id"]
        step_no = row['step_no']
        resource = row["resource"]
        duration_hours = row["total_process_time"]

        # 取得瓶頸時間（資源的可用時間）
        res_ready = resource_available.get(resource, start_time)
        ic(res_ready)

        # 前一道工序的完工時間（若有）
        if step_no > 1:
            prior_step_end = order_step_end.get(order_id, {}).get(step_no - 1, start_time)
        else:
            prior_step_end = start_time
        ic(prior_step_end)
        
        # 排程開始時間是 max(資源可用, 上道工序完工)
        scheduled_start_time = max(res_ready, prior_step_end)
        scheduled_end_time = scheduled_start_time + timedelta(hours=duration_hours)

        # 更新可用時間與完工記錄
        resource_available[resource] = scheduled_end_time
        order_step_end.setdefault(order_id, {})[step_no] = scheduled_end_time

        # 加入結果
        results.append({
            **row,
            "start_time": scheduled_start_time,
            "end_time": scheduled_end_time
        })

        print('-'*30)

    ic(resource_available)
    ic(order_step_end)
    
    # 回傳為 DataFrame
    return pl.DataFrame(results)
