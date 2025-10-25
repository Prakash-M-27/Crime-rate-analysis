import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class CrimeAnalysisSystem:
    """Main class for crime rate analysis with CSV data"""
    
    def __init__(self, csv_file='crime_data.csv'):
        self.csv_file = csv_file
        self.df = None
        self.load_data()
    
    def create_sample_csv(self):
        """Create a sample CSV file if it doesn't exist"""
        sample_data = {
            'State': ['Uttar Pradesh', 'Maharashtra', 'Delhi', 'Madhya Pradesh', 
                     'Rajasthan', 'Kerala', 'Tamil Nadu', 'Karnataka', 'Gujarat',
                     'West Bengal', 'Bihar', 'Odisha', 'Haryana', 'Punjab', 'Assam',
                     'Jharkhand', 'Chhattisgarh', 'Telangana', 'Himachal Pradesh', 'Uttarakhand'],
            'Murder': [2500, 1800, 450, 2100, 1500, 250, 900, 800, 600, 
                      1200, 2000, 800, 600, 400, 500, 700, 650, 550, 150, 200],
            'Rape': [3200, 2400, 1200, 2800, 2200, 800, 1500, 1300, 900,
                    1800, 2500, 1200, 1100, 700, 900, 950, 850, 750, 300, 350],
            'Kidnapping': [4500, 3200, 2800, 3500, 2800, 1200, 2200, 2000, 1800,
                          2500, 3800, 1800, 2200, 1500, 1400, 1600, 1500, 1300, 500, 600],
            'Robbery': [1200, 1500, 900, 800, 600, 300, 700, 800, 500,
                       600, 700, 400, 500, 400, 300, 450, 400, 350, 150, 200],
            'Theft': [15000, 18000, 12000, 13000, 11000, 8000, 14000, 13500, 10000,
                     12000, 9000, 7000, 9000, 8500, 6000, 7500, 7000, 8000, 3000, 3500],
            'Riots': [800, 600, 400, 700, 500, 200, 400, 350, 300,
                     900, 1200, 500, 400, 300, 600, 450, 400, 300, 100, 150],
            'Population_Lakhs': [2000, 1140, 190, 730, 685, 345, 724, 614, 605,
                                913, 1040, 420, 254, 277, 312, 330, 256, 354, 69, 101]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(self.csv_file, index=False)
        print(f"✓ Created sample CSV file: {self.csv_file}")
        return df
    
    def load_data(self):
        """Load crime data from CSV file"""
        try:
            if not os.path.exists(self.csv_file):
                print(f"⚠️  CSV file '{self.csv_file}' not found. Creating sample data...")
                self.df = self.create_sample_csv()
            else:
                self.df = pd.read_csv(self.csv_file)
                print(f"✓ Loaded data from {self.csv_file} successfully!")
            
            # Calculate total crimes and crime rate
            self.df['Total_Crimes'] = (self.df['Murder'] + self.df['Rape'] + 
                                       self.df['Kidnapping'] + self.df['Robbery'] + 
                                       self.df['Theft'] + self.df['Riots'])
            
            self.df['Crime_Rate'] = (self.df['Total_Crimes'] / 
                                    (self.df['Population_Lakhs'] * 100000)) * 100000
            
            print(f"✓ Processed data for {len(self.df)} states")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def display_data(self):
        """Display crime statistics"""
        print("\n╔════════════════════════════════════════════════════════════════════════╗")
        print("║                    STATE-WISE CRIME STATISTICS                         ║")
        print("╚════════════════════════════════════════════════════════════════════════╝\n")
        
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)
        
        print(self.df.to_string(index=False))
        print("\nNote: Crime Rate = Crimes per 100,000 population")
    
    def plot_crime_rate_by_state(self):
        """Plot crime rate comparison by state"""
        plt.figure(figsize=(14, 8))
        
        # Sort by crime rate
        df_sorted = self.df.sort_values('Crime_Rate', ascending=True)
        
        # Create color map (red for high, green for low)
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_sorted)))
        
        plt.barh(df_sorted['State'], df_sorted['Crime_Rate'], color=colors)
        plt.xlabel('Crime Rate (per 100,000 population)', fontsize=12, fontweight='bold')
        plt.ylabel('State', fontsize=12, fontweight='bold')
        plt.title('Crime Rate Comparison Across States (SDG 16)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.grid(axis='x', alpha=0.3)
        
        # Add average line
        avg_rate = self.df['Crime_Rate'].mean()
        plt.axvline(avg_rate, color='blue', linestyle='--', linewidth=2, 
                   label=f'Average: {avg_rate:.2f}')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('crime_rate_by_state.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: crime_rate_by_state.png")
        plt.show()
    
    def plot_crime_categories(self):
        """Plot crime distribution by category"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Pie chart for overall crime distribution
        crime_totals = {
            'Murder': self.df['Murder'].sum(),
            'Rape': self.df['Rape'].sum(),
            'Kidnapping': self.df['Kidnapping'].sum(),
            'Robbery': self.df['Robbery'].sum(),
            'Theft': self.df['Theft'].sum(),
            'Riots': self.df['Riots'].sum()
        }
        
        colors_pie = ['#ff6b6b', '#ee5a6f', '#c44569', '#4a69bd', '#60a3bc', '#f8b500']
        axes[0].pie(crime_totals.values(), labels=crime_totals.keys(), autopct='%1.1f%%',
                   startangle=90, colors=colors_pie, textprops={'fontsize': 11})
        axes[0].set_title('National Crime Distribution by Category', 
                         fontsize=13, fontweight='bold', pad=15)
        
        # Bar chart for category totals
        categories = list(crime_totals.keys())
        values = list(crime_totals.values())
        
        bars = axes[1].bar(categories, values, color=colors_pie, edgecolor='black', linewidth=1.2)
        axes[1].set_xlabel('Crime Category', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Total Cases', fontsize=12, fontweight='bold')
        axes[1].set_title('Total Cases by Crime Category', fontsize=13, fontweight='bold', pad=15)
        axes[1].grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}',
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('crime_categories.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: crime_categories.png")
        plt.show()
    
    def plot_top_bottom_states(self):
        """Plot top 10 high crime and bottom 10 low crime states"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Top 10 highest crime rate states
        top_10 = self.df.nlargest(10, 'Crime_Rate').sort_values('Crime_Rate')
        axes[0].barh(top_10['State'], top_10['Crime_Rate'], color='#e74c3c')
        axes[0].set_xlabel('Crime Rate', fontsize=11, fontweight='bold')
        axes[0].set_title('Top 10 High Crime Rate States', fontsize=13, fontweight='bold', pad=15)
        axes[0].grid(axis='x', alpha=0.3)
        
        # Bottom 10 lowest crime rate states
        bottom_10 = self.df.nsmallest(10, 'Crime_Rate').sort_values('Crime_Rate', ascending=False)
        axes[1].barh(bottom_10['State'], bottom_10['Crime_Rate'], color='#27ae60')
        axes[1].set_xlabel('Crime Rate', fontsize=11, fontweight='bold')
        axes[1].set_title('Top 10 Safest States (Lowest Crime Rate)', 
                         fontsize=13, fontweight='bold', pad=15)
        axes[1].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('top_bottom_states.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: top_bottom_states.png")
        plt.show()
    
    def plot_heatmap(self):
        """Create heatmap of crime categories by state"""
        plt.figure(figsize=(12, 10))
        
        # Select top 15 states by total crimes
        top_states = self.df.nlargest(15, 'Total_Crimes')
        
        # Create data for heatmap
        heatmap_data = top_states[['State', 'Murder', 'Rape', 'Kidnapping', 
                                   'Robbery', 'Theft', 'Riots']].set_index('State')
        
        # Normalize data for better visualization
        heatmap_normalized = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())
        
        sns.heatmap(heatmap_normalized, annot=True, fmt='.2f', cmap='YlOrRd', 
                   linewidths=0.5, cbar_kws={'label': 'Normalized Crime Intensity'})
        plt.title('Crime Category Intensity Heatmap (Top 15 States)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Crime Category', fontsize=12, fontweight='bold')
        plt.ylabel('State', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('crime_heatmap.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: crime_heatmap.png")
        plt.show()
    
    def plot_population_vs_crime(self):
        """Scatter plot: Population vs Total Crimes"""
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot
        scatter = plt.scatter(self.df['Population_Lakhs'], self.df['Total_Crimes'],
                            c=self.df['Crime_Rate'], s=200, alpha=0.6, 
                            cmap='RdYlGn_r', edgecolors='black', linewidth=1.5)
        
        # Add state labels for top 10 crime states
        top_10_crime = self.df.nlargest(10, 'Total_Crimes')
        for idx, row in top_10_crime.iterrows():
            plt.annotate(row['State'], 
                        (row['Population_Lakhs'], row['Total_Crimes']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, alpha=0.8)
        
        plt.colorbar(scatter, label='Crime Rate (per 100,000 pop.)')
        plt.xlabel('Population (in Lakhs)', fontsize=12, fontweight='bold')
        plt.ylabel('Total Crimes', fontsize=12, fontweight='bold')
        plt.title('Population vs Total Crimes (Bubble size: Crime Rate)', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('population_vs_crime.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: population_vs_crime.png")
        plt.show()
    
    def plot_statistical_summary(self):
        """Create statistical summary dashboard"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Crime Rate Distribution
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.hist(self.df['Crime_Rate'], bins=15, color='#3498db', edgecolor='black', alpha=0.7)
        ax1.axvline(self.df['Crime_Rate'].mean(), color='red', linestyle='--', 
                   linewidth=2, label=f"Mean: {self.df['Crime_Rate'].mean():.2f}")
        ax1.axvline(self.df['Crime_Rate'].median(), color='green', linestyle='--', 
                   linewidth=2, label=f"Median: {self.df['Crime_Rate'].median():.2f}")
        ax1.set_xlabel('Crime Rate', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax1.set_title('Crime Rate Distribution', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # 2. Statistical Summary Box
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.axis('off')
        stats_text = f"""
        📊 STATISTICAL SUMMARY
        ━━━━━━━━━━━━━━━━━━━━━
        Total States: {len(self.df)}
        
        Total Crimes: {self.df['Total_Crimes'].sum():,}
        
        Crime Rate Stats:
        • Mean: {self.df['Crime_Rate'].mean():.2f}
        • Median: {self.df['Crime_Rate'].median():.2f}
        • Std Dev: {self.df['Crime_Rate'].std():.2f}
        • Min: {self.df['Crime_Rate'].min():.2f}
        • Max: {self.df['Crime_Rate'].max():.2f}
        
        Highest Crime State:
        {self.df.loc[self.df['Crime_Rate'].idxmax(), 'State']}
        
        Safest State:
        {self.df.loc[self.df['Crime_Rate'].idxmin(), 'State']}
        """
        ax2.text(0.1, 0.5, stats_text, fontsize=10, family='monospace',
                verticalalignment='center')
        
        # 3. Box plot for crime categories
        ax3 = fig.add_subplot(gs[1, :])
        crime_cols = ['Murder', 'Rape', 'Kidnapping', 'Robbery', 'Theft', 'Riots']
        data_for_box = [self.df[col] for col in crime_cols]
        bp = ax3.boxplot(data_for_box, labels=crime_cols, patch_artist=True)
        
        colors_box = ['#ff6b6b', '#ee5a6f', '#c44569', '#4a69bd', '#60a3bc', '#f8b500']
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax3.set_ylabel('Number of Cases', fontsize=11, fontweight='bold')
        ax3.set_title('Crime Category Distribution (Box Plot)', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Top 5 crime categories by state
        ax4 = fig.add_subplot(gs[2, :])
        top_5 = self.df.nlargest(5, 'Crime_Rate')
        x = np.arange(len(top_5))
        width = 0.15
        
        for i, col in enumerate(crime_cols):
            ax4.bar(x + i*width, top_5[col], width, label=col, alpha=0.8)
        
        ax4.set_xlabel('State', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Number of Cases', fontsize=11, fontweight='bold')
        ax4.set_title('Crime Distribution in Top 5 High-Crime States', 
                     fontsize=12, fontweight='bold')
        ax4.set_xticks(x + width * 2.5)
        ax4.set_xticklabels(top_5['State'], rotation=45, ha='right')
        ax4.legend(loc='upper right', ncol=3)
        ax4.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Crime Analysis Statistical Dashboard (SDG 16)', 
                    fontsize=16, fontweight='bold', y=0.995)
        plt.savefig('statistical_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: statistical_dashboard.png")
        plt.show()
    
    def generate_all_visualizations(self):
        """Generate all visualizations at once"""
        print("\n" + "="*60)
        print("Generating All Visualizations...")
        print("="*60 + "\n")
        
        self.plot_crime_rate_by_state()
        self.plot_crime_categories()
        self.plot_top_bottom_states()
        self.plot_heatmap()
        self.plot_population_vs_crime()
        self.plot_statistical_summary()
        
        print("\n" + "="*60)
        print("✅ All visualizations generated successfully!")
        print("="*60)
    
    def display_menu(self):
        """Display interactive menu"""
        print("\n═══════════════ MENU ═══════════════")
        print("1. Display All State Data")
        print("2. Crime Rate Comparison Chart")
        print("3. Crime Categories Distribution")
        print("4. Top & Bottom States Comparison")
        print("5. Crime Heatmap")
        print("6. Population vs Crime Analysis")
        print("7. Statistical Dashboard")
        print("8. Generate ALL Visualizations")
        print("0. Exit")
        print("════════════════════════════════════")
    
    def run(self):
        """Main program loop"""
        print("╔════════════════════════════════════════════════════════╗")
        print("║    CRIME RATE ANALYSIS - STATE-WISE (SDG 16)          ║")
        print("║    Peace, Justice & Strong Institutions               ║")
        print("║    With CSV Data & Graphical Visualizations           ║")
        print("╚════════════════════════════════════════════════════════╝")
        
        while True:
            self.display_menu()
            try:
                choice = input("Enter your choice: ").strip()
                
                if choice == '1':
                    self.display_data()
                elif choice == '2':
                    self.plot_crime_rate_by_state()
                elif choice == '3':
                    self.plot_crime_categories()
                elif choice == '4':
                    self.plot_top_bottom_states()
                elif choice == '5':
                    self.plot_heatmap()
                elif choice == '6':
                    self.plot_population_vs_crime()
                elif choice == '7':
                    self.plot_statistical_summary()
                elif choice == '8':
                    self.generate_all_visualizations()
                elif choice == '0':
                    print("\n✅ Thank you for using Crime Analysis System!")
                    print("Supporting SDG 16 - Peace, Justice & Strong Institutions")
                    break
                else:
                    print("\n❌ Invalid choice! Please try again.")
            except Exception as e:
                print(f"\n❌ Error: {e}")

# Main execution
if __name__ == "__main__":
    # Set style for better-looking plots
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    system = CrimeAnalysisSystem('crime_data.csv')
    system.run()