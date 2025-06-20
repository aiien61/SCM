from typing import Set, Dict, Optional, Tuple
from datetime import timedelta, datetime
from icecream import ic
from rich import print
import polars as pl


def level_the_ruins(ruins_df: pl.DataFrame, bottleneck_resources: Set[str]) -> pl.DataFrame:
    """
    「剷平廢墟」流程：
    1. 找出瓶頸資源上的所有工作。
    2. 依其理想開始時間排序。
    3. 依序排程，解決時間衝突。
    4. 將因排程而產生的延遲，同步反應到該訂單的前序和後續工序上。
    """
    ic.enable()
    ic(ruins_df)
    ic(bottleneck_resources)

    # 建立一個可修改的 DataFrame 複本
    leveled_df: pl.DataFrame = ruins_df.clone()
    ic(leveled_df)

    # 將 DataFrame 轉為以 (order_id, step_no) 為 key 的字典，方便快速更新
    tasks_dict: Dict[tuple, Dict] = {
        (row['order_id'], row['step_no']): row for row in leveled_df.iter_rows(named=True)
    }
    ic(tasks_dict)

    # 篩選出瓶頸上的工作，並依理想開始時間排序
    bottlenect_tasks = (
        leveled_df.filter(pl.col('resource').is_in(bottleneck_resources)).sort("start_time")
    )
    print(bottlenect_tasks)

    # 用來記錄瓶頸資源最後的完工時間
    last_bottleneck_end_time: Optional[datetime] = None

    # 獲取每個訂單的最大 step_no，方便後續的連鎖反應
    max_steps = leveled_df.group_by('order_id').agg(pl.max('step_no')).to_dict(as_series=False)
    ic(max_steps)
    max_step_map = {order: step for order, step in zip(max_steps['order_id'], max_steps['step_no'])}
    ic(max_step_map)

    for task in bottlenect_tasks.iter_rows(named=True):
        ic(task)
        order_id: str = task['order_id']
        step_no: int = task['step_no']
        duration: float = timedelta(hours=task['total_process_time'])
        ic(duration)
        ic(last_bottleneck_end_time)

        # 第一次處理瓶頸工作
        if last_bottleneck_end_time is None:
            last_bottleneck_end_time = task['end_time']
            print('-'*30)
            continue

        # 檢查是否有衝突 (當前工作的理想開始時間 < 上一工作的實際結束時間)
        if task['start_time'] < last_bottleneck_end_time:
            # 延遲是從理想開始時間到實際可以開始的時間
            delay = last_bottleneck_end_time - task['start_time']
            ic(delay)

            # --- 更新當前瓶頸工序 ---
            new_start_time: datetime = last_bottleneck_end_time
            new_end_time: datetime = new_start_time + duration
            ic(new_start_time)
            ic(new_end_time)

            tasks_dict[(order_id, step_no)]['start_time'] = new_start_time
            tasks_dict[(order_id, step_no)]['end_time'] = new_end_time
            ic(tasks_dict)

            # --- 1. 連鎖反應：倒推修改所有【前序】工序 ---
            for i in range(1, step_no):
                prev_task_key: Tuple[str, int] = (order_id, i)
                ic(prev_task_key)
                if prev_task_key in tasks_dict:
                    tasks_dict[prev_task_key]['start_time'] -= delay
                    tasks_dict[prev_task_key]['end_time'] -= delay

                ic(tasks_dict)

            # --- 2. 連鎖反應：正向修改所有【後續】工序 ---
            previous_op_end_time: datetime = new_end_time
            for i in range(step_no + 1, max_step_map[order_id] + 1):
                next_task_key: Tuple[str, int] = (order_id, i)
                if next_task_key in tasks_dict:
                    # TODO: get max{前一工序的新結束時間, 其他訂單的當前工序結束時間}
                    # 後續工序的新開始時間 = 前一工序的新結束時間
                    tasks_dict[next_task_key]['start_time'] = previous_op_end_time

                    # 計算並更新後續工序的新結束時間
                    next_duration = timedelta(hours=tasks_dict[next_task_key]['total_process_time'])
                    tasks_dict[next_task_key]['end_time'] = previous_op_end_time + next_duration

                    # 更新 "前一工序結束時間" 以便下一次迭代使用
                    previous_op_end_time = tasks_dict[next_task_key]['end_time']
            
            # 更新瓶頸的最後完工時間
            last_bottleneck_end_time = new_end_time
        
        else:
            # 沒有衝突，直接更新瓶頸的最後完工時間
            last_bottleneck_end_time = task['end_time']
    
    # 從更新後的字典重建 DataFrame
    return pl.DataFrame(list(tasks_dict.values())).sort('order_id', 'step_no')
