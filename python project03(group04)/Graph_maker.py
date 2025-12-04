# Graph_maker.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import networkx as nx  # NetworkX imported at the top
import tkinter as tk
from tkinter import *
import warnings

warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
def load_goty_csv(path="GOTY(2005-2023).csv"):
    df = pd.read_csv(path)
    # Column for game titles
    title_candidates = [c for c in df.columns if c.lower() in ("name", "game", "title")]
    if title_candidates:
        df = df.rename(columns={title_candidates[0]: "Game"})
    elif "Game" not in df.columns:
        raise ValueError("CSV missing required column: Game/Name/Title")
    # Numeric conversions
    if "Copies sold" in df.columns:
        try:
            df["Copies_sold"] = df["Copies sold"].astype(str).str.replace(",", "").astype(float)
        except:
            df["Copies_sold"] = pd.to_numeric(df["Copies sold"], errors="coerce")
    else:
        df["Copies_sold"] = np.nan
    if "Revenue" in df.columns:
        raw = df["Revenue"].astype(str).str.replace("$", "").str.replace(",", "")
        df["Revenue_clean"] = pd.to_numeric(raw, errors="coerce")
    else:
        df["Revenue_clean"] = np.nan
    if "Ratings" in df.columns:
        df["Ratings_num"] = pd.to_numeric(df["Ratings"], errors="coerce")
    elif "Score" in df.columns:
        df["Ratings_num"] = pd.to_numeric(df["Score"], errors="coerce")
    else:
        df["Ratings_num"] = np.nan
    if "GOTY_Status" not in df.columns:
        df["GOTY_Status"] = "Other"
    else:
        df["GOTY_Status"] = df["GOTY_Status"].fillna("Other")
    if "Genre" not in df.columns:
        df["Genre"] = "Unknown"
    # ADD YEAR if not present (important for predictions)
    if "Year" not in df.columns:
        df["Year"] = 2020  # Default value
    if "Company" not in df.columns:
        df["Company"] = "Unknown"
    df = df.dropna(subset=["Game"]).drop_duplicates(subset=["Game"]).reset_index(drop=True)
    return df
def build_similarity_graph_from_df(df):
    G = nx.Graph()
    # Add nodes
    for _, row in df.iterrows():
        name = row["Game"]
        G.add_node(
            name,
            ratings=row.get("Ratings_num", np.nan),
            copies=row.get("Copies_sold", np.nan),
            revenue=row.get("Revenue_clean", np.nan),
            goty_status=row.get("GOTY_Status", "Nominee"),
            genre=row.get("Genre", "Unknown")
        )
    # We prepare a normalized matrix here
    nodes = list(G.nodes())
    mat = []
    for n in nodes:
        a = G.nodes[n]
        mat.append([
            a.get("ratings", np.nan),
            a.get("copies", np.nan),
            a.get("revenue", np.nan)
        ])
    mat = np.array(mat, float)
    # Minimun and maximum normalization
    with np.errstate(invalid="ignore"):
        mn = np.nanmin(mat, axis=0)
        mx = np.nanmax(mat, axis=0)
        denom = (mx - mn)
        denom[denom == 0] = 1
        norm = (mat - mn) / denom
    # Build edges using inverse Euclidean similarity
    n = len(nodes)
    col_mean = np.nanmean(norm, axis=0)
    for i in range(n):
        for j in range(i + 1, n):
            vi = np.where(np.isnan(norm[i]), col_mean, norm[i])
            vj = np.where(np.isnan(norm[j]), col_mean, norm[j])
            dist = np.linalg.norm(vi - vj)
            sim = 1 / (1 + dist)
            # Filter small similarities
            if sim > 0.05:
                G.add_edge(nodes[i], nodes[j], weight=sim)
    return G
