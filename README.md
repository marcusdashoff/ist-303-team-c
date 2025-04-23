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
# then go to http://127.0.0.1:5000. You should be able to find login info in init_db.py seeding file. 

🚨 🚨 if you are receiving `unable to load module error`, you might neeed to reconfigure your python path, for example, by running `export PYTHONPATH=$PYTHONPATH:/Users/stone/src/ist-303-team-c` 

# run pytest
pytest

# run test coverage
pytest --cov=controllers --cov=main --cov=models --cov=jobs --cov-report=term-missing
```

# Test Coverage Data 
```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
controllers/__init__.py       0      0   100%
controllers/purchase.py      40      5    88%   60, 72-81
controllers/search.py        20      0   100%
controllers/sell.py          35      4    89%   62, 75-78
jobs/fulfillment.py          19      1    95%   56
main.py                      52      0   100%
models/__init__.py            0      0   100%
models/user.py               13      1    92%   10
-------------------------------------------------------
TOTAL                       179     11    94%
```


# Lessons Learned From This Project 
* 😏 **Be Ready for Surprises**: Some things took longer than we 
thought like using outside tools or APIs. It’s important to 
leave extra time in case things don’t go as planned.
* 😏 **Keep Code Organized**: Writing clean, separate pieces of 
code made it easier to test, fix problems, and add new 
features later.
* 😏 **Communicate Early and Often**: Checking in regularly as 
a team helped us stay on the same page, solve
problems quickly, and adjust our plan when needed.


# Project Repo Info
## Commit History
- [main branch commit history](https://github.com/marcusdashoff/ist-303-team-c/commits/main/)
## Contributors
- [contributors page](https://github.com/marcusdashoff/ist-303-team-c/graphs/contributors)
## Overall usage of github
- [Github Actions](https://github.com/marcusdashoff/ist-303-team-c/actions)
- [Github Issue](https://github.com/marcusdashoff/ist-303-team-c/issues)
- [Github Pull Requests](https://github.com/marcusdashoff/ist-303-team-c/pulls?q=is%3Apr+is%3Aclosed)

## Directory Structure
```
.
├── Part C
│   └── Part C Presentation.pptx
├── README.md
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-313.pyc
│   └── main.cpython-313.pyc
├── controllers
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── auth.cpython-313.pyc
│   │   ├── purchase.cpython-313.pyc
│   │   ├── search.cpython-313.pyc
│   │   └── sell.cpython-313.pyc
│   ├── purchase.py
│   ├── search.py
│   └── sell.py
├── database.db
├── helper
│   ├── CurrencyConversion.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── db_connector.cpython-313.pyc
│   └── db_connector.py
├── init_db.py
├── jobs
│   ├── __pycache__
│   │   └── fulfillment.cpython-313.pyc
│   └── fulfillment.py
├── main.py
├── models
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── user.cpython-313.pyc
│   └── user.py
├── requirements.txt
├── schema.sql
├── static
│   └── style.css
├── templates
│   ├── index.html
│   ├── login.html
│   ├── navigation.html
│   ├── purchase.html
│   ├── search.html
│   └── sell.html
└── tests
    ├── __pycache__
    │   ├── __init__.cpython-313.pyc
    │   ├── currency_converter.cpython-313.pyc
    │   ├── test_CurrencyConversion.cpython-313-pytest-8.3.5.pyc
    │   ├── test_fulfillment.cpython-313-pytest-8.3.5.pyc
    │   ├── test_main.cpython-313-pytest-8.3.5.pyc
    │   ├── test_purchase.cpython-313-pytest-8.3.5.pyc
    │   ├── test_search.cpython-313-pytest-8.3.4.pyc
    │   ├── test_search.cpython-313-pytest-8.3.5.pyc
    │   └── test_sell.cpython-313-pytest-8.3.5.pyc
    ├── currency_converter.py
    ├── database.db
    ├── test_CurrencyConversion.py
    ├── test_fulfillment.py
    ├── test_main.py
    ├── test_purchase.py
    ├── test_search.py
    └── test_sell.py

```

# Project Plan  

## Milestone 1
Story 1 + Story 2 + Story 3 + Story 4 + Story 5 + Story 6

### Iteration 1: 
Story 1 + Story 2 + Story 3
### Iteration 2: 
Story 4 + Story 5 + Story 6

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

#### 3/26/25 @ 6:00 in person

- Reviewed pytest in class

#### 3/30/25 @ 7:00 on Teams

- Reviewed stories
- Reviewed end of prior iteration
- Played Planning Poker

#### 4/9/25 @ 7:00 on Teams

- Reviewed Story 4

#### 4/13/25 @ 7:00 on Teams

- Reviewed story 5


#### 2/20/25 @ 7:00 on Teams

- Reviewed Story 6

#### 2/22/25 @ 7:30 on Teams

- Reviewed Presentation
