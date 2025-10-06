import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Security Enhancement Checker", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:#800000;'>🔐 Security Enhancement Checker</h1>
    <p style='text-align:center; font-size:18px; color:#FF8C00;'>
        Evaluate authentication methods by Accuracy, Privacy, Effort, and Intrusiveness.
    </p>
""", unsafe_allow_html=True)

# ---------------------------
# CONNECT TO DATABASE
# ---------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sphinx1906",
        database="MyDatabase"
    )
    query = "SELECT Name, Accuracy, Intrusiveness, Privacy, Effort FROM AuthenticationFactor"
    df = pd.read_sql(query, conn)
    conn.close()
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

# ---------------------------
# CALCULATE COMPOSITE SCORE
# ---------------------------
df["CompositeScore"] = (
    0.4 * df["Accuracy"]
    + 0.3 * (10 - df["Intrusiveness"])
    + 0.2 * df["Privacy"]
    + 0.1 * (10 - df["Effort"])
)

df = df.sort_values(by="CompositeScore", ascending=False)

# ---------------------------
# CHART COLORS
# ---------------------------
colors = ["#FF8C00", "#800000", "#D2691E", "#B22222"]

# ---------------------------
# OVERALL RESULTS
# ---------------------------
st.markdown("## 📊 Overall Evaluation (All Methods)")

# 1️⃣ Metrics Comparison Chart
fig1, ax1 = plt.subplots(figsize=(12, 6))
df_plot = df.set_index("Name")[["Accuracy", "Privacy", "Effort", "Intrusiveness"]]
df_plot.plot(
    kind="bar",
    ax=ax1,
    linewidth=1.5,
    edgecolor="black",
    color=colors
)
ax1.set_title("All Methods – Metric Comparison", fontsize=14, color="#800000", weight="bold")
ax1.set_ylabel("Score (0–10)")
ax1.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.xticks(rotation=45, ha="right")

# Save image
fig1.savefig("chart_all_metrics.png", dpi=300, bbox_inches="tight")
st.pyplot(fig1)

# 2️⃣ Composite Score Chart
fig2, ax2 = plt.subplots(figsize=(12, 6))
df_plot2 = df.set_index("Name")["CompositeScore"]
df_plot2.plot(kind="bar", color="#FF8C00", ax=ax2, edgecolor="black", linewidth=1.5)
ax2.set_title("All Methods – Composite Scores", fontsize=14, color="#800000", weight="bold")
ax2.set_ylabel("Composite Score")
ax2.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.xticks(rotation=45, ha="right")

# Save image
fig2.savefig("chart_all_composite.png", dpi=300, bbox_inches="tight")
st.pyplot(fig2)

# Save CSV
df.to_csv("all_methods_results.csv", index=False)
st.success("✅ Saved: all_methods_results.csv, chart_all_metrics.png, chart_all_composite.png")

# ---------------------------
# USER SELECTION
# ---------------------------
st.markdown("## 🎯 Select Authentication Methods to Compare")

selected_methods = st.multiselect(
    "Select authentication methods to include:",
    options=df["Name"].tolist(),
    default=[]
)

if selected_methods:
    df_selected = df[df["Name"].isin(selected_methods)]
    st.dataframe(df_selected[["Name", "CompositeScore"]])

    # ---------------------------
    # STRENGTHS & WEAKNESSES
    # ---------------------------
    st.markdown("## 💬 Strengths & Weaknesses")
    for _, row in df_selected.iterrows():
        st.markdown(f"### {row['Name']}")
        st.write("• ✅ High Accuracy" if row["Accuracy"] >= 8 else "• ⚠️ Lower Accuracy")
        st.write("• ✅ Good Privacy" if row["Privacy"] >= 7 else "• ⚠️ Privacy Risk")
        st.write("• ✅ Low Effort" if row["Effort"] <= 4 else "• ⚠️ High Effort Required")
        st.write("• ✅ User-Friendly" if row["Intrusiveness"] <= 4 else "• ⚠️ Disruptive Login")
        st.markdown("---")

    # ---------------------------
    # SELECTED CHARTS
    # ---------------------------
    st.markdown("### 📊 Metric Comparison (Selected Methods)")

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    df_sel_plot = df_selected.set_index("Name")[["Accuracy", "Privacy", "Effort", "Intrusiveness"]]
    df_sel_plot.plot(
        kind="bar",
        ax=ax3,
        linewidth=1.5,
        edgecolor="black",
        color=colors
    )
    ax3.set_title("Selected Methods – Metric Comparison", fontsize=14, color="#800000", weight="bold")
    ax3.set_ylabel("Score (0–10)")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=45, ha="right")

    # Save image
    fig3.savefig("chart_selected_metrics.png", dpi=300, bbox_inches="tight")
    st.pyplot(fig3)

    st.markdown("### 🧮 Composite Scores (Selected Methods)")

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    df_sel_plot2 = df_selected.set_index("Name")["CompositeScore"]
    df_sel_plot2.plot(kind="bar", color="#FF8C00", ax=ax4, edgecolor="black", linewidth=1.5)
    ax4.set_title("Selected Methods – Composite Scores", fontsize=14, color="#800000", weight="bold")
    ax4.set_ylabel("Composite Score")
    ax4.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=45, ha="right")

    # Save image
    fig4.savefig("chart_selected_composite.png", dpi=300, bbox_inches="tight")
    st.pyplot(fig4)

    # Save CSV
    df_selected.to_csv("selected_methods_results.csv", index=False)
    st.success("✅ Saved: selected_methods_results.csv, chart_selected_metrics.png, chart_selected_composite.png")

    # ---------------------------
    # AUTOMATED RECOMMENDATION
    # ---------------------------
    top_method = df_selected.iloc[0]
    recommendation = []
    if top_method["Accuracy"] >= 8:
        recommendation.append("high accuracy")
    if top_method["Privacy"] >= 7:
        recommendation.append("strong privacy")
    if top_method["Effort"] <= 4:
        recommendation.append("low effort")
    if top_method["Intrusiveness"] <= 4:
        recommendation.append("user-friendly design")

    st.markdown("## 🏆 Recommendation")
    st.success(
        f"**Top Recommendation:** {top_method['Name']} "
        f"(Composite Score: {round(top_method['CompositeScore'], 2)})\n\n"
        f"This method is recommended because it demonstrates: {', '.join(recommendation)}."
    )
else:
    st.info("Please select at least one authentication method to view comparisons.")
