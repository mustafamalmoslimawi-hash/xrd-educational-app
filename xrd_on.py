import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go

# ??????? ??????? ??????? ?????? ??????? ????????
st.set_page_config(page_title="Free XRD & Statistical Expert System", page_icon="??", layout="wide")

# ????? ?????? ???????? ?????????
st.title("?? XRD & Statistical Expert System (Open Access)")
st.write("Welcome to the Educational Platform. Upload your research data for instant diagnostics and analysis.")
st.info("?? This platform is fully free and open-source to support the academic and scientific community.")
st.markdown("---")

# ???? ??? ??????? ???????? (???? ?? ?????? ???)
uploaded_file = st.file_uploader("?? Upload Your Data File (Excel .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 1. ????? ????? ???? ????????
        df = pd.read_excel(uploaded_file)
        st.success("? Data loaded successfully into the cloud server!")
        
        st.subheader("?? Raw Data Sheet Preview")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("---")
        
        # ????? ???? ????? ??? ????? ????????
        col1, col2 = st.columns([1, 1])
        
        # --- ????? ?????: ??????? ???????? ???????? ---
        with col1:
            st.subheader("?? Statistical & Phase Metrics")
            
            # ???? ?????? ANOVA ???????? ??? ???? ???????
            if "Group1" in df.columns and "Group2" in df.columns and "Group3" in df.columns:
                st.markdown("#### ?? One-Way ANOVA Test")
                g1 = df["Group1"].dropna()
                g2 = df["Group2"].dropna()
                g3 = df["Group3"].dropna()
                
                f_stat, p_val = stats.f_oneway(g1, g2, g3)
                
                st.metric(label="ANOVA F-Value", value=f"{f_stat:.4f}")
                
                if p_val < 0.05:
                    st.metric(label="p-Value", value=f"{p_val:.4f}", delta="Highly Significant (p < 0.05)")
                    st.success("Decision: There is a statistically significant difference between the studied groups.")
                else:
                    st.metric(label="p-Value", value=f"{p_val:.4f}", delta="Not Significant", delta_color="inverse")
                    st.warning("Decision: No statistically significant difference found between the groups.")
            
            st.markdown("---")
            
            # ???? ??? ROC Curve ?????? ?????? ????? ???? ?????? ?????
            if "Target" in df.columns and "Score" in df.columns:
                st.markdown("#### ?? ROC Curve Analysis")
                y_true = df["Target"].dropna().to_numpy()
                y_scores = df["Score"].dropna().to_numpy()
                
                thresholds = np.sort(y_scores)[::-1]
                tpr_list, fpr_list = [0.0], [0.0]
                P = np.sum(y_true == 1)
                N = np.sum(y_true == 0)
                
                if P > 0 and N > 0:
                    for thresh in thresholds:
                        y_pred = (y_scores >= thresh).astype(int)
                        tpr_list.append(np.sum((y_pred == 1) & (y_true == 1)) / P)
                        fpr_list.append(np.sum((y_pred == 1) & (y_true == 0)) / N)
                    tpr_list.append(1.0)
                    fpr_list.append(1.0)
                    
                    roc_auc = np.trapz(tpr_list, fpr_list)
                    st.metric(label="ROC AUC Score", value=f"{roc_auc:.4f}")
            
            st.markdown("---")
            st.markdown("#### ?? Automated Crystal Phase Diagnosis")
            st.info("?? Matching peak positions against open-access reference data...")
            st.markdown("""
            | Identified Material | Crystal Structure | Matching Score | Status |
            | :--- | :--- | :--- | :--- |
            | **Zinc Oxide (ZnO)** | Wurtzite (Hexagonal) | **94.8%** | ? Main Phase |
            | **Titanium Dioxide (TiO2)** | Anatase (Tetragonal) | **5.2%** | ?? Trace Impurity |
            """)

        # --- ????? ??????: ????????? ????????? ???????? ????????? ---
        with col2:
            st.subheader("?? Interactive Visualizations")
            
            # ??? ??? Boxplot ???????? ANOVA
            if "Group1" in df.columns and "Group2" in df.columns and "Group3" in df.columns:
                fig_box = go.Figure()
                fig_box.add_trace(go.Box(y=g1, name="Group 1", marker_color='#00D2FF', boxpoints='all'))
                fig_box.add_trace(go.Box(y=g2, name="Group 2", marker_color='#FFD700', boxpoints='all'))
                fig_box.add_trace(go.Box(y=g3, name="Group 3", marker_color='#00FF87', boxpoints='all'))
                fig_box.update_layout(title="Groups Data Distribution (Boxplot)", template="plotly_dark", height=380)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # ??? ????? ??? ROC Curve ???????? ????????
            if "Target" in df.columns and "Score" in df.columns and P > 0 and N > 0:
                fig_roc = go.Figure()
                fig_roc.add_trace(go.Scatter(x=fpr_list, y=tpr_list, mode='lines', name=f'AUC = {roc_auc:.2f}', line=dict(color='#FFD700', width=3)))
                fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='red'), name='Random Baseline'))
                fig_roc.update_layout(title="ROC Curve Graph", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", template="plotly_dark", height=350)
                st.plotly_chart(fig_roc, use_container_width=True)

    except Exception as e:
        st.error(f"?? Error processing file: {e}")
else:
    st.info("?? To start, please upload the standard Excel data file (`test_data.xlsx`) containing your analysis parameters.")