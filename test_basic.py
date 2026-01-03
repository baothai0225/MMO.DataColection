"""
Simple test script to verify the data collection functionality
"""
from tls_client_wrapper import TLSClientWrapper
from shopee_scraper import ShopeeDataScraper
from api_client import InternalAPIClient
from data_collection import DataCollectionPipeline
from config import Config


def test_tls_client():
    """Test TLS Client Wrapper"""
    print("Testing TLS Client Wrapper...")
    client = TLSClientWrapper()
    assert client.session is not None
    assert client.client_identifier == Config.TLS_CLIENT_IDENTIFIER
    client.close()
    print("✓ TLS Client Wrapper test passed")


def test_shopee_scraper():
    """Test Shopee Scraper"""
    print("Testing Shopee Scraper...")
    scraper = ShopeeDataScraper()
    assert scraper.client is not None
    assert scraper.base_url == Config.SHOPEE_VN_URL
    scraper.close()
    print("✓ Shopee Scraper test passed")


def test_api_client():
    """Test API Client"""
    print("Testing API Client...")
    client = InternalAPIClient()
    assert client.client is not None
    assert client.api_url is not None
    client.close()
    print("✓ API Client test passed")


def test_data_collection_pipeline():
    """Test Data Collection Pipeline"""
    print("Testing Data Collection Pipeline...")
    pipeline = DataCollectionPipeline()
    assert pipeline.shopee_scraper is not None
    assert pipeline.api_client is not None
    pipeline.close()
    print("✓ Data Collection Pipeline test passed")


def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Tests for MMO Data Collection")
    print("=" * 60)
    print()
    
    try:
        test_tls_client()
        print()
        
        test_shopee_scraper()
        print()
        
        test_api_client()
        print()
        
        test_data_collection_pipeline()
        print()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {str(e)}")
        return False
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
