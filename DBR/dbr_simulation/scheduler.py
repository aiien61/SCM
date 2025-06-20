from typing import List, Dict
from datetime import datetime, timedelta
from icecream import ic
import polars as pl

# Intentionally create ruins 
def create_ruins_schedule(df: pl.DataFrame, shipping_buffer: timedelta) -> pl.DataFrame:
    """
    使用倒推法 (Backward Scheduling) 從交期開始安排理想時程，以建立「廢墟」。
    這個階段故意不處理資源衝突。
    """
    ic.disable()
    ic(shipping_buffer)
    # 儲存每個訂單的下一道工序的開始時間，用於倒推
    # key: (order_id, step_no), value: start_datetime
    next_step_start_times: Dict[tuple[str, int], datetime] = {}

    results: List[dict] = []

    # 必須從最後一道工序開始倒推，所以將 DataFrame 反轉
    for row in df.sort("due_date", "order_id", "step_no", descending=True).iter_rows(named=True):
        ic(row)
        order_id: str = row['order_id']
        step_no: int = row['step_no']
        due_date: datetime.date = row['due_date']
        duration_hours: float = row['total_process_time']

        # 找出本工序的結束時間
        # 如果是最後一道工序，結束時間 = 交期 - 出貨緩衝
        # 否則，結束時間 = 下一道工序的開始時間
        is_last_step: bool = (order_id, step_no + 1) not in df.select(['order_id', 'step_no']).rows()
        if is_last_step:
            # 假設 due_date 是當天結束，所以先轉成 datetime
            
            # due_date: date type
            # datetime.min.time(): time type of hour 0 minute 0
            # datetime.combine(date, time): date + time -> datetime type
            start_of_due_date: datetime = datetime.combine(due_date, datetime.min.time())
            end_of_due_date: datetime = start_of_due_date + timedelta(days=1)
            scheduled_end_time: datetime = end_of_due_date - shipping_buffer

        else:
            scheduled_end_time: datetime = next_step_start_times[(order_id, step_no + 1)]
        
        # 計算開始時間
        scheduled_start_time: datetime = scheduled_end_time - timedelta(hours=duration_hours)

        # 記錄本工序的開始時間，給前一道工序參考
        next_step_start_times[(order_id, step_no)] = scheduled_start_time

        # 加入結果
        results.append({
            **row,
            "start_time": scheduled_start_time,
            "end_time": scheduled_end_time
        })

        ic(results)
        print('-'*30)

    # 將結果轉為 DataFrame 並恢復原始排序
    return pl.DataFrame(results).sort("due_date", "order_id", "step_no")
