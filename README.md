# Financial-Helper

This application records a user's spending on Google Maps. This allows the user to see where they spend their money. The app also sends weekly emails with a transaction and balance summary.

### How it works
![trimmed financial advisor pictorial](https://user-images.githubusercontent.com/42727015/63906020-2c08a000-c9e4-11e9-8634-0c81660eb401.png)

The PLAID API obtains transaction information from your bank which is processed and sent through a AJAX POST request to be displayed on google maps.


### Installing
Python:
```
sudo pip3 install plaid
sudo pip3 install fpdf
sudo pip3 install flask 
sudo pip3 install opencage
```
API keys:
* Google api key from the [Google Developers Console](https://console.developers.google.com)
* [Opencage API key](https://opencagedata.com/api)

### Usage
Once the backend.py program is executed, webpage can be seen in the this local URL: http://127.0.0.1:5000/
Emails containing transaction information are sent once every week. 



### Financial-Helper in Action
![Timeline3](https://user-images.githubusercontent.com/42727015/63825362-893f1b80-c928-11e9-8c57-042a7e7e3987.gif)



