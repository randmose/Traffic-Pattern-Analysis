"""
Congestion Detector Module
Identifies congestion hotspots in the traffic network.
"""

import numpy as np
from typing import List, Dict, Tuple
from .traffic_network import TrafficNetwork


class CongestionDetector:
    """
    Analyzes traffic network to identify congestion hotspots.
    """
    
    def __init__(self, network: TrafficNetwork):
        """
        Initialize the congestion detector.
        
        Args:
            network: TrafficNetwork instance to analyze
        """
        self.network = network
    
    def identify_hotspots(self, threshold: float = 0.5) -> List[Dict]:
        """
        Identify congestion hotspots based on congestion levels.
        
        Args:
            threshold: Congestion level threshold (0.0 to 1.0)
            
        Returns:
            List of dictionaries containing hotspot information
        """
        hotspots = []
        
        for edge in self.network.graph.edges():
            from_node, to_node = edge
            edge_data = self.network.graph[from_node][to_node]
            
            congestion_level = edge_data.get('congestion_level', 0.0)
            
            if congestion_level >= threshold:
                traffic_info = self.network.get_current_traffic(from_node, to_node)
                
                hotspot = {
                    'from': from_node,
                    'to': to_node,
                    'congestion_level': congestion_level,
                    'severity': self._categorize_severity(congestion_level),
                    'distance': edge_data.get('distance', 0),
                    'speed_limit': edge_data.get('speed_limit', 0),
                    'lanes': edge_data.get('lanes', 1),
                    'vehicle_count': traffic_info['vehicle_count'] if traffic_info else 0
                }
                hotspots.append(hotspot)
        
        # Sort by congestion level (highest first)
        hotspots.sort(key=lambda x: x['congestion_level'], reverse=True)
        
        return hotspots
    
    def _categorize_severity(self, congestion_level: float) -> str:
        """
        Categorize congestion severity.
        
        Args:
            congestion_level: Congestion level (0.0 to 1.0)
            
        Returns:
            Severity category string
        """
        if congestion_level >= 0.8:
            return "Critical"
        elif congestion_level >= 0.6:
            return "High"
        elif congestion_level >= 0.4:
            return "Moderate"
        else:
            return "Low"
    
    def get_intersection_congestion(self) -> Dict[str, float]:
        """
        Calculate average congestion level for each intersection.
        
        Returns:
            Dictionary mapping intersection ID to average congestion
        """
        intersection_congestion = {}
        
        for node in self.network.graph.nodes():
            incoming_edges = list(self.network.graph.in_edges(node))
            outgoing_edges = list(self.network.graph.out_edges(node))
            all_edges = incoming_edges + outgoing_edges
            
            if all_edges:
                congestion_levels = []
                for edge in all_edges:
                    edge_data = self.network.graph[edge[0]][edge[1]]
                    congestion_levels.append(edge_data.get('congestion_level', 0.0))
                
                intersection_congestion[node] = np.mean(congestion_levels)
            else:
                intersection_congestion[node] = 0.0
        
        return intersection_congestion
    
    def get_top_congested_intersections(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Get the most congested intersections.
        
        Args:
            top_n: Number of top intersections to return
            
        Returns:
            List of tuples (intersection_id, congestion_level)
        """
        intersection_congestion = self.get_intersection_congestion()
        sorted_intersections = sorted(
            intersection_congestion.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_intersections[:top_n]
    
    def generate_hotspot_report(self, threshold: float = 0.5) -> str:
        """
        Generate a text report of congestion hotspots.
        
        Args:
            threshold: Congestion level threshold
            
        Returns:
            Formatted report string
        """
        hotspots = self.identify_hotspots(threshold)
        
        report = "=" * 60 + "\n"
        report += "TRAFFIC CONGESTION HOTSPOT REPORT\n"
        report += "=" * 60 + "\n\n"
        report += f"Total hotspots identified: {len(hotspots)}\n"
        report += f"Congestion threshold: {threshold:.1%}\n\n"
        
        if hotspots:
            report += "-" * 60 + "\n"
            report += "TOP CONGESTION HOTSPOTS:\n"
            report += "-" * 60 + "\n\n"
            
            for i, hotspot in enumerate(hotspots[:10], 1):
                report += f"{i}. Road: {hotspot['from']} → {hotspot['to']}\n"
                report += f"   Congestion Level: {hotspot['congestion_level']:.1%}\n"
                report += f"   Severity: {hotspot['severity']}\n"
                report += f"   Vehicle Count: {hotspot['vehicle_count']}\n"
                report += f"   Distance: {hotspot['distance']:.2f} km\n"
                report += f"   Speed Limit: {hotspot['speed_limit']} km/h\n"
                report += f"   Lanes: {hotspot['lanes']}\n\n"
        else:
            report += "No congestion hotspots detected above the threshold.\n\n"
        
        # Add intersection analysis
        top_intersections = self.get_top_congested_intersections()
        report += "-" * 60 + "\n"
        report += "MOST CONGESTED INTERSECTIONS:\n"
        report += "-" * 60 + "\n\n"
        
        for i, (intersection, congestion) in enumerate(top_intersections, 1):
            report += f"{i}. {intersection}: {congestion:.1%} average congestion\n"
        
        report += "\n" + "=" * 60 + "\n"
        
        return report
