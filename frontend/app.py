

####################################################################################################
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px

from backend.ingestion.file_handler import save_uploaded_file
from backend.parsing.parser import extract_text_from_file, parse_fields
from backend.db.db_utils import initialize_db, insert_receipt

from backend.algorithms.search import search_by_keyword, search_by_amount_range, search_by_date_pattern
from backend.algorithms.sort import sort_by_field
from backend.algorithms.aggregate import compute_basic_stats, vendor_frequency, monthly_trend


# ------------------ INIT ---------------------
st.set_page_config(page_title="Receipt Insights App", layout="wide")
initialize_db()


# ------------------ HELPERS ------------------
def get_all_receipts_df():
    conn = sqlite3.connect("data/db.sqlite3")
    df = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    return df


# ------------------ LAYOUT -------------------
st.title(" Receipt Insights Dashboard")

tab1, tab2, tab3 = st.tabs([" Upload", " Search & Sort", " Analytics"])


# ------------------ TAB 1: Upload & Parse -------------------
with tab1:
    st.header("Upload Your Receipt or Bill")
    st.markdown("Supported formats: `.jpg`, `.png`, `.pdf`, `.txt`")

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf", "txt"])

    if uploaded_file is not None:
        file_path = Path("data/uploads") / uploaded_file.name

        if file_path.exists():
            st.warning(" File already exists. Please rename or upload a different file.")
        else:
            with st.spinner("Validating and saving file..."):
                success, message = save_uploaded_file(uploaded_file)

            if success:
                st.success(message)

                # Process and parse the file
                text = extract_text_from_file(str(file_path))
                if text.strip():
                    parsed_data = parse_fields(text)
                    st.subheader("Parsed Receipt Data")
                    st.json(parsed_data)

                    insert_receipt(parsed_data)
                    st.success(" Receipt data saved to database.")
                else:
                    st.warning(" No text could be extracted from the file.")
            else:
                st.error(message)


# ------------------ TAB 2: Search & Sort -------------------
with tab2:
    st.header(" Search & Sort Your Receipts")
    df_all = get_all_receipts_df()

    if df_all.empty:
        st.info("No receipts found. Upload some in the 'Upload' tab.")
    else:
        st.subheader("All Receipts")
        st.dataframe(df_all, use_container_width=True)

        st.subheader("Search Filters")

        col1, col2, col3 = st.columns(3)
        with col1:
            keyword = st.text_input("Search by Vendor/Category")
        with col2:
            min_amt = st.number_input("Min Amount", min_value=0.0, value=0.0)
            max_amt = st.number_input("Max Amount", min_value=0.0, value=10000.0)
        with col3:
            date_pattern = st.text_input("Date Pattern (e.g., 2024-07)")

        if st.button(" Apply Search"):
            results = df_all.copy()

            if keyword:
                results = pd.DataFrame(search_by_keyword(keyword), columns=df_all.columns)
            if min_amt or max_amt:
                results = pd.DataFrame(search_by_amount_range(min_amt, max_amt), columns=df_all.columns)
            if date_pattern:
                results = pd.DataFrame(search_by_date_pattern(date_pattern), columns=df_all.columns)

            if not results.empty:
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No results found for the given criteria.")

        st.divider()

        st.subheader("Sort Records")
        sort_field = st.selectbox("Sort by", ["vendor", "date", "amount", "category"])
        ascending = st.radio("Order", ["Ascending", "Descending"], horizontal=True) == "Ascending"

        if st.button("↕ Sort Table"):
            sorted_data = sort_by_field(sort_field, ascending)
            st.dataframe(pd.DataFrame(sorted_data, columns=df_all.columns), use_container_width=True)


# ------------------ TAB 3: Analytics -------------------
with tab3:
    st.header(" Aggregated Analytics")

    df_all = get_all_receipts_df()
    if df_all.empty:
        st.info("No data available. Upload receipts to see analytics.")
    else:
        st.subheader("Summary Statistics")
        stats = compute_basic_stats()
        st.json(stats)

        st.subheader(" Monthly Spending Trend")
        monthly_data = monthly_trend()
        if monthly_data:
            fig_line = px.line(x=list(monthly_data.keys()), y=list(monthly_data.values()),
                               labels={"x": "Month", "y": "Amount"},
                               title="Monthly Spending Trend")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Not enough date data to compute trends.")

        st.subheader(" Vendor Frequency")
        vendor_data = vendor_frequency()
        if vendor_data:
            fig_bar = px.bar(x=list(vendor_data.keys()), y=list(vendor_data.values()),
                             labels={"x": "Vendor", "y": "Frequency"},
                             title="Vendor Occurrence")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No vendor data to visualize.")

















###################################################################################


# # import sys
# # from pathlib import Path

# # # Add project root to sys.path
# # sys.path.append(str(Path(__file__).resolve().parent.parent))


