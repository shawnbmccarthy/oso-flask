# Oso Workshop

This project represents the very basics of a marketplace shopping cart. A lot of 
features are not implemented.

Every REST call (except /api/v1/users) requires a request arg called uid, which represents
the users uuid. Typically we would use JWT tokens or other mechanisms as needed.

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

All code changes will occur in [carts.py](./oso_demo/routes/carts.py)

### Exercise 1: list all authorized carts

A user should be able to see all their carts and public carts, this is an example of using 
list api's to ask what we have access to.

using [`oso.list`](https://www.osohq.com/docs/app-integration/client-apis/python#list-centralized]%20[#list-centralized) 
we can return a list of carts that the user is allowed to see, edit the `get_all_users` function in
[users.py](./oso_demo/routes/users.py).

* Use the oso client, found in the current_app context (`current_app.oso`)
* oso.list will return a list of uid strings
* these strings can be used as a filter to sqlalchemy filter

### Exercise 2: create a cart

all users can create a cart; when a cart is created, at least one fact needs to be written to Oso. A `has_relation` 
triplet in the form of (`Cart`, `"owner"`, `User`) and if the cart is public, we need to also write an `is_public`
rule to Oso.

To see examples of these facts run this from the command line:

```
# all has_relation rules
oso-cloud get has_relation _ _ _ 

# query all cart owners
oso-cloud query has_relation Cart:_ "owner" User:_

# all public carts
oso-cloud query is_public Cart:_
```

Get will simply retrieve all facts stored in the development server, while query will use the policy to derive facts

### Exercise 3: read a users cart

In this exercise we will use `authorize` to ensure the user is allowed to read the requested cart, if not we should 
return unauthorized to the user

**reference**: [authorize](https://www.osohq.com/docs/app-integration/client-apis/python#authorize-centralized)

### Exercise 4: delete a cart

In this exercise we need to delete the cart from the database, we need to first ensure the user is authorized to 
delete the cart, then once the cart is removed from the database we need to remove 1 or more facts for the user.

* authorize to valid user can indeed delete cart
* delete cart from database (filtered appropriately)
* remove oso facts

### Exercise 5: get all items in a cart

This exercise is similar to `Exercise 1` for items

### Exercise 6: add item to cart

This exercise is similar to `Exercise 2`, but we are adding a
product to the cart

### Exercise 7:

This exercise is similar to `Exercise 2`, but we are removing an item from the cart

## Shop

A user can own one or more shops, and a shop can have one or more staff members, products
belong to shops and can be added to and managed by both staff and owners.

Shops and products are marked active using the is_active fact and anyone can view a shop or
product if it is active.

The rules for `Shop` and `Product` can be seen in [policy.polar](./authorization/policy.polar)

All code changes will occur in [shops.py](./oso_demo/routes/shops.py)

### Exercise 1: list all active shops

This is similar to exercise 1 in shops

### Exercise 2: create a shop

This is similar to exercise 2 in shops

### Exercise 3: get all active products for all active shops

For this exercise, could we use the query builder to get a list of all active products across all active shops?

## Global Admin

Oso supports roles that can span the entire application, this is called [global roles](https://www.osohq.com/docs/modeling-in-polar/role-based-access-control-rbac/globalroles)
which can be used for global admins. 

### Exercise 1: What global admin use cases can we think of?

Lets think of some global admin use cases and implement them.

## Query Interface

Oso provides a rich query interface that allows for complex evaluation of policies to determine things like:
1. what carts can a use view: `oso-cloud query User:<UID> "view" Cart:_`
2. what permissions do all users have access to a cart: `oso-cloud query User:_ _ Cart:<CART_ID>`

The [query builder](https://www.osohq.com/docs/app-integration/client-apis/python#method-build-query) interface makes 
use of the policy to list derived information about any rule in the policy.

## Local Authorization

[Local authorization](https://www.osohq.com/docs/authorization-data/local-authorization) allows oso to make decisions 
based on data stored in the applications local database. Oso never reads the data, Oso only needs to understand the 
structure.

As Oso evaluates the policy, a data-bindings file is sent to oso describing the SQL queries that need to execute to 
make the authorization decision. These bindings are then used to create complex filters that are then passed to the 
database using the applications ORM.

