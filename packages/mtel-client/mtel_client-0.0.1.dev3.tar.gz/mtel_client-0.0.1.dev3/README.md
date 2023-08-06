# Little library for getting info from Mtel.me (Montenegro) profile.

### How to use:
```python
from mtel_client.client import Profile

data = Profile(email='test@test.com', password="test")

data.user
data.balance
data.tariff
data.user_detail
```
That's it!

## How to get your balance
```
data.balance.value
```

## How to find out the expiration date of your tariff
```
data.tariff.balance.formattedExpiredDate
```