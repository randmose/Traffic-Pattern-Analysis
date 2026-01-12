"""
Visualization Module
Provides visualization capabilities for traffic networks and analysis results.
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Optional, List, Dict
from .traffic_network import TrafficNetwork


class TrafficVisualizer:
    """
    Visualizes traffic networks, congestion hotspots, and optimized routes.
    """
    
    def __init__(self, network: TrafficNetwork):
        """
        Initialize the visualizer.
        
        Args:
            network: TrafficNetwork instance to visualize
        """
        self.network = network
    
    def visualize_network(self, output_file: Optional[str] = None, 
                         show_congestion: bool = True):
        """
        Visualize the entire traffic network.
        
        Args:
            output_file: Path to save the figure (if None, display only)
            show_congestion: Whether to color roads by congestion level
        """
        plt.figure(figsize=(12, 10))
        
        # Get node positions
        pos = {}
        for node in self.network.graph.nodes():
            node_data = self.network.graph.nodes[node]
            pos[node] = (node_data.get('lon', 0), node_data.get('lat', 0))
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.network.graph,
            pos,
            node_color='lightblue',
            node_size=300,
            alpha=0.9
        )
        
        # Draw edges with congestion coloring
        if show_congestion:
            edges = self.network.graph.edges()
            congestion_levels = [
                self.network.graph[u][v].get('congestion_level', 0)
                for u, v in edges
            ]
            
            nx.draw_networkx_edges(
                self.network.graph,
                pos,
                edge_color=congestion_levels,
                edge_cmap=plt.cm.RdYlGn_r,
                edge_vmin=0,
                edge_vmax=1,
                width=2,
                alpha=0.7,
                arrows=True,
                arrowsize=10
            )
            
            # Add colorbar
            sm = plt.cm.ScalarMappable(
                cmap=plt.cm.RdYlGn_r,
                norm=plt.Normalize(vmin=0, vmax=1)
            )
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=plt.gca(), label='Congestion Level')
        else:
            nx.draw_networkx_edges(
                self.network.graph,
                pos,
                width=2,
                alpha=0.5,
                arrows=True,
                arrowsize=10
            )
        
        # Draw labels (only for smaller networks)
        if len(self.network.graph.nodes()) <= 30:
            nx.draw_networkx_labels(
                self.network.graph,
                pos,
                font_size=8,
                font_weight='bold'
            )
        
        plt.title('Traffic Network Visualization', fontsize=16, fontweight='bold')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Network visualization saved to {output_file}")
        
        plt.show()
    
    def visualize_hotspots(self, hotspots: List[Dict], 
                          output_file: Optional[str] = None):
        """
        Visualize congestion hotspots on the network.
        
        Args:
            hotspots: List of hotspot dictionaries from CongestionDetector
            output_file: Path to save the figure (if None, display only)
        """
        plt.figure(figsize=(12, 10))
        
        # Get node positions
        pos = {}
        for node in self.network.graph.nodes():
            node_data = self.network.graph.nodes[node]
            pos[node] = (node_data.get('lon', 0), node_data.get('lat', 0))
        
        # Draw all nodes
        nx.draw_networkx_nodes(
            self.network.graph,
            pos,
            node_color='lightgray',
            node_size=200,
            alpha=0.6
        )
        
        # Draw all edges in light color
        nx.draw_networkx_edges(
            self.network.graph,
            pos,
            edge_color='lightgray',
            width=1,
            alpha=0.3,
            arrows=True,
            arrowsize=10
        )
        
        # Highlight hotspot edges
        hotspot_edges = [(h['from'], h['to']) for h in hotspots]
        hotspot_colors = [h['congestion_level'] for h in hotspots]
        
        nx.draw_networkx_edges(
            self.network.graph,
            pos,
            edgelist=hotspot_edges,
            edge_color=hotspot_colors,
            edge_cmap=plt.cm.Reds,
            edge_vmin=0,
            edge_vmax=1,
            width=4,
            alpha=0.9,
            arrows=True,
            arrowsize=15
        )
        
        # Add colorbar
        sm = plt.cm.ScalarMappable(
            cmap=plt.cm.Reds,
            norm=plt.Normalize(vmin=0, vmax=1)
        )
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=plt.gca(), label='Congestion Level')
        
        # Draw labels for smaller networks
        if len(self.network.graph.nodes()) <= 30:
            nx.draw_networkx_labels(
                self.network.graph,
                pos,
                font_size=8
            )
        
        plt.title(f'Congestion Hotspots ({len(hotspots)} identified)', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Hotspot visualization saved to {output_file}")
        
        plt.show()
    
    def visualize_route(self, route: Dict, output_file: Optional[str] = None):
        """
        Visualize an optimized route on the network.
        
        Args:
            route: Route dictionary from RouteOptimizer
            output_file: Path to save the figure (if None, display only)
        """
        plt.figure(figsize=(12, 10))
        
        # Get node positions
        pos = {}
        for node in self.network.graph.nodes():
            node_data = self.network.graph.nodes[node]
            pos[node] = (node_data.get('lon', 0), node_data.get('lat', 0))
        
        # Draw all nodes in light color
        nx.draw_networkx_nodes(
            self.network.graph,
            pos,
            node_color='lightgray',
            node_size=200,
            alpha=0.6
        )
        
        # Draw all edges in light color
        nx.draw_networkx_edges(
            self.network.graph,
            pos,
            edge_color='lightgray',
            width=1,
            alpha=0.3,
            arrows=True,
            arrowsize=10
        )
        
        # Highlight route path
        path = route['path']
        route_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        
        nx.draw_networkx_edges(
            self.network.graph,
            pos,
            edgelist=route_edges,
            edge_color='blue',
            width=4,
            alpha=0.9,
            arrows=True,
            arrowsize=15
        )
        
        # Highlight start and end nodes
        start_node = route['start']
        end_node = route['end']
        
        nx.draw_networkx_nodes(
            self.network.graph,
            pos,
            nodelist=[start_node],
            node_color='green',
            node_size=500,
            label='Start'
        )
        
        nx.draw_networkx_nodes(
            self.network.graph,
            pos,
            nodelist=[end_node],
            node_color='red',
            node_size=500,
            label='End'
        )
        
        # Draw labels
        if len(self.network.graph.nodes()) <= 30:
            nx.draw_networkx_labels(
                self.network.graph,
                pos,
                font_size=8
            )
        
        # Add route information
        info_text = (
            f"Distance: {route['total_distance']:.2f} km\n"
            f"Time: {route['total_time']*60:.1f} min\n"
            f"Avg Congestion: {route['avg_congestion']:.1%}"
        )
        plt.text(
            0.02, 0.98, info_text,
            transform=plt.gca().transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontsize=10
        )
        
        plt.title(f'Optimized Route: {start_node} → {end_node}',
                 fontsize=16, fontweight='bold')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Route visualization saved to {output_file}")
        
        plt.show()
    
    def visualize_comparison(self, routes: Dict[str, Dict], 
                           output_file: Optional[str] = None):
        """
        Visualize comparison of different route optimization strategies.
        
        Args:
            routes: Dictionary of routes from RouteOptimizer.compare_routes()
            output_file: Path to save the figure (if None, display only)
        """
        # Define route types and their display properties
        route_configs = []
        route_order = ['fastest', 'shortest', 'least_congested']
        route_titles = {
            'fastest': 'Fastest Route',
            'shortest': 'Shortest Route', 
            'least_congested': 'Least Congested'
        }
        route_colors = {
            'fastest': 'blue',
            'shortest': 'green',
            'least_congested': 'orange'
        }
        
        # Build configuration list based on available routes
        for key in route_order:
            if key in routes:
                route_configs.append((key, route_titles.get(key, key), route_colors.get(key, 'gray')))
        
        if not route_configs:
            return
        
        fig, axes = plt.subplots(1, len(route_configs), figsize=(6 * len(route_configs), 6))
        
        # Handle single route case
        if len(route_configs) == 1:
            axes = [axes]
        
        for idx, (route_key, title, color) in enumerate(route_configs):
            ax = axes[idx]
            plt.sca(ax)
            
            route = routes[route_key]
            if route is None:
                ax.text(0.5, 0.5, 'No route found', 
                       ha='center', va='center', fontsize=14)
                ax.set_title(title)
                continue
            
            # Get node positions
            pos = {}
            for node in self.network.graph.nodes():
                node_data = self.network.graph.nodes[node]
                pos[node] = (node_data.get('lon', 0), node_data.get('lat', 0))
            
            # Draw network
            nx.draw_networkx_nodes(
                self.network.graph, pos, node_color='lightgray',
                node_size=100, alpha=0.4, ax=ax
            )
            nx.draw_networkx_edges(
                self.network.graph, pos, edge_color='lightgray',
                width=0.5, alpha=0.2, arrows=False, ax=ax
            )
            
            # Draw route
            path = route['path']
            route_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(
                self.network.graph, pos, edgelist=route_edges,
                edge_color=color, width=3, alpha=0.9, arrows=True, ax=ax
            )
            
            # Highlight start/end
            nx.draw_networkx_nodes(
                self.network.graph, pos, nodelist=[route['start']],
                node_color='green', node_size=200, ax=ax
            )
            nx.draw_networkx_nodes(
                self.network.graph, pos, nodelist=[route['end']],
                node_color='red', node_size=200, ax=ax
            )
            
            # Add info
            info_text = (
                f"Distance: {route['total_distance']:.2f} km\n"
                f"Time: {route['total_time']*60:.1f} min\n"
                f"Congestion: {route['avg_congestion']:.1%}"
            )
            ax.text(
                0.02, 0.98, info_text,
                transform=ax.transAxes,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontsize=8
            )
            
            ax.set_title(title, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"Route comparison saved to {output_file}")
        
        plt.show()