# # import os
# # import streamlit as st
# # from backend.ingestion.file_handler import save_uploaded_file
# # from backend.parsing.parser import extract_text_from_file, parse_fields
# # st.set_page_config(page_title="Receipt Uploader - Phase 1", layout="centered")
# # st.title(" Upload Your Receipt or Bill")

# # st.markdown("Supported formats: `.jpg`, `.png`, `.pdf`, `.txt`")

# # uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf", "txt"])

# # if uploaded_file is not None:
# #     with st.spinner("Validating and saving file..."):
# #         success, message = save_uploaded_file(uploaded_file)
# #     if success:
# #         st.success(message)
# #     else:
# #         st.error(message)



# # # After successful upload
# # if success:
# #     file_path = os.path.join("data/uploads", uploaded_file.name)
# #     text = extract_text_from_file(file_path)
    
# #     if text.strip():
# #         parsed_data = parse_fields(text)
# #         st.subheader("Parsed Receipt Data")
# #         st.json(parsed_data)
# #     else:
# #         st.warning("No text could be extracted from the file.")



# import sys
# from pathlib import Path

# # Add project root to sys.path
# sys.path.append(str(Path(__file__).resolve().parent.parent))

# import os
# import streamlit as st
# from backend.ingestion.file_handler import save_uploaded_file
# from backend.parsing.parser import extract_text_from_file, parse_fields
# from backend.db.db_utils import initialize_db, insert_receipt
# import pandas as pd
# import plotly.express as px

# from backend.algorithms.search import search_by_keyword, search_by_amount_range, search_by_date_pattern
# from backend.algorithms.sort import sort_by_field
# from backend.algorithms.aggregate import compute_basic_stats, vendor_frequency, monthly_trend

# st.set_page_config(page_title="Receipt Uploader - Phase 1", layout="centered")
# initialize_db()

# st.title(" Upload Your Receipt or Bill")

# st.markdown("Supported formats: `.jpg`, `.png`, `.pdf`, `.txt`")

# uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf", "txt"])

# if uploaded_file is not None:
#     with st.spinner("Validating and saving file..."):
#         success, message = save_uploaded_file(uploaded_file)
#     if success:
#         st.success(message)
#         # After successful upload
#         file_path = os.path.join("data/uploads", uploaded_file.name)
#         text = extract_text_from_file(file_path)
#         if text.strip():
#             parsed_data = parse_fields(text)
#             st.subheader("Parsed Receipt Data")
#             st.json(parsed_data)
#             insert_receipt(parsed_data)
#             st.success("Receipt data saved to database.")
#         else:
#             st.warning("No text could be extracted from the file.")
#     else:
#         st.error(message)
# def get_all_receipts_df():
#     import sqlite3
#     conn = sqlite3.connect("data/db.sqlite3")
#     df = pd.read_sql_query("SELECT * FROM receipts", conn)
#     conn.close()
#     return df

# st.header("📑 All Receipts")
# df_all = get_all_receipts_df()
# st.dataframe(df_all)
# st.subheader("🔍 Search Filters")

# col1, col2, col3 = st.columns(3)

# with col1:
#     keyword = st.text_input("Search by Vendor/Category")

# with col2:
#     min_amt = st.number_input("Min Amount", min_value=0.0, value=0.0)
#     max_amt = st.number_input("Max Amount", min_value=0.0, value=10000.0)

# with col3:
#     date_pattern = st.text_input("Search by Date Pattern (e.g., 2024-07)")

# if st.button("Apply Search"):
#     results = []

#     if keyword:
#         results = search_by_keyword(keyword)
#     elif min_amt or max_amt:
#         results = search_by_amount_range(min_amt, max_amt)
#     elif date_pattern:
#         results = search_by_date_pattern(date_pattern)

#     if results:
#         st.dataframe(pd.DataFrame(results, columns=df_all.columns))
#     else:
#         st.warning("No results found.")
# st.subheader("↕️ Sort Records")

# sort_field = st.selectbox("Sort by", ["vendor", "date", "amount", "category"])
# ascending = st.radio("Order", ["Ascending", "Descending"]) == "Ascending"

# if st.button("Sort Table"):
#     sorted_data = sort_by_field(sort_field, ascending)
#     st.dataframe(pd.DataFrame(sorted_data, columns=df_all.columns))
# st.subheader("📊 Aggregated Statistics")

# stats = compute_basic_stats()
# st.json(stats)

# st.subheader("📈 Monthly Spend Trend")
# monthly_data = monthly_trend()
# fig_line = px.line(x=list(monthly_data.keys()), y=list(monthly_data.values()),
#                    labels={"x": "Month", "y": "Amount"},
#                    title="Monthly Spending Trend")
# st.plotly_chart(fig_line)

# st.subheader("🏷️ Vendor Frequency")
# vendor_data = vendor_frequency()
# fig_bar = px.bar(x=list(vendor_data.keys()), y=list(vendor_data.values()),
#                  labels={"x": "Vendor", "y": "Frequency"},
#                  title="Top Vendors")
# st.plotly_chart(fig_bar)







