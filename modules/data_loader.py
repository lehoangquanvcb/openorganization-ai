import pandas as pd
from pathlib import Path
FILES=["employees","monthly_metrics","organization","kpi_cascade","competency","succession","culture","strategy","transformation","process_log","documents","meetings","agent_views","network","leaders","knowledge","organization_memory","data_dictionary"]
def load_all(data_dir: Path):
    out={}
    for f in FILES:
        try: out[f]=pd.read_csv(data_dir/f"{f}.csv")
        except Exception: out[f]=pd.DataFrame()
    return out
