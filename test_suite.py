#!/usr/bin/env python3
"""
Test Script - Validates all core functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from traffic_analysis import TrafficNetwork, CongestionDetector, RouteOptimizer, TrafficVisualizer

def test_traffic_network():
    """Test TrafficNetwork functionality."""
    print("Testing TrafficNetwork...")
    network = TrafficNetwork(lane_capacity=2000)
    
    # Test adding intersections
    network.add_intersection("A", 0.0, 0.0)
    network.add_intersection("B", 0.0, 1.0)
    network.add_intersection("C", 1.0, 1.0)
    assert len(network.get_all_intersections()) == 3, "Failed to add intersections"
    
    # Test adding roads
    network.add_road("A", "B", 10.0, 50, 2)
    network.add_road("B", "C", 8.0, 60, 3)
    assert len(network.get_all_roads()) == 2, "Failed to add roads"
    
    # Test updating traffic
    network.update_traffic_flow("A", "B", 1000)
    traffic = network.get_current_traffic("A", "B")
    assert traffic is not None, "Failed to get traffic data"
    assert traffic['vehicle_count'] == 1000, "Incorrect vehicle count"
    
    print("✓ TrafficNetwork tests passed")
    return network

def test_congestion_detector(network):
    """Test CongestionDetector functionality."""
    print("Testing CongestionDetector...")
    detector = CongestionDetector(network)
    
    # Test hotspot detection
    hotspots = detector.identify_hotspots(threshold=0.0)
    assert isinstance(hotspots, list), "Hotspots should be a list"
    
    # Test intersection congestion
    intersection_congestion = detector.get_intersection_congestion()
    assert isinstance(intersection_congestion, dict), "Should return dict"
    assert len(intersection_congestion) == 3, "Should have 3 intersections"
    
    # Test top intersections
    top = detector.get_top_congested_intersections(top_n=2)
    assert len(top) <= 2, "Should return at most 2 intersections"
    
    # Test report generation
    report = detector.generate_hotspot_report()
    assert isinstance(report, str), "Report should be string"
    assert "CONGESTION HOTSPOT REPORT" in report, "Report missing header"
    
    print("✓ CongestionDetector tests passed")

def test_route_optimizer(network):
    """Test RouteOptimizer functionality."""
    print("Testing RouteOptimizer...")
    optimizer = RouteOptimizer(network)
    
    # Test optimal route finding
    route = optimizer.find_optimal_route("A", "C", "time")
    assert route is None or 'path' in route, "Route should have path"
    
    # Test route comparison
    routes = optimizer.compare_routes("A", "C")
    assert 'fastest' in routes, "Should have fastest route"
    assert 'shortest' in routes, "Should have shortest route"
    assert 'least_congested' in routes, "Should have least congested route"
    
    # Test alternative routes
    alternatives = optimizer.find_alternative_routes("A", "C", k=2)
    assert isinstance(alternatives, list), "Should return list"
    
    # Test report generation
    if routes['fastest']:
        report = optimizer.generate_route_report("A", "C")
        assert isinstance(report, str), "Report should be string"
        assert "ROUTE OPTIMIZATION REPORT" in report, "Report missing header"
    
    print("✓ RouteOptimizer tests passed")

def test_visualization(network):
    """Test TrafficVisualizer functionality."""
    print("Testing TrafficVisualizer...")
    visualizer = TrafficVisualizer(network)
    
    # Test that visualizer initializes
    assert visualizer.network == network, "Network not set correctly"
    
    print("✓ TrafficVisualizer tests passed")

def test_sample_network():
    """Test sample network generation."""
    print("Testing sample network generation...")
    network = TrafficNetwork()
    network.generate_sample_network(grid_size=3)
    
    assert len(network.get_all_intersections()) == 9, "Should have 9 intersections"
    assert len(network.get_all_roads()) > 0, "Should have roads"
    
    # Verify traffic data exists
    assert len(network.traffic_data) > 0, "Should have traffic data"
    
    print("✓ Sample network generation tests passed")

def main():
    """Run all tests."""
    print("=" * 60)
    print("TRAFFIC PATTERN ANALYSIS - TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # Test basic network functionality
        network = test_traffic_network()
        
        # Test congestion detection
        test_congestion_detector(network)
        
        # Test route optimization
        test_route_optimizer(network)
        
        # Test visualization
        test_visualization(network)
        
        # Test sample network generation
        test_sample_network()
        
        print()
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
