import json
import random
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class PropertyFetcher:
    def __init__(self):
        self.properties = []
        self.load_or_create_properties()

    def load_or_create_properties(self):
        """Load existing properties or create new ones"""
        try:
            with open('properties.json', 'r') as f:
                self.properties = json.load(f)
        except:
            self.properties = self.fetch_sample_properties()
            self.save_properties()

    def fetch_sample_properties(self):
        """
        Creates sample property data
        """
        try:
            # Create sample data with more variety
            cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Miami", "Seattle", "Boston"]
            streets = ["Main St", "Oak Ave", "Maple Rd", "Cedar Ln", "Pine Dr", "Beach Blvd", "Lake View Dr", "Market St"]
            states = ["NY", "CA", "IL", "TX", "AZ", "FL", "WA", "MA"]
            property_types = ["Single Family", "Condo", "Townhouse", "Multi-Family", "Apartment"]
            conditions = ["Excellent", "Good", "Fair", "Needs Work"]
            
            properties = []
            for i in range(20):  # Generate 20 sample properties
                city = random.choice(cities)
                street = random.choice(streets)
                state = random.choice(states)
                number = random.randint(100, 9999)
                
            properties = []
            for i in range(50):  # Generate 50 sample properties
                city = random.choice(cities)
                street = random.choice(streets)
                state = random.choice(states)
                number = random.randint(100, 9999)
                prop_type = random.choice(property_types)
                condition = random.choice(conditions)
                
                base_price = self._generate_sample_price()
                monthly_rent = round(base_price * random.uniform(0.005, 0.012))  # 0.5% to 1.2% of price
                
                # Calculate investment metrics
                monthly_expenses = round(base_price * random.uniform(0.001, 0.002))  # Property tax, insurance, maintenance
                vacancy_rate = random.uniform(0.03, 0.08)  # 3-8% vacancy rate
                annual_rent = monthly_rent * 12
                annual_expenses = monthly_expenses * 12
                effective_gross_income = annual_rent * (1 - vacancy_rate)
                net_operating_income = effective_gross_income - annual_expenses
                cash_flow = net_operating_income - (base_price * 0.05)  # Assuming 5% mortgage rate
                roi = (cash_flow / base_price) * 100
                
                property_item = {
                    'id': f"prop_{i}",
                    'address': f"{number} {street}",
                    'city': city,
                    'state': state,
                    'price': base_price,
                    'bedrooms': self._generate_sample_rooms(),
                    'bathrooms': self._generate_sample_rooms(),
                    'sqft': self._generate_sample_sqft(),
                    'type': prop_type,
                    'condition': condition,
                    'year_built': random.randint(1950, 2024),
                    'monthly_rent': monthly_rent,
                    'monthly_expenses': monthly_expenses,
                    'vacancy_rate': round(vacancy_rate * 100, 1),
                    'cap_rate': round(((monthly_rent * 12) / base_price) * 100, 2),
                    'cash_flow': round(cash_flow / 12, 2),  # Monthly cash flow
                    'roi': round(roi, 2),
                    'price_per_sqft': round(base_price / self._generate_sample_sqft(), 2),
                    'lot_size': round(random.uniform(0.1, 2.0), 2),
                    'appreciation_potential': random.randint(1, 5),  # 1-5 rating
                    'neighborhood_rating': random.randint(1, 5),  # 1-5 rating
                    'last_updated': datetime.now().isoformat()
                }
                properties.append(property_item)
            return properties
        except Exception as e:
            print(f"Error fetching properties: {str(e)}")
            return []

    def _generate_sample_price(self):
        """Generate a random price for demo purposes"""
        import random
        return random.randint(200000, 1500000)

    def _generate_sample_rooms(self):
        """Generate a random number of rooms for demo purposes"""
        import random
        return random.randint(1, 5)

    def _generate_sample_sqft(self):
        """Generate a random square footage for demo purposes"""
        import random
        return random.randint(1000, 4000)

    def save_properties(self):
        """Save the properties to a JSON file"""
        try:
            with open('properties.json', 'w') as f:
                json.dump(self.properties, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving properties: {str(e)}")
            return False

    def search_properties(self, params):
        """Search properties based on various criteria"""
        results = self.properties.copy()
        
        if 'query' in params:
            query = params['query'][0].lower()
            results = [p for p in results if
                      query in p['address'].lower() or
                      query in p['city'].lower() or
                      query in p['state'].lower() or
                      query in p['type'].lower()]

        if 'min_price' in params:
            min_price = int(params['min_price'][0])
            results = [p for p in results if p['price'] >= min_price]

        if 'max_price' in params:
            max_price = int(params['max_price'][0])
            results = [p for p in results if p['price'] <= max_price]

        if 'bedrooms' in params:
            beds = int(params['bedrooms'][0])
            results = [p for p in results if p['bedrooms'] >= beds]

        if 'bathrooms' in params:
            baths = int(params['bathrooms'][0])
            results = [p for p in results if p['bathrooms'] >= baths]

        if 'property_type' in params:
            prop_type = params['property_type'][0]
            results = [p for p in results if p['type'] == prop_type]

        if 'min_cap_rate' in params:
            min_cap = float(params['min_cap_rate'][0])
            results = [p for p in results if p['cap_rate'] >= min_cap]

        if 'min_cash_flow' in params:
            min_cash = float(params['min_cash_flow'][0])
            results = [p for p in results if p['cash_flow'] >= min_cash]

        if 'min_roi' in params:
            min_roi = float(params['min_roi'][0])
            results = [p for p in results if p['roi'] >= min_roi]

        if 'max_vacancy' in params:
            max_vacancy = float(params['max_vacancy'][0])
            results = [p for p in results if p['vacancy_rate'] <= max_vacancy]

        if 'min_neighborhood_rating' in params:
            min_rating = int(params['min_neighborhood_rating'][0])
            results = [p for p in results if p['neighborhood_rating'] >= min_rating]

        if 'sort_by' in params:
            sort_key = params['sort_by'][0]
            reverse = params.get('sort_order', ['asc'])[0] == 'desc'
            results.sort(key=lambda x: x[sort_key], reverse=reverse)

        return results

class PropertyAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.property_fetcher = PropertyFetcher()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/properties':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            params = parse_qs(parsed_path.query)
            properties = self.property_fetcher.search_properties(params)
            
            self.wfile.write(json.dumps(properties).encode())
            return
        
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PropertyAPIHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()