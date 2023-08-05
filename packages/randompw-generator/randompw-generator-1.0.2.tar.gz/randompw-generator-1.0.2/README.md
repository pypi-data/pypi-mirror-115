# Random Password Generator

Python package to generate random passwords.

# Usage

* Install the package

```bash
pip install randompw-generator
```

* Import the package

```python
from rpg import RandomPassword
```

* Create an instance of the RandomPassword and generate password

```python
pw = RandomPassword()
pw.generate()
```

# Configuration

The default length of the password is 15, it can be changed at the time of instantiation.

```python
# It will generate a password of the length of 20
pw = RandomPassword(20)
pw.generate()
```

Length can also be increased by specifying the number of each type of character.

example :

```python
pw = RandomPassword()

# Set the number of lowercase character to 10.
pw.set_lower(10)

# Set the number of lowercase character to 9.
pw.set_upper(9)

# Set the number of lowercase character to 3.
pw.set_digits(3)

# Set the number of lowercase character to 4.
pw.set_spchars(4)

# It'll generate a password contaning 10 lowercase
# 9 upppercase, 3 digits and 4 special characters.
pw.generate()
``` 