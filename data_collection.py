"""
Main Data Collection Module
Orchestrates data collection from websites and API invocation
"""
import logging
from typing import Optional
from shopee_scraper import ShopeeDataScraper
from api_client import InternalAPIClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataCollectionPipeline:
    """Main pipeline for collecting and processing data"""
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize data collection pipeline
        
        Args:
            api_url: Optional internal API URL
        """
        self.shopee_scraper = ShopeeDataScraper()
        self.api_client = InternalAPIClient(api_url)
        logger.info("DataCollectionPipeline initialized")
    
    def collect_and_send_homepage_data(self) -> bool:
        """
        Collect homepage data from Shopee and send to internal API
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Starting homepage data collection...")
            
            # Collect data from Shopee
            homepage_data = self.shopee_scraper.get_homepage_data()
            
            if not homepage_data:
                logger.error("Failed to collect homepage data")
                return False
            
            logger.info(f"Collected homepage data: {homepage_data.get('content_length', 0)} bytes")
            
            # Send data to internal API
            api_response = self.api_client.send_data('shopee/homepage', homepage_data)
            
            if api_response:
                logger.info("Successfully sent homepage data to API")
                return True
            else:
                logger.error("Failed to send data to API")
                return False
                
        except Exception as e:
            logger.error(f"Error in homepage data collection: {str(e)}")
            return False
    
    def search_and_send_products(self, keyword: str, limit: int = 10) -> bool:
        """
        Search for products and send results to internal API
        
        Args:
            keyword: Search keyword
            limit: Maximum number of products
            
        Returns:
            True if successful, False otherwise
        """
        # Validate keyword
        if not keyword or not keyword.strip():
            logger.error("Keyword cannot be empty")
            return False
        
        if len(keyword) > 200:
            logger.error("Keyword exceeds maximum length of 200 characters")
            return False
        
        try:
            logger.info(f"Searching for products with keyword: {keyword}")
            
            # Search products on Shopee
            products = self.shopee_scraper.search_products(keyword, limit)
            
            if not products:
                logger.error("Failed to search products")
                return False
            
            logger.info(f"Found products data")
            
            # Send products to internal API
            data_to_send = {
                'keyword': keyword,
                'limit': limit,
                'products': products
            }
            
            api_response = self.api_client.send_data('shopee/products', data_to_send)
            
            if api_response:
                logger.info("Successfully sent products data to API")
                return True
            else:
                logger.error("Failed to send products to API")
                return False
                
        except Exception as e:
            logger.error(f"Error in product search and send: {str(e)}")
            return False
    
    def collect_product_details(self, shop_id: int, item_id: int) -> bool:
        """
        Collect product details and send to internal API
        
        Args:
            shop_id: Shop ID
            item_id: Item ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Collecting product details for shop_id={shop_id}, item_id={item_id}")
            
            # Get product details
            product_details = self.shopee_scraper.get_product_details(shop_id, item_id)
            
            if not product_details:
                logger.error("Failed to get product details")
                return False
            
            logger.info("Collected product details")
            
            # Send to internal API
            api_response = self.api_client.send_data('shopee/product-details', product_details)
            
            if api_response:
                logger.info("Successfully sent product details to API")
                return True
            else:
                logger.error("Failed to send product details to API")
                return False
                
        except Exception as e:
            logger.error(f"Error in product details collection: {str(e)}")
            return False
    
    def close(self):
        """Cleanup resources"""
        self.shopee_scraper.close()
        self.api_client.close()
        logger.info("DataCollectionPipeline closed")