def draw_networkx_winners_analysis(fig, df):
    """ACTUAL NetworkX visualization - clean and meaningful"""
    fig.clf()
    ax = fig.add_subplot(111)
    # Create NetworkX graph
    G = nx.Graph()
    # Get only winners
    winners_df = df[df['GOTY_Status'] == 'Winner'].copy()
    if winners_df.empty:
        ax.text(0.5, 0.5, "No winner data available",
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return
    # Add winner nodes with attributes
    for _, row in winners_df.iterrows():
        G.add_node(row['Game'],
                   rating=row['Ratings_num'],
                   copies=row.get('Copies_sold', 0),
                   genre=row.get('Genre', 'Unknown'),
                   year=row.get('Year', 2020))
    # Connect winners with similar ratings (within 3 points)
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            rating_diff = abs(G.nodes[nodes[i]]['rating'] - G.nodes[nodes[j]]['rating'])
            if rating_diff <= 3:  # Similar ratings
                G.add_edge(nodes[i], nodes[j], weight=1 - (rating_diff / 10))
    # Use circular layout for clean visualization
    pos = nx.circular_layout(G)
    # Size nodes by rating
    node_sizes = [800 + (G.nodes[node]['rating'] - 80) * 30 for node in G.nodes()]
    # Color nodes by rating (higher = hotter color)
    node_colors = [G.nodes[node]['rating'] for node in G.nodes()]
    # Draw NetworkX graph
    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_size=node_sizes,
                           node_color=node_colors,
                           cmap='YlOrRd',
                           edgecolors='black',
                           linewidths=2,
                           alpha=0.9)
    # Draw edges
    if G.number_of_edges() > 0:
        edge_weights = [G[u][v].get('weight', 0.5) * 3 for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, ax=ax,
                               width=edge_weights,
                               alpha=0.4,
                               edge_color='gray',
                               style='solid')
    # Create labels (shorten long names)
    labels = {}
    for node in G.nodes():
        if len(node) > 12:
            labels[node] = node[:10] + '...'
        else:
            labels[node] = node
    nx.draw_networkx_labels(G, pos, labels=labels,
                            ax=ax, font_size=9, font_weight='bold')
    ax.set_title("GOTY Winners Network Analysis\n(Connected by Similar Ratings)",
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    # Add NetworkX statistics
    if G.number_of_nodes() > 0:
        # Calculate NetworkX metrics
        try:
            centrality = nx.degree_centrality(G)
            most_central = max(centrality, key=centrality.get)
            avg_clustering = nx.average_clustering(G)
            stats_text = f"Winners: {G.number_of_nodes()} | Connections: {G.number_of_edges()}\n"
            stats_text += f"Most Connected: {most_central[:15]}...\n"
            stats_text += f"Avg. Clustering: {avg_clustering:.2f}"
            ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.5",
                              facecolor="lightblue", alpha=0.8,
                              edgecolor='blue'))
        except:
            pass
    # Add colorbar for ratings
    sm = plt.cm.ScalarMappable(cmap='YlOrRd',
                               norm=plt.Normalize(vmin=min(node_colors),
                                                  vmax=max(node_colors)))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label('Game Rating', fontsize=10)
    fig.tight_layout()
