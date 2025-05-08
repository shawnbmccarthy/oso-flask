#
# User represents both:
# 1. customer
# 2. vendor
#
global {
    roles = ["admin"];
}

actor User {}

# not built out in flask
resource Profile {
    permissions = ["view", "update", "archive", "request.delete", "delete"];
    roles = ["viewer"];

    relations = {
        owner: User
    };

    "viewer" if "owner";

    "delete" if global "admin";

    "update" if "owner";
    "archive" if "owner";
    "request.delete" if "owner";

    "view" if "viewer" or is_public(resource);
}

#
# a shopping cart should only be editable
# by the customer that created it
#
resource Cart {
    permissions = ["view", "update", "delete"];

    relations = {
        owner: User
    };

    "update" if "owner";
    "delete" if "owner";
    "view" if "owner" or is_public(resource);
}

#
# resource shop
#
resource Shop {
    permissions = [
        "view",
        "update",
        "create.product",
        "update.inventory",
        "deactivate",
        "archive",
        "request.delete"
    ];

    roles = ["admin", "staff"];

    relations = {
        owner: User
    };

    "admin" if "owner";
    "staff" if "admin";
    "admin" if global "admin";

    "request.delete" if "owner";
    "archive" if "owner";
    "deactivate" if "admin";
    "update" if "admin";
    "create.product" if "staff";

    "view" if "staff" or is_active(resource);
}

resource Product {
    permissions = ["view", "update", "delete", "archive", "deactivate"];
    roles = ["admin", "staff"];

    relations = {
        belongs_to: Shop
    };

    role if role on "belongs_to";

    "delete" if "admin";
    "update" if "staff";
    "archive" if "staff";
    "deactivate" if "staff";
    "view" if "staff" or is_active(resource);
}

test "user can edit their own cart, but view others public cart" {
    setup {
        has_relation(Cart{"c"}, "owner", User{"a"});
        has_relation(Cart{"d"}, "owner", User{"b"});
        is_public(Cart{"d"});
    }
    assert allow(User{"a"}, action:String, Cart{"c"}) iff
        action in ["delete", "update", "view"];

    assert allow(User{"b"}, action:String, Cart{"d"}) iff
        action in ["delete", "update", "view"];

    assert allow(User{"a"}, "view", Cart{"d"});
    assert_not allow(User{"a"}, "update", Cart{"d"});
}