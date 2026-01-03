"""
Example script demonstrating the usage of MMO Data Collection
"""
import sys
from data_collection import DataCollectionPipeline


def main():
    """Main function to demonstrate data collection"""
    
    print("=" * 60)
    print("MMO Data Collection - Example Usage")
    print("=" * 60)
    print()
    
    # Initialize the data collection pipeline
    # You can pass custom API URL: DataCollectionPipeline(api_url='http://your-api.com/api')
    pipeline = DataCollectionPipeline()
    
    try:
        # Example 1: Collect homepage data from Shopee
        print("1. Collecting Shopee homepage data...")
        print("-" * 60)
        success = pipeline.collect_and_send_homepage_data()
        if success:
            print("✓ Successfully collected and sent homepage data")
        else:
            print("✗ Failed to collect homepage data")
        print()
        
        # Example 2: Search for products
        print("2. Searching for products...")
        print("-" * 60)
        keyword = "phone"  # You can change this to any keyword
        success = pipeline.search_and_send_products(keyword, limit=5)
        if success:
            print(f"✓ Successfully searched and sent products for '{keyword}'")
        else:
            print(f"✗ Failed to search products for '{keyword}'")
        print()
        
        # Example 3: Get product details (example IDs)
        print("3. Getting product details...")
        print("-" * 60)
        # Note: These are example IDs, replace with actual IDs from search results
        shop_id = 12345678
        item_id = 87654321
        success = pipeline.collect_product_details(shop_id, item_id)
        if success:
            print(f"✓ Successfully collected product details")
        else:
            print(f"✗ Failed to collect product details")
        print()
        
        print("=" * 60)
        print("Example completed!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        pipeline.close()


if __name__ == "__main__":
    main()
