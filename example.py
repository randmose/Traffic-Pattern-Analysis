#!/usr/bin/env python3
"""
Example Script: Custom Traffic Network Analysis
Demonstrates how to create a custom traffic network and perform analysis.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from traffic_analysis import TrafficNetwork, CongestionDetector, RouteOptimizer


def create_city_network():
    """Create a sample city traffic network."""
    network = TrafficNetwork()
    
    # Add intersections (major city locations)
    locations = {
        'Downtown': (40.7128, -74.0060),
        'Airport': (40.6413, -73.7781),
        'University': (40.7295, -73.9965),
        'Mall': (40.7589, -73.9851),
        'Hospital': (40.7614, -73.9776),
        'Stadium': (40.7505, -73.9934),
        'Harbor': (40.7069, -74.0113),
        'Park': (40.7829, -73.9654)
    }
    
    for location, (lat, lon) in locations.items():
        network.add_intersection(location, lat, lon)
    
    # Add roads with different characteristics
    roads = [
        ('Downtown', 'Airport', 15.5, 60, 3),
        ('Downtown', 'University', 3.2, 40, 2),
        ('Downtown', 'Harbor', 2.1, 30, 2),
        ('University', 'Mall', 2.8, 50, 2),
        ('University', 'Stadium', 1.5, 40, 1),
        ('Mall', 'Hospital', 1.2, 50, 2),
        ('Mall', 'Park', 3.5, 60, 3),
        ('Hospital', 'Stadium', 1.8, 40, 2),
        ('Stadium', 'Park', 2.4, 50, 2),
        ('Airport', 'Mall', 12.0, 70, 4),
        ('Harbor', 'Stadium', 4.5, 50, 2),
    ]
    
    # Add roads in both directions
    for from_loc, to_loc, distance, speed, lanes in roads:
        network.add_road(from_loc, to_loc, distance, speed, lanes)
        network.add_road(to_loc, from_loc, distance, speed, lanes)
    
    # Simulate traffic conditions (vehicle counts per hour)
    traffic_scenarios = [
        ('Downtown', 'Airport', 2500),  # Heavy traffic
        ('Airport', 'Downtown', 2200),  # Heavy traffic
        ('Downtown', 'University', 1800), # Heavy traffic
        ('University', 'Downtown', 1600),
        ('University', 'Mall', 900),
        ('Mall', 'University', 850),
        ('Mall', 'Hospital', 600),
        ('Hospital', 'Mall', 550),
        ('Stadium', 'Harbor', 1200),  # Moderate traffic
        ('Harbor', 'Stadium', 1100),
        ('Park', 'Mall', 700),
        ('Mall', 'Park', 750),
        ('University', 'Stadium', 800),
        ('Stadium', 'University', 750),
        ('Hospital', 'Stadium', 650),
        ('Stadium', 'Hospital', 700),
        ('Stadium', 'Park', 900),
        ('Park', 'Stadium', 850),
        ('Airport', 'Mall', 2000),  # Heavy highway traffic
        ('Mall', 'Airport', 1900),
        ('Downtown', 'Harbor', 1500),
        ('Harbor', 'Downtown', 1400),
        ('Mall', 'Park', 750),
        ('Park', 'Mall', 700),
    ]
    
    for from_loc, to_loc, vehicles in traffic_scenarios:
        network.update_traffic_flow(from_loc, to_loc, vehicles)
    
    return network


def main():
    """Run the example analysis."""
    print("=" * 70)
    print("CUSTOM TRAFFIC NETWORK ANALYSIS EXAMPLE")
    print("=" * 70)
    print()
    
    # Create custom network
    print("Creating custom city traffic network...")
    network = create_city_network()
    print(f"✓ Network created with {len(network.get_all_intersections())} locations")
    print(f"✓ Total road segments: {len(network.get_all_roads())}")
    print()
    
    # Analyze congestion
    print("Analyzing congestion hotspots...")
    detector = CongestionDetector(network)
    hotspots = detector.identify_hotspots(threshold=0.1)  # 10% threshold
    
    print(f"✓ Found {len(hotspots)} congestion hotspots")
    print()
    
    # Show top hotspots
    print("TOP 5 CONGESTION HOTSPOTS:")
    print("-" * 70)
    for i, hotspot in enumerate(hotspots[:5], 1):
        print(f"{i}. {hotspot['from']} → {hotspot['to']}")
        print(f"   Severity: {hotspot['severity']}")
        print(f"   Congestion: {hotspot['congestion_level']:.1%}")
        print(f"   Vehicles: {hotspot['vehicle_count']}")
        print()
    
    # Find optimal routes
    print("=" * 70)
    print("ROUTE OPTIMIZATION EXAMPLES")
    print("=" * 70)
    print()
    
    route_pairs = [
        ('Downtown', 'Airport'),
        ('University', 'Park'),
        ('Harbor', 'Hospital')
    ]
    
    optimizer = RouteOptimizer(network)
    
    for start, end in route_pairs:
        print(f"Route: {start} → {end}")
        print("-" * 70)
        
        # Compare different strategies
        routes = optimizer.compare_routes(start, end)
        
        if routes['fastest']:
            print(f"Fastest Route:")
            print(f"  Path: {' → '.join(routes['fastest']['path'])}")
            print(f"  Time: {routes['fastest']['total_time']*60:.1f} minutes")
            print(f"  Distance: {routes['fastest']['total_distance']:.2f} km")
            print(f"  Avg Congestion: {routes['fastest']['avg_congestion']:.1%}")
        
        if routes['shortest']:
            print(f"Shortest Route:")
            print(f"  Path: {' → '.join(routes['shortest']['path'])}")
            print(f"  Distance: {routes['shortest']['total_distance']:.2f} km")
            print(f"  Time: {routes['shortest']['total_time']*60:.1f} minutes")
        
        print()
    
    # Urban planning recommendations
    print("=" * 70)
    print("URBAN PLANNING RECOMMENDATIONS")
    print("=" * 70)
    print()
    
    top_intersections = detector.get_top_congested_intersections(top_n=3)
    
    print("Priority Infrastructure Improvements:")
    print()
    for i, (location, congestion) in enumerate(top_intersections, 1):
        print(f"{i}. {location}")
        print(f"   Average Congestion: {congestion:.1%}")
        
        if congestion > 0.7:
            print(f"   Recommendation: Add lanes or create bypass route")
        elif congestion > 0.5:
            print(f"   Recommendation: Optimize traffic light timing")
        else:
            print(f"   Recommendation: Monitor for future growth")
        print()
    
    print("=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
