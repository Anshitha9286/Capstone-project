import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data"


@st.cache_data
def load(name):
    return pd.read_csv(DATA / f"{name}.csv")


@st.cache_data
def load_json(name):
    with open(DATA / f"{name}.json") as f:
        return json.load(f)
