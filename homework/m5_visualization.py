"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(8, 4))
    # 計算訂單數最準確的方式是 countplot
    sns.countplot(data=df, x='category', palette='viridis', ax=ax)
    ax.set_title("Order Count by Category")
    return fig


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    df = _load_data()
    # 建立畫布與座標軸
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # 畫出直方圖，指定 bins=20
    sns.histplot(data=df, x='amount', bins=20, ax=ax, color='skyblue', kde=True)
    
    ax.set_title("Distribution of Order Amounts")
    return fig


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    df = _load_data()
    plt.figure(figsize=(8, 4))
    fig = sns.barplot(data=df, x='region', y='amount', palette='viridis', hue='region', legend=False)
    plt.title('This is title', fontweight='bold')
    plt.xlabel('This is xlabel')
    plt.ylabel('This is ylabel')
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    # TODO: 你的程式碼
    df = _load_data()
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    trend = df.groupby(['month', 'region'])['amount'].sum().reset_index()
    
    trend = trend[trend['region'].isin(['North', 'South'])]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=trend, x='month', y='amount', hue='region', marker='o', ax=ax)
    plt.xticks(rotation=45)
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x='vip_level', y='amount', palette='Set2', ax=ax)
    return fig


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    sns.scatterplot(data=df, x='unit_price', y='amount', alpha=0.6, ax=ax)
    
    ax.set_title("Unit Price vs. Total Amount")
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    """
    針對指定類別，畫 2×2 的 subplot dashboard：
    1. 左上：該類別月營收趨勢 (折線圖)
    2. 右上：該類別各地區營收 (長條圖)
    3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    4. 右下：該類別訂單金額分佈 (直方圖)

    回傳 matplotlib Figure 物件
    提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    """
    # TODO: 你的程式碼
    df = _load_data()
    cat_df = df[df['category'] == category].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"Dashboard: {category}", fontsize=20, fontweight='bold')

    # 1. 左上：月營收趨勢
    cat_df['month'] = cat_df['order_date'].dt.to_period('M').astype(str)
    mon_rev = cat_df.groupby('month')['amount'].sum()
    mon_rev.plot(kind='line', marker='o', ax=axes[0, 0], color='blue')
    axes[0, 0].set_title("Monthly Revenue Trend")

    # 2. 右上：各地區營收
    sns.barplot(data=cat_df, x='region', y='amount', estimator=sum, ax=axes[0, 1])
    axes[0, 1].set_title("Revenue by Region")

    # 3. 左下：Top 5 商品
    top5 = cat_df.groupby('product_name')['amount'].sum().nlargest(5)
    top5.plot(kind='barh', ax=axes[1, 0], color='green')
    axes[1, 0].set_title("Top 5 Products")

    # 4. 右下：金額分佈
    sns.histplot(cat_df['amount'], bins=15, kde=True, ax=axes[1, 1], color='orange')
    axes[1, 1].set_title("Order Amount Distribution")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig