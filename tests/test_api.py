"""
API endpoint tests for the Cartouche Bot Service.
Tests all API endpoints and their functionality.
"""
import os
import sys
import asyncio
import logging
import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

# Create test client
client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    logger.info("Testing root endpoint...")
    
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    
    logger.info("Root endpoint test passed")

def test_health_endpoint():
    """Test health endpoint."""
    logger.info("Testing health endpoint...")
    
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    
    logger.info("Health endpoint test passed")

def test_admin_stats_endpoint():
    """Test admin stats endpoint."""
    logger.info("Testing admin stats endpoint...")
    
    response = client.get("/api/admin/stats")
    assert response.status_code == 200
    
    logger.info("Admin stats endpoint test passed")

def test_admin_bots_endpoint():
    """Test admin bots endpoint."""
    logger.info("Testing admin bots endpoint...")
    
    response = client.get("/api/admin/bots")
    assert response.status_code == 200
    
    logger.info("Admin bots endpoint test passed")

def test_admin_activities_endpoint():
    """Test admin activities endpoint."""
    logger.info("Testing admin activities endpoint...")
    
    response = client.get("/api/admin/activities")
    assert response.status_code == 200
    
    logger.info("Admin activities endpoint test passed")

def test_admin_config_endpoint():
    """Test admin config endpoint."""
    logger.info("Testing admin config endpoint...")
    
    response = client.get("/api/admin/config")
    assert response.status_code == 200
    
    logger.info("Admin config endpoint test passed")

def test_bots_endpoint():
    """Test bots endpoint."""
    logger.info("Testing bots endpoint...")
    
    response = client.get("/api/bots/")
    assert response.status_code == 200
    
    logger.info("Bots endpoint test passed")

def test_monitoring_health_endpoint():
    """Test monitoring health endpoint."""
    logger.info("Testing monitoring health endpoint...")
    
    response = client.get("/api/monitoring/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"
    
    logger.info("Monitoring health endpoint test passed")

def test_monitoring_stats_endpoint():
    """Test monitoring stats endpoint."""
    logger.info("Testing monitoring stats endpoint...")
    
    response = client.get("/api/monitoring/stats")
    assert response.status_code == 200
    
    logger.info("Monitoring stats endpoint test passed")

def test_monitoring_reactions_endpoint():
    """Test monitoring reactions endpoint."""
    logger.info("Testing monitoring reactions endpoint...")
    
    response = client.get("/api/monitoring/reactions")
    assert response.status_code == 200
    
    logger.info("Monitoring reactions endpoint test passed")

def run_tests():
    """Run all tests."""
    logger.info("Starting API endpoint tests...")
    
    # Create test results directory
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    
    # Run tests
    test_functions = [
        test_root_endpoint,
        test_health_endpoint,
        test_admin_stats_endpoint,
        test_admin_bots_endpoint,
        test_admin_activities_endpoint,
        test_admin_config_endpoint,
        test_bots_endpoint,
        test_monitoring_health_endpoint,
        test_monitoring_stats_endpoint,
        test_monitoring_reactions_endpoint
    ]
    
    results = {}
    for test_func in test_functions:
        test_name = test_func.__name__
        try:
            test_func()
            results[test_name] = True
        except Exception as e:
            logger.error(f"Test {test_name} failed: {str(e)}")
            results[test_name] = False
    
    # Log results
    logger.info("API endpoint test results:")
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        logger.info(f"  {test_name}: {status}")
    
    # Write results to file
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(results_dir / f"api_test_results_{timestamp}.txt", "w") as f:
        f.write(f"API Endpoint Test Results - {datetime.now().isoformat()}\n")
        f.write("=" * 50 + "\n\n")
        
        for test_name, result in results.items():
            status = "PASSED" if result else "FAILED"
            f.write(f"{test_name}: {status}\n")
    
    # Return overall result
    return all(results.values())

if __name__ == "__main__":
    # Run tests
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result else 1)