def draw_prediction_dashboard(fig, df):
    """GOTY prediction dashboard with NetworkX info"""
    fig.clf()
    # Create 2x2 grid
    ax1 = fig.add_subplot(221)  # Winners vs Nominees
    ax2 = fig.add_subplot(222)  # Genre success
    ax3 = fig.add_subplot(223)  # Rating thresholds
    ax4 = fig.add_subplot(224)  # Prediction formula
    fig.suptitle('GOTY Nomination Predictor', fontsize=16, fontweight='bold', y=0.98)
    # 1. Winners vs Nominees scatter
    winners = df[df['GOTY_Status'] == 'Winner']
    nominees = df[df['GOTY_Status'] == 'Nominee']
    others = df[df['GOTY_Status'] == 'Other']
    # Plot nominees
    if not nominees.empty:
        ax1.scatter(nominees['Ratings_num'], nominees.get('Copies_sold', 1),
                    alpha=0.6, s=50, c='blue', label='Nominees')
    # Plot winners
    if not winners.empty:
        ax1.scatter(winners['Ratings_num'], winners.get('Copies_sold', 1),
                    alpha=1.0, s=200, c='gold', marker='*',
                    edgecolors='black', linewidth=2, label='Winners')
    # PLot non-nominees
    if not others.empty:
        ax1.scatter(
            others['Ratings_num'],
            others.get('Copies_sold', 1),
            alpha=0.4,
            s=40,
            c='gray',
            label='Other Games'
        )
    ax1.set_xlabel('Ratings', fontsize=10)
    ax1.set_ylabel('Copies Sold', fontsize=10)
    ax1.set_title('Winners vs Nominees', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    # Add threshold line at 85 rating
    ax1.axvline(x=85, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax1.text(85.5, ax1.get_ylim()[1] * 0.9, '85+ rating\nthreshold',
             fontsize=8, color='red', va='top')
    # ADD NETWORKX INFO to scatter plot
    if not winners.empty:
        # Create simple NetworkX graph of winners for analysis
        G_winners = nx.Graph()
        for _, row in winners.iterrows():
            G_winners.add_node(row['Game'], rating=row['Ratings_num'])
        # Calculate NetworkX metric
        if G_winners.number_of_nodes() > 1:
            # Connect winners with close ratings
            nodes = list(G_winners.nodes())
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    if abs(G_winners.nodes[nodes[i]]['rating'] -
                           G_winners.nodes[nodes[j]]['rating']) <= 5:
                        G_winners.add_edge(nodes[i], nodes[j])
            if G_winners.number_of_edges() > 0:
                # Use NetworkX to find average path length
                try:
                    if nx.is_connected(G_winners):
                        avg_path = nx.average_shortest_path_length(G_winners)
                        ax1.text(0.02, 0.98,
                                 f"Winner Network:\nAvg. Connections: {avg_path:.1f}",
                                 transform=ax1.transAxes,
                                 fontsize=9,
                                 bbox=dict(boxstyle="round,pad=0.3",
                                           facecolor="yellow", alpha=0.3),
                                 va='top')
                except:
                    pass
    # 2. Genre success (top 6 genres)
    top_genres = df['Genre'].value_counts().head(6).index
    genre_success = []
    for genre in top_genres:
        genre_df = df[df['Genre'] == genre]
        if len(genre_df) > 0:
            win_rate = (genre_df['GOTY_Status'] == 'Winner').mean() * 100
            genre_success.append(win_rate)
        else:
            genre_success.append(0)
    bars = ax2.bar(range(len(top_genres)), genre_success,
                   color=plt.cm.Set3(np.arange(len(top_genres)) / len(top_genres)))
    ax2.set_xticks(range(len(top_genres)))
    ax2.set_xticklabels(top_genres, rotation=45, ha='right', fontsize=9)
    ax2.set_ylabel('Win Rate (%)', fontsize=10)
    ax2.set_title('Win Rate by Genre', fontsize=12)
    ax2.set_ylim(0, 100)
    # Add value labels
    for bar, rate in zip(bars, genre_success):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 2,
                 f'{rate:.1f}%', ha='center', va='bottom', fontsize=8)
    # 3. Rating distribution
    rating_bins = np.arange(70, 101, 5)
    winner_counts = []
    nominee_counts = []
    other_counts = []
    for i in range(len(rating_bins) - 1):
        low, high = rating_bins[i], rating_bins[i + 1]
        bin_df = df[(df['Ratings_num'] >= low) & (df['Ratings_num'] < high)]
        winner_counts.append((bin_df['GOTY_Status'] == 'Winner').sum())
        nominee_counts.append((bin_df['GOTY_Status'] == 'Nominee').sum())
        other_counts.append((bin_df['GOTY_Status'] == 'Other').sum())
    x_pos = rating_bins[:-1] + 2.5
    width = 3.5
    ax3.bar(x_pos - width / 2, nominee_counts, width, label='Nominees',
            alpha=0.7, color='blue')
    ax3.bar(x_pos + width / 2, winner_counts, width, label='Winners',
            alpha=0.9, color='gold')
    ax3.bar(x_pos + width, other_counts, width,
            label='Other', alpha=0.7, color='gray')
    ax3.set_xlabel('Rating Range', fontsize=10)
    ax3.set_ylabel('Number of Games', fontsize=10)
    ax3.set_title('Rating Distribution', fontsize=12)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    # 4. Prediction criteria
    ax4.axis('off')
    criteria_text = "PREDICTION CRITERIA\n\n"
    criteria_text += "High Chance of Nomination:\n"
    criteria_text += "• Rating ≥ 85\n"
    criteria_text += "• Sales ≥ 2M copies\n"
    criteria_text += "• Genre: RPG or Action\n"
    criteria_text += "• Release: Q4 (Oct-Dec)\n\n"
    criteria_text += "Winning Factors:\n"
    criteria_text += "• Rating ≥ 90\n"
    criteria_text += "• High critic acclaim\n"
    criteria_text += "• Cultural impact\n"
    criteria_text += "• Genre innovation"
    ax4.text(0.1, 0.5, criteria_text, fontsize=11,
             bbox=dict(facecolor='#f8f9fa', edgecolor='#ddd',
                       boxstyle='round,pad=1'), va='center')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
def draw_yearly_analysis(fig, df):
    """Year-by-year analysis"""
    fig.clf()
    if 'Year' not in df.columns:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "No Year data available",
                ha='center', va='center', fontsize=14)
        ax.axis('off')
        return
    # Group by year here
    yearly_stats = df.groupby('Year').agg({
        'Ratings_num': 'mean',
        'GOTY_Status': lambda x: (x == 'Winner').sum()
    }).reset_index()
    # And create plot
    ax = fig.add_subplot(111)
    # Line for average game ratings
    line1 = ax.plot(yearly_stats['Year'], yearly_stats['Ratings_num'],
                    marker='o', linewidth=2, markersize=6,
                    color='green', label='Avg Rating')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Rating', fontsize=12, color='green')
    ax.tick_params(axis='y', labelcolor='green')
    ax.set_ylim(70, 100)
    # Bars for number of winners
    ax2 = ax.twinx()
    bars = ax2.bar(yearly_stats['Year'], yearly_stats['GOTY_Status'],
                   alpha=0.3, color='red', label='Winners')
    ax2.set_ylabel('Number of Winners', fontsize=12, color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, yearly_stats['GOTY_Status'].max() * 1.2)
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
                     str(int(height)), ha='center', va='bottom',
                     fontsize=9, color='red')
    ax.set_title('Yearly Trends: Ratings & Winners', fontsize=14, fontweight='bold')
    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
