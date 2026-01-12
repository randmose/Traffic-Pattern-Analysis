"""
Route Optimizer Module
Finds optimal routes considering traffic conditions.
"""

import networkx as nx
from typing import List, Optional, Dict, Tuple
from .traffic_network import TrafficNetwork


class RouteOptimizer:
    """
    Optimizes routes through the traffic network considering current traffic conditions.
    """
    
    def __init__(self, network: TrafficNetwork):
        """
        Initialize the route optimizer.
        
        Args:
            network: TrafficNetwork instance to optimize routes on
        """
        self.network = network
    
    def find_optimal_route(self, start: str, end: str, 
                          optimization: str = "time") -> Optional[Dict]:
        """
        Find the optimal route between two intersections.
        
        Args:
            start: Starting intersection ID
            end: Ending intersection ID
            optimization: Optimization criterion ("time", "distance", or "avoid_congestion")
            
        Returns:
            Dictionary containing route information or None if no path exists
        """
        if start not in self.network.graph or end not in self.network.graph:
            return None
        
        try:
            if optimization == "time":
                # Use travel time as weight
                path = nx.shortest_path(
                    self.network.graph, 
                    start, 
                    end, 
                    weight='travel_time'
                )
                total_cost = nx.shortest_path_length(
                    self.network.graph,
                    start,
                    end,
                    weight='travel_time'
                )
            elif optimization == "distance":
                # Use distance as weight
                path = nx.shortest_path(
                    self.network.graph,
                    start,
                    end,
                    weight='distance'
                )
                total_cost = nx.shortest_path_length(
                    self.network.graph,
                    start,
                    end,
                    weight='distance'
                )
            elif optimization == "avoid_congestion":
                # Use congestion level as weight
                path = nx.shortest_path(
                    self.network.graph,
                    start,
                    end,
                    weight='congestion_level'
                )
                total_cost = nx.shortest_path_length(
                    self.network.graph,
                    start,
                    end,
                    weight='congestion_level'
                )
            else:
                return None
            
            # Calculate route statistics
            total_distance = 0
            total_time = 0
            avg_congestion = 0
            segments = []
            
            for i in range(len(path) - 1):
                from_node = path[i]
                to_node = path[i + 1]
                edge_data = self.network.graph[from_node][to_node]
                
                segment = {
                    'from': from_node,
                    'to': to_node,
                    'distance': edge_data.get('distance', 0),
                    'travel_time': edge_data.get('travel_time', 0),
                    'congestion_level': edge_data.get('congestion_level', 0),
                    'speed_limit': edge_data.get('speed_limit', 0)
                }
                segments.append(segment)
                
                total_distance += segment['distance']
                total_time += segment['travel_time']
                avg_congestion += segment['congestion_level']
            
            avg_congestion = avg_congestion / len(segments) if segments else 0
            
            return {
                'start': start,
                'end': end,
                'path': path,
                'segments': segments,
                'total_distance': total_distance,
                'total_time': total_time,
                'avg_congestion': avg_congestion,
                'optimization_type': optimization,
                'optimization_value': total_cost
            }
            
        except nx.NetworkXNoPath:
            return None
    
    def compare_routes(self, start: str, end: str) -> Dict[str, Optional[Dict]]:
        """
        Compare different route optimization strategies.
        
        Args:
            start: Starting intersection ID
            end: Ending intersection ID
            
        Returns:
            Dictionary with routes for each optimization type
        """
        return {
            'fastest': self.find_optimal_route(start, end, "time"),
            'shortest': self.find_optimal_route(start, end, "distance"),
            'least_congested': self.find_optimal_route(start, end, "avoid_congestion")
        }
    
    def find_alternative_routes(self, start: str, end: str, 
                               k: int = 3) -> List[Dict]:
        """
        Find k alternative routes between two intersections.
        
        Args:
            start: Starting intersection ID
            end: Ending intersection ID
            k: Number of alternative routes to find
            
        Returns:
            List of route dictionaries
        """
        if start not in self.network.graph or end not in self.network.graph:
            return []
        
        try:
            # Find k shortest paths based on travel time
            paths = list(nx.shortest_simple_paths(
                self.network.graph,
                start,
                end,
                weight='travel_time'
            ))
            
            routes = []
            for path in paths[:k]:
                # Calculate statistics for this path
                total_distance = 0
                total_time = 0
                avg_congestion = 0
                segments = []
                
                for i in range(len(path) - 1):
                    from_node = path[i]
                    to_node = path[i + 1]
                    edge_data = self.network.graph[from_node][to_node]
                    
                    segment = {
                        'from': from_node,
                        'to': to_node,
                        'distance': edge_data.get('distance', 0),
                        'travel_time': edge_data.get('travel_time', 0),
                        'congestion_level': edge_data.get('congestion_level', 0)
                    }
                    segments.append(segment)
                    
                    total_distance += segment['distance']
                    total_time += segment['travel_time']
                    avg_congestion += segment['congestion_level']
                
                avg_congestion = avg_congestion / len(segments) if segments else 0
                
                routes.append({
                    'path': path,
                    'segments': segments,
                    'total_distance': total_distance,
                    'total_time': total_time,
                    'avg_congestion': avg_congestion
                })
            
            return routes
            
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
    
    def generate_route_report(self, start: str, end: str) -> str:
        """
        Generate a detailed route report with multiple options.
        
        Args:
            start: Starting intersection ID
            end: Ending intersection ID
            
        Returns:
            Formatted report string
        """
        report = "=" * 60 + "\n"
        report += "ROUTE OPTIMIZATION REPORT\n"
        report += "=" * 60 + "\n\n"
        report += f"Start: {start}\n"
        report += f"End: {end}\n\n"
        
        routes = self.compare_routes(start, end)
        
        # Fastest route
        report += "-" * 60 + "\n"
        report += "FASTEST ROUTE (Time-Optimized):\n"
        report += "-" * 60 + "\n"
        if routes['fastest']:
            route = routes['fastest']
            report += f"Total Travel Time: {route['total_time']*60:.1f} minutes\n"
            report += f"Total Distance: {route['total_distance']:.2f} km\n"
            report += f"Average Congestion: {route['avg_congestion']:.1%}\n"
            report += f"Path: {' → '.join(route['path'])}\n\n"
        else:
            report += "No route found.\n\n"
        
        # Shortest route
        report += "-" * 60 + "\n"
        report += "SHORTEST ROUTE (Distance-Optimized):\n"
        report += "-" * 60 + "\n"
        if routes['shortest']:
            route = routes['shortest']
            report += f"Total Distance: {route['total_distance']:.2f} km\n"
            report += f"Total Travel Time: {route['total_time']*60:.1f} minutes\n"
            report += f"Average Congestion: {route['avg_congestion']:.1%}\n"
            report += f"Path: {' → '.join(route['path'])}\n\n"
        else:
            report += "No route found.\n\n"
        
        # Least congested route
        report += "-" * 60 + "\n"
        report += "LEAST CONGESTED ROUTE:\n"
        report += "-" * 60 + "\n"
        if routes['least_congested']:
            route = routes['least_congested']
            report += f"Average Congestion: {route['avg_congestion']:.1%}\n"
            report += f"Total Distance: {route['total_distance']:.2f} km\n"
            report += f"Total Travel Time: {route['total_time']*60:.1f} minutes\n"
            report += f"Path: {' → '.join(route['path'])}\n\n"
        else:
            report += "No route found.\n\n"
        
        report += "=" * 60 + "\n"
        
        return report
