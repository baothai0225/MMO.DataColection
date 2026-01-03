# MMO Data Collection

A Python-based data collection tool that uses the `tls-client` library to access websites like Shopee.vn for data scraping and interacts with internal APIs.

## Features

- **TLS Client Integration**: Uses `tls-client` library for enhanced security and bypassing bot detection
- **Shopee Data Scraper**: Collect data from Shopee Vietnam marketplace
  - Homepage data collection
  - Product search functionality
  - Product details retrieval
- **Internal API Client**: Send collected data to your internal APIs
- **Configurable**: Easy configuration through environment variables
- **Retry Logic**: Built-in retry mechanism for robust data collection
- **Logging**: Comprehensive logging for monitoring and debugging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/baothai0225/MMO.DataColection.git
cd MMO.DataColection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Create a `.env` file based on `.env.example` and configure:

- `INTERNAL_API_URL`: Your internal API endpoint
- `API_TIMEOUT`: API request timeout in seconds
- `TLS_CLIENT_IDENTIFIER`: Browser identifier for TLS client
- `MAX_RETRIES`: Maximum retry attempts
- `RETRY_DELAY`: Delay between retries in seconds

## Usage

### Quick Start

Run the example script:
```bash
python example.py
```

### Using in Your Code

```python
from data_collection import DataCollectionPipeline

# Initialize pipeline
pipeline = DataCollectionPipeline()

# Collect homepage data
pipeline.collect_and_send_homepage_data()

# Search products
pipeline.search_and_send_products("laptop", limit=10)

# Get product details
pipeline.collect_product_details(shop_id=12345, item_id=67890)

# Clean up
pipeline.close()
```

### Individual Components

#### TLS Client Wrapper
```python
from tls_client_wrapper import TLSClientWrapper

client = TLSClientWrapper()
response = client.get("https://shopee.vn/")
client.close()
```

#### Shopee Scraper
```python
from shopee_scraper import ShopeeDataScraper

scraper = ShopeeDataScraper()
data = scraper.get_homepage_data()
products = scraper.search_products("phone", limit=5)
scraper.close()
```

#### API Client
```python
from api_client import InternalAPIClient

api = InternalAPIClient(api_url="http://your-api.com/api")
response = api.send_data("/endpoint", {"key": "value"})
api.close()
```

## Project Structure

```
MMO.DataColection/
├── config.py                 # Configuration management
├── tls_client_wrapper.py     # TLS client wrapper
├── shopee_scraper.py         # Shopee data scraper
├── api_client.py             # Internal API client
├── data_collection.py        # Main data collection pipeline
├── example.py                # Example usage script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Dependencies

- `tls-client>=1.0.1`: TLS client for enhanced web requests
- `requests>=2.31.0`: HTTP library
- `python-dotenv>=1.0.0`: Environment variable management

## Security Notes

- The `.env` file is gitignored and should never be committed
- Keep your API credentials secure
- Use appropriate TLS client identifiers to match real browsers
- Respect website terms of service and rate limits

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