def draw_genre_company_chart(fig, df):
    """Genre and company analysis"""
    fig.clf()
    # Create subplots
    ax1 = fig.add_subplot(121)  # Genre nominations
    ax2 = fig.add_subplot(122)  # Company performance
    fig.suptitle('Genre & Company Analysis', fontsize=16, fontweight='bold', y=0.98)
    # 1. Genre nominations (top 8)
    genre_counts = df['Genre'].value_counts().head(8)
    bars1 = ax1.barh(range(len(genre_counts)), genre_counts.values,
                     color=plt.cm.viridis(np.linspace(0.2, 0.8, len(genre_counts))))
    ax1.set_yticks(range(len(genre_counts)))
    ax1.set_yticklabels(genre_counts.index, fontsize=9)
    ax1.set_xlabel('Number of Games', fontsize=10)
    ax1.set_title('Most Common Genres', fontsize=12)
    ax1.invert_yaxis()  # Highest at top
    # Add count labels
    for i, count in enumerate(genre_counts.values):
        ax1.text(count + 0.5, i, str(count), va='center', fontsize=9)
    # 2. Company performance (if available)
    if 'Company' in df.columns and df['Company'].nunique() > 1:
        # Get companies with at least 2 games
        company_counts = df['Company'].value_counts()
        top_companies = company_counts[company_counts >= 2].head(8).index
        company_stats = []
        for company in top_companies:
            company_df = df[df['Company'] == company]
            nominations = len(company_df)
            wins = (company_df['GOTY_Status'] == 'Winner').sum()
            win_rate = (wins / nominations * 100) if nominations > 0 else 0
            company_stats.append({
                'Company': company[:15] + ('...' if len(company) > 15 else ''),
                'Nominations': nominations,
                'Win Rate': win_rate
            })
        if company_stats:
            company_df = pd.DataFrame(company_stats)
            y_pos = range(len(company_df))
            bars2 = ax2.barh(y_pos, company_df['Win Rate'],
                             color=plt.cm.plasma(np.linspace(0.2, 0.8, len(company_df))))
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(company_df['Company'], fontsize=9)
            ax2.set_xlabel('Win Rate (%)', fontsize=10)
            ax2.set_title('Company Win Rates', fontsize=12)
            ax2.set_xlim(0, 100)
            ax2.invert_yaxis()
            # Add win rate labels
            for i, (_, row) in enumerate(company_df.iterrows()):
                ax2.text(row['Win Rate'] + 2, i,
                         f"{row['Win Rate']:.1f}% ({row['Nominations']} games)",
                         va='center', fontsize=8)
        else:
            ax2.text(0.5, 0.5, "Insufficient company data",
                     ha='center', va='center', transform=ax2.transAxes)
            ax2.axis('off')
    else:
        ax2.text(0.5, 0.5, "No company data available",
                 ha='center', va='center', transform=ax2.transAxes)
        ax2.axis('off')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
