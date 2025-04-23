#
# User represents both:
# 1. customer
# 2. vendor
#
actor User {}

#
# a shopping cart should only be editable
# by the customer that created it
#
resource ShoppingCart {}

#
# resource shop
#