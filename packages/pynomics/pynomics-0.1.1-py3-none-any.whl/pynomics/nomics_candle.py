from pydantic import BaseModel, Field
from nomics import Nomics  # type:ignore
import json
from typing import List, Optional
import pandas as pd
from datetime import datetime, timedelta


class VolumeTransparency(BaseModel):
    _: Optional[str] = Field(None, alias="?")
    A: Optional[str]
    B: Optional[str]
    D: Optional[str] = None


class NomicsCandle(BaseModel):
    timestamp: str
    open: str
    high: str
    low: str
    close: str
    volume: str
    transparent_open: str
    transparent_high: str
    transparent_low: str
    transparent_close: str
    transparent_volume: str
    volume_transparency: VolumeTransparency


class NomicsCandles(BaseModel):
    candles: Optional[List[NomicsCandle]] = []

    def to_dataframe(self, save: bool = False, currency: str = None):
        df = pd.DataFrame([item.dict() for item in self.candles])
        if save:
            df.to_csv(f"{currency}_hourly.csv", index=False)
        return df

    def from_json_file(self, json_path: str):
        with open(json_path) as f:
            data = json.load(f)
        for item in data:
            self.candles += [NomicsCandle(**item)]
        return self


def str2nomics_timestamp(date_: str, delta: int = 0):
    date_new = datetime.strptime(date_, "%Y-%m-%dT%H:%M:%SZ")
    date_new = date_new + timedelta(days=delta)
    date_new = str(date_new).replace(" ", "T") + "Z"
    return date_new


def fetch_nomics_hourly(*, currency: str, i: int = 1, key: str = ""):
    all_data: list = []
    year = "2017"
    for i in range(i):
        try:
            start_dt = str2nomics_timestamp(f"{year}-01-01T00:00:00Z", delta=7 * i)
            print(f"Fetching hourly data for {currency} starting from {start_dt}")
            data = nomics.Candles.get_candles(
                interval="1h",
                currency=currency,
                start=start_dt,
            )
            all_data += data
            json_object = json.dumps(all_data, indent=2)
            with open(f"nomics_{currency}_hourly.json", "w") as f:
                f.write(json_object)
        except Exception as e:
            print(
                f"[FAIL] Fetching hourly data for {currency} starting from {start_dt}:Error: {e}"
            )
    print(f"End reached for currency {currency}!")


if __name__ == "__main__":
    x = NomicsCandles().from_json_file(
        json_path="/Users/soumendra/Documents/project-zoo/omnia-server/data/seed/json/nomics_BCH_hourly.json"
    )
    print(x.candles[10])