class GraphWindow(tk.Toplevel):
    def __init__(self, master=None, G=None, df=None):
        super().__init__(master)
        self.title("GOTY Analysis Dashboard")
        self.geometry("1200x800")
        self.configure(bg="#1a1a2e")
        self.G = G
        self.df = df
        # If df not provided but G is, extract df from G
        if df is None and G is not None:
            self.df = self._graph_to_dataframe(G)
        # Header
        header = Frame(self, bg="#2d2d44", height=60)
        header.pack(fill="x", padx=10, pady=5)
        Label(header, text="🎮 GOTY Prediction Analytics",
              font=("Arial", 16, "bold"), bg="#2d2d44", fg="white").pack(side="left", padx=20, pady=10)
        # Main content
        main_frame = Frame(self, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        # Left panel - controls
        left_panel = Frame(main_frame, bg="#2d2d44", width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        Label(left_panel, text="Select View:", font=("Arial", 12, "bold"),
              bg="#2d2d44", fg="white").pack(pady=15)
        # View buttons - ADDED NETWORKX VIEW
        self.view_var = tk.StringVar(value="dashboard")
        views = [
            ("📊 Prediction Dashboard", "dashboard"),
            ("📈 Yearly Trends", "yearly"),
            ("🎮 Genre & Company", "genre_company"),
            ("🌐 Winners Network", "networkx"),  # NEW: NetworkX view
        ]
        for text, value in views:
            btn = Radiobutton(
                left_panel, text=text, value=value,
                variable=self.view_var, command=self.redraw,
                bg="#2d2d44", fg="white", selectcolor="#444466",
                activebackground="#3d3d55", font=("Arial", 10),
                indicatoron=0, width=20, height=2
            )
            btn.pack(pady=5, padx=10)
        # NetworkX info box
        nx_info = Frame(left_panel, bg="#2d2d44")
        nx_info.pack(side="bottom", pady=20, fill="x", padx=0)
        Label(nx_info, text="NetworkX Features:", font=("Arial", 10, "bold"),
              bg="#2d2d44", fg="lightgreen").pack(anchor="w")
        features = [
            "• Graph analysis",
            "• Centrality metrics",
            "• Winner connections",
            "• Similarity networks"
        ]
        for feature in features:
            Label(nx_info, text=feature, font=("Arial", 8),
                  bg="#2d2d44", fg="lightgray", justify="left").pack(anchor="w", padx=5)
        # Right panel - graph display
        self.right_panel = Frame(main_frame, bg="#1a1a2e")
        self.right_panel.pack(side="right", fill="both", expand=True)
        # Create figure
        self.fig = plt.Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        # Info label
        self.info_label = Label(self, text="Ready", bg="#1a1a2e", fg="lightgreen",
                                font=("Arial", 9))
        self.info_label.pack(side="bottom", pady=5)
        # Initial draw
        self.redraw()
    def _graph_to_dataframe(self, G):
        """Convert graph to dataframe for analysis"""
        games = []
        for node in G.nodes():
            games.append({
                'Game': node,
                'Ratings_num': G.nodes[node].get('ratings', np.nan),
                'Copies_sold': G.nodes[node].get('copies', np.nan),
                'Revenue_clean': G.nodes[node].get('revenue', np.nan),
                'GOTY_Status': G.nodes[node].get('goty_status', 'Nominee'),
                'Genre': G.nodes[node].get('genre', 'Unknown'),
                'Year': 2020  # Default
            })
        return pd.DataFrame(games)
    def redraw(self):
        if self.df is None or self.df.empty:
            self._show_error("No data available")
            return
        view = self.view_var.get()
        try:
            if view == "dashboard":
                draw_prediction_dashboard(self.fig, self.df)
                self.info_label.config(text="Showing: Prediction dashboard with key factors")
            elif view == "yearly":
                draw_yearly_analysis(self.fig, self.df)
                self.info_label.config(text="Showing: Yearly trends and patterns")
            elif view == "genre_company":
                draw_genre_company_chart(self.fig, self.df)
                self.info_label.config(text="Showing: Genre and company analysis")
            elif view == "networkx":  # NEW: NetworkX view
                draw_networkx_winners_analysis(self.fig, self.df)
                self.info_label.config(text="NetworkX Analysis: Winners connected by similar ratings")
            else:
                self._show_error(f"Unknown view: {view}")
                return
            self.canvas.draw()
        except Exception as e:
            self._show_error(f"Error: {str(e)}")
    def _show_error(self, message):
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, message, ha='center', va='center', fontsize=12)
        ax.axis('off')
        self.canvas.draw()
        self.info_label.config(text="Error displaying graph")