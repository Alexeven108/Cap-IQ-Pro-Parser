import st

from risklens.file_handler import upload_file

df = upload_file()
if df is not None:
    st.dataframe(df.head())
