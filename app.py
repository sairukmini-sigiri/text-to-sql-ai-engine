import sqlite3
import pandas as pd
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI SQL Analytics Engine", layout="wide")
st.title("Natural Language Text-to-SQL Analytics Engine")

# Fetch API Key from Streamlit secrets or user sidebar input
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

schema_info = """
Table: sales
Columns: order_id (INTEGER), product_name (TEXT), category (TEXT), revenue (REAL), order_date (DATE)
"""

user_query = st.text_input("Ask a business question about the data:", "What is our total revenue by product category?")

if st.button("Generate & Run Query"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    else:
        client = Groq(api_key=api_key)
       
        # System prompt to generate clean SQL
        prompt = f"""
        You are an expert SQL engineer. Given the following database schema, generate ONLY a valid SQLite query to answer the user request.
        Do not include markdown formatting, code blocks (```), or explanations. Return strictly raw SQL.

        Schema:
        {schema_info}

        User Request: {user_query}
        """

        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
           
            sql_query = response.choices[0].message.content.strip()
            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")

            # Execute Query on local SQLite DB
            conn = sqlite3.connect('analytics.db')
            df = pd.read_sql_query(sql_query, conn)
            conn.close()

            st.subheader("Query Results")
            st.dataframe(df)

            # Generate AI Executive Summary from dataframe output
            summary_prompt = f"Summarize the following data table in 2 concise business bullet points:\n{df.to_string()}"
            summary_resp = client.chat.completions.create(
                messages=[{"role": "user", "content": summary_prompt}],
                model="llama-3.3-70b-versatile",
            )
           
            st.subheader("Executive Insight")
            st.write(summary_resp.choices[0].message.content)

        except Exception as e:
            st.error(f"Error executing request: {e}")