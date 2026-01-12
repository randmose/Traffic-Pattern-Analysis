"""
Traffic Network Module
Handles the representation of road networks with traffic data.
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional


class TrafficNetwork:
    """
    Represents a traffic network as a graph structure.
    Nodes represent intersections, edges represent roads with traffic data.
    """
    
    def __init__(self, lane_capacity: int = 2000):
        """
        Initialize an empty traffic network.
        
        Args:
            lane_capacity: Vehicle capacity per hour per lane (default: 2000)
        """
        self.graph = nx.DiGraph()
        self.traffic_data = {}
        self.lane_capacity = lane_capacity
    
    def add_intersection(self, intersection_id: str, latitude: float = 0.0, longitude: float = 0.0):
        """
        Add an intersection to the network.
        
        Args:
            intersection_id: Unique identifier for the intersection
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        """
        self.graph.add_node(intersection_id, lat=latitude, lon=longitude)
    
    def add_road(self, from_intersection: str, to_intersection: str, 
                 distance: float, speed_limit: float, lanes: int = 1):
        """
        Add a road segment between two intersections.
        
        Args:
            from_intersection: Starting intersection ID
            to_intersection: Ending intersection ID
            distance: Length of road segment in km
            speed_limit: Speed limit in km/h
            lanes: Number of lanes
        """
        self.graph.add_edge(
            from_intersection, 
            to_intersection,
            distance=distance,
            speed_limit=speed_limit,
            lanes=lanes,
            base_travel_time=distance / speed_limit  # hours
        )
    
    def update_traffic_flow(self, from_intersection: str, to_intersection: str, 
                           vehicle_count: int, timestamp: Optional[str] = None):
        """
        Update traffic flow data for a road segment.
        
        Args:
            from_intersection: Starting intersection ID
            to_intersection: Ending intersection ID
            vehicle_count: Number of vehicles on the segment
            timestamp: Time of measurement (optional)
        """
        edge_key = (from_intersection, to_intersection)
        if edge_key not in self.traffic_data:
            self.traffic_data[edge_key] = []
        
        self.traffic_data[edge_key].append({
            'vehicle_count': vehicle_count,
            'timestamp': timestamp
        })
        
        # Update current travel time based on congestion
        if self.graph.has_edge(from_intersection, to_intersection):
            edge_data = self.graph[from_intersection][to_intersection]
            base_time = edge_data['base_travel_time']
            lanes = edge_data.get('lanes', 1)
            
            # Calculate congestion factor (simplified model)
            capacity = lanes * self.lane_capacity  # vehicles per hour per lane
            congestion_factor = 1 + (vehicle_count / capacity) ** 2
            
            self.graph[from_intersection][to_intersection]['travel_time'] = base_time * congestion_factor
            self.graph[from_intersection][to_intersection]['congestion_level'] = min(congestion_factor - 1, 1.0)
    
    def get_current_traffic(self, from_intersection: str, to_intersection: str) -> Optional[Dict]:
        """
        Get current traffic data for a road segment.
        
        Args:
            from_intersection: Starting intersection ID
            to_intersection: Ending intersection ID
            
        Returns:
            Dictionary with current traffic data or None
        """
        edge_key = (from_intersection, to_intersection)
        if edge_key in self.traffic_data and self.traffic_data[edge_key]:
            return self.traffic_data[edge_key][-1]
        return None
    
    def get_all_intersections(self) -> List[str]:
        """Get list of all intersection IDs."""
        return list(self.graph.nodes())
    
    def get_all_roads(self) -> List[Tuple[str, str]]:
        """Get list of all road segments as (from, to) tuples."""
        return list(self.graph.edges())
    
    def generate_sample_network(self, grid_size: int = 5):
        """
        Generate a sample grid-based traffic network for demonstration.
        
        Args:
            grid_size: Size of the grid (grid_size x grid_size intersections)
        """
        # Create grid of intersections
        for i in range(grid_size):
            for j in range(grid_size):
                intersection_id = f"I_{i}_{j}"
                self.add_intersection(intersection_id, latitude=i * 0.01, longitude=j * 0.01)
        
        # Add horizontal and vertical roads
        for i in range(grid_size):
            for j in range(grid_size):
                current = f"I_{i}_{j}"
                
                # Add horizontal roads (both directions)
                if j < grid_size - 1:
                    next_h = f"I_{i}_{j+1}"
                    distance = np.random.uniform(0.5, 2.0)
                    speed_limit = np.random.choice([30, 40, 50, 60])
                    lanes = np.random.choice([1, 2, 3])
                    self.add_road(current, next_h, distance, speed_limit, lanes)
                    self.add_road(next_h, current, distance, speed_limit, lanes)
                
                # Add vertical roads (both directions)
                if i < grid_size - 1:
                    next_v = f"I_{i+1}_{j}"
                    distance = np.random.uniform(0.5, 2.0)
                    speed_limit = np.random.choice([30, 40, 50, 60])
                    lanes = np.random.choice([1, 2, 3])
                    self.add_road(current, next_v, distance, speed_limit, lanes)
                    self.add_road(next_v, current, distance, speed_limit, lanes)
        
        # Simulate random traffic
        for edge in self.graph.edges():
            vehicle_count = np.random.randint(50, 1500)
            self.update_traffic_flow(edge[0], edge[1], vehicle_count)
