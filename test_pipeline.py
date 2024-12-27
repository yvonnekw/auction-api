import time
import datetime

from tests.product import *
from tests.product.category import create_category
from tests.product.create_product import create_product

t0 = time.time()
create_category()
t1 = time.time()
print("Step 1: create_category test Done")
print("-----> Test completed in ", str(t1-t0), " seconds ", "\n")

t0 = time.time()
create_product()
t1 = time.time()
print("Step 1: create_product test Done")
print("-----> Test completed in ", str(t1-t0), " seconds ", "\n")
