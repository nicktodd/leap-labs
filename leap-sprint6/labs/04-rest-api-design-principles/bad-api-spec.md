# Existing API — "Order Management Service"

This is what a previous team built. It works — every endpoint here has been manually tested and
does what it claims. Your job in this lab is not to check whether it works; it's to critique
*how it's designed*.

| Method | URL | What it does |
|---|---|---|
| `GET` | `/getAllOrders` | Returns every order in the system |
| `GET` | `/getOrder?id=123` | Returns one order, by id |
| `POST` | `/createOrder` | Creates a new order, body contains the order details |
| `POST` | `/deleteOrder/123` | Deletes the order with id 123 |
| `GET` | `/updateOrderStatus?id=123&status=REJECTED` | Changes an order's status |
| `POST` | `/order` | Also creates an order — an older endpoint, kept for backward compatibility |
| `GET` | `/orders/123/getFee` | Returns the calculated fee for order 123 |

**Every endpoint returns HTTP 200**, including failures. The response body always has this
shape:

```json
{ "success": true, "data": { ... } }
```

or, on failure:

```json
{ "success": false, "error": "order not found" }
```

There is no `/v1/`, `/v2/`, or any other version marker anywhere — just the bare paths above.
There has never been a breaking change to this API, so versioning has never come up.
