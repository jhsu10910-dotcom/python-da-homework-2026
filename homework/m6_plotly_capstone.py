"""
M6 Plotly 互動儀表板 & Capstone — 課後作業
===========================================
情境：從原始資料到互動式儀表板，完成完整的資料分析 pipeline。

資料路徑：
  - datasets/ecommerce/orders_raw.csv（原始髒資料）
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.bar()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    rev_by_cat = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(rev_by_cat, x='category', y='amount', title="Revenue by Category")
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv", parse_dates=['order_date'])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly_rev = df.groupby('month')['amount'].sum().reset_index()
    fig = px.line(monthly_rev, x='month', y='amount', title="Monthly Revenue Trend", markers=True)
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    fig = px.pie(df, names='vip_level', values='amount', title="Revenue Share by VIP Level")
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
    # 讀取原始訂單資料
    orders = pd.read_csv(raw_path)
    
    # 標準化欄位名稱（去除空格，轉小寫）
    orders.columns = orders.columns.str.strip().str.lower()
    
    # 重命名欄位
    orders = orders.rename(columns={
        'order_id ': 'order_id',
        'product_id': 'product_id',
        ' qty': 'qty'
    })
    
    # 清理金額：移除 $ 符號和逗號，轉為 float
    orders['amount'] = orders['amount'].astype(str).str.replace('$', '').str.replace(',', '')
    orders['amount'] = pd.to_numeric(orders['amount'], errors='coerce')
    
    # 解析日期
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
    
    # 移除缺值
    orders = orders.dropna()
    
    # 去重
    orders = orders.drop_duplicates()
    
    # 讀取客戶資料和商品資料
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    # 合併客戶資料
    orders = orders.merge(customers, on='customer_id', how='left')
    
    # 合併商品資料
    orders = orders.merge(products, on='product_id', how='left')
    
    return orders


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict：
    {
        "total_revenue": float,       # 總營收
        "order_count": int,           # 訂單數
        "active_customers": int,      # 不重複客戶數
        "avg_order_value": float,     # 平均客單價
    }
    """
    return {
        "total_revenue": float(df['amount'].sum()),
        "order_count": len(df),
        "active_customers": df['customer_id'].nunique(),
        "avg_order_value": float(df['amount'].mean()),
    }


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖：
    - X：商品單價 (unit_price)
    - Y：訂單金額 (amount)
    - 顏色：商品類別 (category)
    - hover 顯示：商品名稱 (product_name)
    回傳 plotly Figure 物件
    提示：px.scatter(hover_data=['product_name'])
    """
    fig = px.scatter(
        df,
        x='unit_price',
        y='amount',
        color='category',
        hover_data=['product_name'],
        title="Unit Price vs Order Amount by Category"
    )
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：完整的互動式儀表板

    流程：
    1. 清理 orders_raw.csv + 合併三張表
    2. 建立 2×2 subplot dashboard（用 plotly make_subplots）：
       - 左上：月營收趨勢 (line)
       - 右上：Top 10 商品營收 (bar)
       - 左下：各地區營收 (bar)
       - 右下：類別營收佔比 (pie/donut)
    3. 設定整體標題

    回傳 plotly Figure 物件
    提示：from plotly.subplots import make_subplots
    """
    # 清理和合併資料
    df = yellow_clean_and_merge(
        "datasets/ecommerce/orders_raw.csv",
        "datasets/ecommerce/customers.csv",
        "datasets/ecommerce/products.csv"
    )
    
    # 建立 2×2 subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Monthly Revenue Trend",
            "Top 10 Products by Revenue",
            "Revenue by Region",
            "Revenue Share by Category"
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"type": "pie"}]
        ]
    )
    
    # 1. 左上：月營收趨勢 (line)
    df_copy = df.copy()
    df_copy['month'] = df_copy['order_date'].dt.to_period('M').astype(str)
    monthly_rev = df_copy.groupby('month')['amount'].sum().reset_index()
    fig.add_trace(
        go.Scatter(
            x=monthly_rev['month'],
            y=monthly_rev['amount'],
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#1f77b4')
        ),
        row=1, col=1
    )
    
    # 2. 右上：Top 10 商品營收 (bar)
    top10_products = df.groupby('product_name')['amount'].sum().nlargest(10).reset_index()
    fig.add_trace(
        go.Bar(
            y=top10_products['product_name'],
            x=top10_products['amount'],
            orientation='h',
            name='Product Revenue',
            marker=dict(color='#ff7f0e')
        ),
        row=1, col=2
    )
    
    # 3. 左下：各地區營收 (bar)
    region_rev = df.groupby('region')['amount'].sum().reset_index()
    fig.add_trace(
        go.Bar(
            x=region_rev['region'],
            y=region_rev['amount'],
            name='Region Revenue',
            marker=dict(color='#2ca02c')
        ),
        row=2, col=1
    )
    
    # 4. 右下：類別營收佔比 (pie)
    category_rev = df.groupby('category')['amount'].sum().reset_index()
    fig.add_trace(
        go.Pie(
            labels=category_rev['category'],
            values=category_rev['amount'],
            name='Category Share'
        ),
        row=2, col=2
    )
    
    # 更新軸標籤
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
    
    fig.update_xaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_yaxes(title_text="Product", row=1, col=2)
    
    fig.update_xaxes(title_text="Region", row=2, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=2, col=1)
    
    # 設定整體標題
    fig.update_layout(
        title_text="E-Commerce Dashboard",
        height=900,
        showlegend=True
    )
    
    return fig