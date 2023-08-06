## Selenium-recaptcha-solver

This package is used to solve recaptcha challenges when 
using a Selenium web driver for web automation tasks.

## Requirements 

Python 3.7+

Main dependencies:
  <ul>
    <li>SpeechRecognition python package to transcribe speech</li>
    <li>Pydub for file conversions</li>
</ul>

## Installation

```bash
python -m pip install selenium-recaptcha-solver
```

## Usage

```python
from selenium_recaptcha_solver import API
from selenium import webdriver

# Example driver, the API works for any browser
driver = webdriver.Chrome()

# Create API object and bind it to your webdriver
api_client = API(driver=driver)

# Fetch random web page
driver.get('https://foo.bar.com')

# Get example iframe web element
iframe = driver.find_element(
    by='insert-your-locator-here', 
    value='insert-captcha-iframe-here',
)

# Solve Captcha using API
api_client.solve_recaptcha_v2(iframe=iframe)

# Write the rest of your operations to do after solving the Captcha
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
