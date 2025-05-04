# Oso Workshop

This project represents the very basics of a marketplace shopping cart. A lot of 
features are not implemented.

For this workshop the exercise will include:
1. **integrate Oso into shopping cart**: make use of Oso to support viewing public carts
   and editing only our own carts
2. **integrate Oso into shops**: use Oso to determine the set of permissions we have based
   on our user id.
3. **query interface**: make use of our Oso actions api, query builder api's to run rich
   queries to determine access
4. **local authorization**: Optional, use Oso local authorization to determine access
5. **global admin**: Optional, adding global admins for managing 
6. **user profile**: Optional, create a user profile route based on the policy

## Shopping Cart

A shopping cart is owned by a user, products from any shop can be added to a shopping cart.
Shopping carts can be publicly viewed if they are marked as such so that any user can 
The rules (see [policy.polar](./authorization/policy.polar))

1. A user should be able to see all their carts and public carts
   1. using [`oso.list`](https://www.osohq.com/docs/app-integration/client-apis/python#list-centralized]%20[#list-centralized) we can return a list of objects 
2. A user should be able to update their own carts

## Shop

A user can own one more more shops, and a shop can have one or more staff members.



