"""
Visualization components for the dashboard.
"""

from typing import Dict, Any, List, Optional
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DashboardVisualizer:
    """
    Generate interactive visualizations for analysis results.
    """
    
    def __init__(self, theme: str = "light"):
        """Initialize visualizer with theme."""
        self.theme = theme
        self._setup_theme()
        
    def _setup_theme(self):
        """Setup theme colors and styles."""
        self.colors = {
            "light": {
                "primary": "#2563eb",
                "secondary": "#7c3aed",
                "success": "#059669",
                "warning": "#d97706",
                "error": "#dc2626",
                "background": "#ffffff",
                "text": "#1f2937"
            },
            "dark": {
                "primary": "#3b82f6",
                "secondary": "#8b5cf6",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444",
                "background": "#1f2937",
                "text": "#f3f4f6"
            }
        }[self.theme]

    def create_tech_stack_visualization(
        self,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create technology stack visualization.
        
        Args:
            analysis_result: Analysis result from TechStackAnalyzer
            
        Returns:
            Dictionary containing Plotly figure data
        """
        # Create sunburst chart for tech stack
        tech_data = self._prepare_tech_data(analysis_result)
        
        fig = go.Figure(go.Sunburst(
            ids=tech_data["ids"],
            labels=tech_data["labels"],
            parents=tech_data["parents"],
            values=tech_data["values"],
            branchvalues="total",
            marker=dict(
                colors=tech_data["colors"]
            ),
            hovertemplate="<b>%{label}</b><br>Score: %{value:.2%}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Technology Stack Analysis",
            width=600,
            height=600,
            paper_bgcolor=self.colors["background"],
            plot_bgcolor=self.colors["background"],
            font=dict(
                color=self.colors["text"]
            )
        )
        
        return fig.to_dict()

    def create_analysis_dashboard(
        self,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive analysis dashboard.
        
        Args:
            results: Combined analysis results
            
        Returns:
            Dictionary containing multiple Plotly figures
        """
        # Create subplot layout
        fig = make_subplots(
            rows=2,
            cols=2,
            specs=[
                [{"type": "domain"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "heatmap"}]
            ],
            subplot_titles=(
                "Technology Distribution",
                "Framework Usage",
                "Performance Metrics",
                "Dependency Matrix"
            )
        )
        
        # Add technology distribution (pie chart)
        tech_data = results.get("technologies", {})
        fig.add_trace(
            go.Pie(
                labels=list(tech_data.keys()),
                values=list(tech_data.values()),
                name="Technologies"
            ),
            row=1, col=1
        )
        
        # Add framework usage (bar chart)
        framework_data = results.get("frameworks", {})
        fig.add_trace(
            go.Bar(
                x=list(framework_data.keys()),
                y=list(framework_data.values()),
                name="Frameworks"
            ),
            row=1, col=2
        )
        
        # Add performance metrics (line chart)
        if "performance" in results:
            perf_data = results["performance"]
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(perf_data))),
                    y=list(perf_data.values()),
                    mode="lines+markers",
                    name="Performance"
                ),
                row=2, col=1
            )
            
        # Add dependency matrix (heatmap)
        if "dependencies" in results:
            dep_data = results["dependencies"]
            fig.add_trace(
                go.Heatmap(
                    z=dep_data["matrix"],
                    x=dep_data["labels"],
                    y=dep_data["labels"],
                    colorscale="Viridis"
                ),
                row=2, col=2
            )
            
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            paper_bgcolor=self.colors["background"],
            plot_bgcolor=self.colors["background"],
            font=dict(
                color=self.colors["text"]
            )
        )
        
        return fig.to_dict()

    def create_metrics_visualization(
        self,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create metrics visualization.
        
        Args:
            metrics: Analysis metrics
            
        Returns:
            Dictionary containing Plotly figure data
        """
        # Create gauge charts for key metrics
        fig = make_subplots(
            rows=1,
            cols=3,
            specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Add security score
        if "security_score" in metrics:
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=metrics["security_score"] * 100,
                    title={"text": "Security Score"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": self.colors["primary"]},
                        "steps": [
                            {"range": [0, 50], "color": self.colors["error"]},
                            {"range": [50, 75], "color": self.colors["warning"]},
                            {"range": [75, 100], "color": self.colors["success"]}
                        ]
                    }
                ),
                row=1, col=1
            )
            
        # Add performance score
        if "performance_score" in metrics:
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=metrics["performance_score"] * 100,
                    title={"text": "Performance Score"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": self.colors["secondary"]},
                        "steps": [
                            {"range": [0, 50], "color": self.colors["error"]},
                            {"range": [50, 75], "color": self.colors["warning"]},
                            {"range": [75, 100], "color": self.colors["success"]}
                        ]
                    }
                ),
                row=1, col=2
            )
            
        # Add code quality score
        if "quality_score" in metrics:
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=metrics["quality_score"] * 100,
                    title={"text": "Code Quality"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": self.colors["success"]},
                        "steps": [
                            {"range": [0, 50], "color": self.colors["error"]},
                            {"range": [50, 75], "color": self.colors["warning"]},
                            {"range": [75, 100], "color": self.colors["success"]}
                        ]
                    }
                ),
                row=1, col=3
            )
            
        # Update layout
        fig.update_layout(
            height=400,
            paper_bgcolor=self.colors["background"],
            plot_bgcolor=self.colors["background"],
            font=dict(
                color=self.colors["text"]
            )
        )
        
        return fig.to_dict()

    def _prepare_tech_data(
        self,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, List[Any]]:
        """Prepare technology data for visualization."""
        ids = []
        labels = []
        parents = []
        values = []
        colors = []
        
        # Add root
        ids.append("root")
        labels.append("Technologies")
        parents.append("")
        values.append(1.0)
        colors.append(self.colors["primary"])
        
        # Add technologies
        for tech, score in analysis_result["technologies"].items():
            ids.append(f"tech_{tech}")
            labels.append(tech)
            parents.append("root")
            values.append(score)
            colors.append(self.colors["secondary"])
            
            # Add frameworks for each technology
            if tech in analysis_result["frameworks"]:
                for fw, fw_score in analysis_result["frameworks"][tech].items():
                    ids.append(f"fw_{tech}_{fw}")
                    labels.append(fw)
                    parents.append(f"tech_{tech}")
                    values.append(fw_score * score)  # Adjust score relative to parent
                    colors.append(self.colors["success"])
                    
        return {
            "ids": ids,
            "labels": labels,
            "parents": parents,
            "values": values,
            "colors": colors
        }