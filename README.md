# Stock Trading App - Team Project

## Team Members

- Eman Alzahrani
- Marcus Dashoff
- Raymond Derrick Dimla
- James Hah
- Chen Zhu

## Project Concept

We are developing a simple stock trading app that allows users to:
- Buy and sell stocks
- View their portfolio
- Cancel unfulfilled orders
- Analyze stock market trends with easy-to-read graphs

The app will provide:
- Real-time stock price updates
- Market trends
- News
- Historical performance data

Additional features include:
- Currency conversion
- Tracking market opening and closing times for various global markets

# How to Run

```
# init virtual env
python3 -m venv venv

# run vierutal env
source venv/bin/activate

# install dependencies
pip install -r requirements.txt 

# initialize database
python init_db.py

# run app
flask --app main.py run --debug

# if you are receiving `unable to load module error`, you might neeed to reconfigure your python path, 
# for example, by running `export PYTHONPATH=$PYTHONPATH:/Users/stone/src/ist-303-team-c` 

# run pytest
pytest

# run test coverage
pytest --cov=controllers --cov=main --cov=models --cov=jobs --cov-report=term-missing
```


# Project Plan  

## Milestone 1
Story 1 + Story 2 + Story 3


## 1. Project Kickoff (Basics V.1) - Chen  
- **User DB Table Setup**  
  - `user (id, email, balance, password)`  
- **Stock Trade DB Table Design and Setup**  
  - Stock Schema: `stock (id, ticker, full_name)`  
  - Purchase & Sell Schema:  
    - `purchase (id, user_id, stock_id, price, datetime, fulfilled_by_id, is_canceled)`  
    - `sell (id, user_id, stock_id, price, datetime, fulfilled_by_id, is_canceled)`  
- **User Authentication**  
  - User login with session setting  
  - User logout with session unsetting  
- **Navigation Setup**  
  - Page tabs: **Main, Sell, Buy, Info**  

## 2. Stock Search and Display (Basics V.1) - Marcus  
- **Info Page Features**  
  - Search box with submit button (user enters ticker and clicks submit)  
  - Stock info page (using stock ID as parameter)  
    - DB query search  
    - Show last price  
    - Show highest historical price  
    - Show lowest historical price  
    - Trade volume within the past 24 hours  
    - *(More details to be added in later iterations)*  
  - Refresh button *(low priority)*  

## 3. Buy Order (Basics V.1.5~2.0) - James  
- **Purchase Page Features**  
  - Input fields: stock symbol, shares, price  
  - Submit button  
  - Database call: Create multiple purchase entries & insert into DB  
  - *(Fulfillment logic will be added later)*  
- **Cancel Purchase Order**  
  - Display unfulfilled purchase orders with a `Cancel` button  
  - Clicking `Cancel` removes the entry from the `purchase` table  

## 4. Sell Order (Basics V.1.5~2.0) - James  
- **Sell Page Features**  
  - Input fields: stock symbol, shares, price  
  - Submit button  
  - Database call: Create multiple sell entries & insert into DB  
  - *(Fulfillment logic will be added later)*  
- **Cancel Sell Order**  
  - Display unfulfilled sell orders with a `Cancel` button  
  - Clicking `Cancel` removes the entry from the `sell` table  

## 5. Order Fulfillment Logic (Basics V.3) - Eman
- **User Stock DB Table Setup**  
  - `user_stock (user_id, stock_id, shares)`  
- **Order Processing**  
  - When a purchase/sell order is created, perform:  
    - Order search & fulfillment  
    - `Upsert` user stock shares count  

## 6. Order History and Portfolio Performance (Basics V.3) - Eman
- **Main Page Features**  
  - List of past fulfilled transactions  
  - Display user’s current balance  
  - Display user’s current stock holdings  

## 7. User Portfolio Performance Trend *(Low Priority - Future Iterations)*  - Raymond
- Algorithm to calculate daily performance per stock  
- Use user’s stock holdings to calculate total performance  

## 8. Stock Graph and Market News *(Low Priority - Future Iterations)*  
- **Stock Graph**  
- **Market News** *(Pending decision on external API usage)*  
- Add to the Main Page  

## 9. Currency Conversion *(Low Priority - Future Iterations)*  - Raymond
- If an external API is needed, defer until after core functionalities are completed  

## 10. Market Open/Close Times *(Low Priority - Future Iterations)*  - Marcus
- If an external API is needed, defer until after core functionalities are completed  

---

## Additional Tasks  

### 1. Burndown Chart  
- Track team progress  
- [Burndown Chart Link](https://cgu0-my.sharepoint.com/:x:/g/personal/marcus_dashoff_cgu_edu/EcCni_jThsBJvpLt8faw6WsBARXbuQ9OJch2m55Aj7UJOA?e=T1mGGv)  
- Reference: *Head First Software Development* by Pilone & Miles (p. 104)  

### 2. Stand-Up Meeting Evidence (GitHub Documentation)  
#### 2/14/25 @ 7:30 on Zoom  
- Parsed out stories  
- Partially filled out burndown chart  
- Set next meeting time/date  

#### 2/19/25 @ 6:30 @ CGU  
- Reviewed and assigned more stories  
- Set next meeting time/date  

#### 2/23/25 @ 7:30 on Teams  
- Broke down stories into tasks  
- Created burndown chart  
- Assigned members tasks and deliverables  
