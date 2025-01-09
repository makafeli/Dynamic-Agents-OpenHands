# Visualization Guide

The OpenHands Dynamic Agents visualization system provides interactive data visualization for analysis results and monitoring.

## Overview

The visualization system uses Plotly for interactive charts and dashboards, providing:
- Technology stack visualization
- Performance metrics
- Security analysis
- Code quality metrics
- Real-time monitoring

## Basic Usage

### Dashboard Setup

```python
from openhands_dynamic_agents.dashboard import Dashboard, DashboardVisualizer

# Initialize
dashboard = Dashboard(port=8080)
visualizer = DashboardVisualizer(theme="light")

# Create visualization
tech_viz = visualizer.create_tech_stack_visualization(results)
dashboard.add_visualization("tech_stack", tech_viz)

# Start dashboard
dashboard.start()
```

### Quick Visualizations

```python
# Technology stack sunburst
viz = visualizer.create_tech_stack_visualization(analysis_results)

# Metrics gauge chart
viz = visualizer.create_metrics_visualization(metrics)

# Full analysis dashboard
viz = visualizer.create_analysis_dashboard(all_results)
```

## Visualization Types

### Technology Stack Visualization

```python
def create_tech_stack_viz(results):
    """Create technology stack sunburst chart."""
    return {
        "data": [{
            "type": "sunburst",
            "labels": ["Python", "Django", "React", "TypeScript"],
            "parents": ["", "Python", "", ""],
            "values": [30, 20, 25, 25],
            "branchvalues": "total"
        }],
        "layout": {
            "title": "Technology Stack Distribution"
        }
    }
```

Example output:
```
                  Technologies
                      [100%]
                    /        \
               Python      JavaScript
               [50%]        [50%]
              /    \        /    \
         Django  Flask   React  Vue.js
         [30%]  [20%]   [30%]  [20%]
```

### Performance Metrics

```python
def create_performance_viz(metrics):
    """Create performance metrics dashboard."""
    return {
        "data": [{
            "type": "indicator",
            "mode": "gauge+number",
            "value": metrics["performance_score"] * 100,
            "title": {"text": "Performance Score"},
            "gauge": {
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 50], "color": "red"},
                    {"range": [50, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "green"}
                ]
            }
        }],
        "layout": {
            "title": "Performance Metrics"
        }
    }
```

### Security Analysis

```python
def create_security_viz(security_results):
    """Create security analysis visualization."""
    return {
        "data": [{
            "type": "scatter",
            "mode": "markers",
            "x": security_results["vulnerability_locations"],
            "y": security_results["severity_scores"],
            "marker": {
                "size": 10,
                "color": security_results["severity_colors"]
            }
        }],
        "layout": {
            "title": "Security Vulnerabilities",
            "xaxis": {"title": "Code Location"},
            "yaxis": {"title": "Severity"}
        }
    }
```

### Real-time Monitoring

```python
class MonitoringDashboard:
    """Real-time monitoring dashboard."""
    
    def __init__(self):
        self.app = Dashboard()
        self.visualizer = DashboardVisualizer()
        
    async def update_metrics(self, metrics):
        """Update real-time metrics."""
        viz = self.visualizer.create_metrics_visualization(metrics)
        await self.app.update_visualization("metrics", viz)
        
    def start(self):
        """Start monitoring dashboard."""
        self.app.start()

# Usage
dashboard = MonitoringDashboard()
dashboard.start()

# Update metrics
await dashboard.update_metrics(new_metrics)
```

## Custom Visualizations

### Creating Custom Visualizations

```python
from openhands_dynamic_agents.dashboard import BaseVisualization

class CustomVisualization(BaseVisualization):
    """Custom visualization type."""
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom visualization."""
        return {
            "data": [{
                "type": "custom_chart",
                "x": data["x_values"],
                "y": data["y_values"]
            }],
            "layout": {
                "title": "Custom Visualization"
            }
        }

# Register custom visualization
dashboard.register_visualization("custom", CustomVisualization())
```

### Extending Existing Visualizations

```python
class EnhancedTechStackViz(TechStackVisualization):
    """Enhanced technology stack visualization."""
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create enhanced visualization."""
        base_viz = super().create(data)
        
        # Add enhancements
        base_viz["data"].append({
            "type": "scatter",
            "mode": "markers",
            "name": "Version Info"
        })
        
        return base_viz
```

## Dashboard Customization

### Themes

```python
# Available themes
themes = {
    "light": {
        "background": "#ffffff",
        "text": "#1f2937",
        "primary": "#3b82f6",
        "secondary": "#8b5cf6"
    },
    "dark": {
        "background": "#1f2937",
        "text": "#f3f4f6",
        "primary": "#60a5fa",
        "secondary": "#a78bfa"
    }
}

# Use theme
visualizer = DashboardVisualizer(theme="dark")
```

### Layout Customization

```python
def customize_layout(viz: Dict[str, Any]) -> Dict[str, Any]:
    """Customize visualization layout."""
    viz["layout"].update({
        "template": "plotly_dark",
        "font": {"family": "Roboto, sans-serif"},
        "showlegend": True,
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02
        }
    })
    return viz
```

### Interactive Features

```python
def add_interactivity(viz: Dict[str, Any]) -> Dict[str, Any]:
    """Add interactive features."""
    viz["layout"]["updatemenus"] = [{
        "buttons": [
            {
                "args": [{"visible": [True, False, False]}],
                "label": "Technology",
                "method": "update"
            },
            {
                "args": [{"visible": [False, True, False]}],
                "label": "Performance",
                "method": "update"
            }
        ]
    }]
    return viz
```

## Best Practices

1. **Performance**
   - Use appropriate chart types
   - Limit data points
   - Enable caching
   - Use streaming for real-time data

2. **Responsiveness**
   - Make visualizations responsive
   - Handle window resizing
   - Support mobile devices

3. **Accessibility**
   - Add proper labels
   - Use color-blind friendly palettes
   - Include text alternatives

4. **Data Updates**
   - Implement efficient update mechanisms
   - Handle data streaming
   - Manage state properly

## Troubleshooting

Common issues and solutions:

1. **Performance Issues**
   - Reduce data points
   - Use appropriate chart types
   - Enable data aggregation

2. **Layout Problems**
   - Check responsive settings
   - Verify theme compatibility
   - Review container sizes

3. **Update Issues**
   - Verify WebSocket connection
   - Check update frequency
   - Review data format