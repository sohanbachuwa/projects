from threading import Lock
import random
import time
import threading

# Constants
NUM_TICKERS = 1024
BUY = 0
SELL = 1

class Order:
    def __init__(self, order_type, ticker, quantity, price, timestamp=None):
        self.order_type = order_type  # BUY or SELL
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp or time.time()

class OrderBook:
    def __init__(self):
        # Create arrays for buy and sell orders for each ticker
        self.buy_orders = [[] for _ in range(NUM_TICKERS)]
        self.sell_orders = [[] for _ in range(NUM_TICKERS)]
        
        # Use locks per ticker to prevent race conditions
        self.locks = [Lock() for _ in range(NUM_TICKERS)]
        
        # Transaction log
        self.transaction_log = []
        self.log_lock = Lock()
        
    def add_order(self, order_type, ticker, quantity, price):
        """Add a new order to the order book."""
        if not (0 <= ticker < NUM_TICKERS):
            raise ValueError(f"Ticker ID must be between 0 and {NUM_TICKERS-1}")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if price <= 0:
            raise ValueError("Price must be positive")
        
        order = Order(order_type, ticker, quantity, price)
        
        # Lock the ticker's order book to prevent race conditions
        with self.locks[ticker]:
            if order_type == BUY:
                self.buy_orders[ticker].append(order)
                # Sort buy orders by price (highest first) and then by timestamp (oldest first)
                self.buy_orders[ticker].sort(key=lambda x: (-x.price, x.timestamp))
            else:  # SELL
                self.sell_orders[ticker].append(order)
                # Sort sell orders by price (lowest first) and then by timestamp (oldest first)
                self.sell_orders[ticker].sort(key=lambda x: (x.price, x.timestamp))
        
        # Try to match orders after adding new one
        self.match_orders(ticker)
        
        return order
    
    def match_orders(self, ticker):
        """Match buy and sell orders for a given ticker."""
        if not (0 <= ticker < NUM_TICKERS):
            raise ValueError(f"Ticker ID must be between 0 and {NUM_TICKERS-1}")
        
        # Lock the ticker's order book to prevent race conditions
        with self.locks[ticker]:
            # If no orders to match, return early
            if not self.buy_orders[ticker] or not self.sell_orders[ticker]:
                return
            
            # O(n) approach: Compare the highest buy price with the lowest sell price
            # Keep matching until no more matches are possible
            while (self.buy_orders[ticker] and self.sell_orders[ticker] and 
                   self.buy_orders[ticker][0].price >= self.sell_orders[ticker][0].price):
                
                buy_order = self.buy_orders[ticker][0]
                sell_order = self.sell_orders[ticker][0]
                
                # Determine the quantity to trade
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = sell_order.price  # Use the sell price for the trade
                
                # Update order quantities
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                
                # Log the transaction
                transaction = {
                    'ticker': ticker,
                    'price': trade_price,
                    'quantity': trade_quantity,
                    'timestamp': time.time()
                }
                
                with self.log_lock:
                    self.transaction_log.append(transaction)
                
                # Remove orders that have been fully executed
                if buy_order.quantity == 0:
                    self.buy_orders[ticker].pop(0)
                
                if sell_order.quantity == 0:
                    self.sell_orders[ticker].pop(0)

# Simulation function to generate random orders
def simulate_trading(order_book, num_orders=1000, max_threads=10):
    def generate_random_orders(thread_id, orders_per_thread):
        for _ in range(orders_per_thread):
            order_type = random.choice([BUY, SELL])
            ticker = random.randint(0, NUM_TICKERS - 1)
            quantity = random.randint(1, 100)
            price = random.uniform(10.0, 1000.0)
            
            order_book.add_order(order_type, ticker, quantity, price)
            
            # Small sleep to simulate real-world timing
            time.sleep(random.uniform(0.001, 0.01))
    
    threads = []
    orders_per_thread = num_orders // max_threads
    
    # Create and start threads
    for i in range(max_threads):
        thread = threading.Thread(target=generate_random_orders, args=(i, orders_per_thread))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return order_book

# Function to display the status of the order book
def display_order_book_stats(order_book):
    total_buy_orders = sum(len(orders) for orders in order_book.buy_orders)
    total_sell_orders = sum(len(orders) for orders in order_book.sell_orders)
    total_transactions = len(order_book.transaction_log)
    
    print(f"Total buy orders: {total_buy_orders}")
    print(f"Total sell orders: {total_sell_orders}")
    print(f"Total transactions: {total_transactions}")
    
    # Display some sample transactions if available
    if order_book.transaction_log:
        print("\nSample transactions:")
        for i in range(min(5, len(order_book.transaction_log))):
            t = order_book.transaction_log[i]
            print(f"Ticker: {t['ticker']}, Quantity: {t['quantity']}, Price: {t['price']:.2f}")

# Main function to run the simulation
def main():
    order_book = OrderBook()
    
    print("Starting trading simulation...")
    start_time = time.time()
    
    # Run the simulation with 10,000 orders and 8 threads
    simulate_trading(order_book, num_orders=10000, max_threads=8)
    
    end_time = time.time()
    print(f"Simulation completed in {end_time - start_time:.2f} seconds")
    
    # Display statistics
    display_order_book_stats(order_book)

if __name__ == "__main__":
    main()
