import sys
import pandas as pd
import numpy as np

try:
    import arnio
    print("Arnio imported successfully!")
except ImportError:
    print("Could not import arnio")
    sys.exit(1)

df = pd.DataFrame({
    'col1': [1, 2, np.nan, 4],
    'col2': ['a', 'b', 'c', None],
    'col3': [pd.NaT, pd.NaT, pd.NaT, pd.NaT], # all NaT
    'col4': [{'a':1}, {'b':2}, {}, []], # dicts and lists inside
    'col5': [complex(1,2), 3, 4, 5] # complex numbers!
})

print("Testing auto_clean on weird datatypes...")
try:
    cleaned = arnio.auto_clean(df)
    print("auto_clean handled it!")
except Exception as e:
    print(f"BUG FOUND in auto_clean! {type(e).__name__}: {e}")

print("Testing profile...")
try:
    report = arnio.profile(df)
    print("profile handled it!")
except Exception as e:
    print(f"BUG FOUND in profile! {type(e).__name__}: {e}")

# test empty DataFrame
empty_df = pd.DataFrame()
print("Testing auto_clean on empty DataFrame...")
try:
    arnio.auto_clean(empty_df)
    print("auto_clean empty df passed")
except Exception as e:
    print(f"BUG FOUND in auto_clean empty df! {type(e).__name__}: {e}")

# test read_csv with missing file
print("Testing read_csv with missing file...")
try:
    arnio.read_csv("does_not_exist_xyz123.csv")
    print("read_csv handled missing file")
except FileNotFoundError:
    print("read_csv correctly raised FileNotFoundError")
except Exception as e:
    print(f"BUG FOUND in read_csv missing file! {type(e).__name__}: {e}")
