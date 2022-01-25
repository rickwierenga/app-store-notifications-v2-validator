# AppStore Notifications V2 Validator

Read and validate [App Store Server Notifications V2](https://developer.apple.com/documentation/appstoreservernotifications/app_store_server_notifications_v2).

## Usage

```py
import appstore_notifications_v2_validator as asn2
request_body = b'{"signedPayload":"eyJh .... "}'
try:
	data = asn2.parse(request_body)
except InvalidTokenError:
	pass
```

`data` is a dictionary:

```
{
  "notificationType": "SUBSCRIBED",
  "subtype": "RESUBSCRIBE",
  "notificationUUID": "00000000-0000-0000-0000-000000000000",
  "data": {
    "bundleId": "com.example.App",
    "bundleVersion": "1",
    "environment": "Sandbox",
    "signedTransactionInfo": {
      "transactionId": "0000000000000000",
      "originalTransactionId": "0000000000000000",
      "webOrderLineItemId": "0000000000000000",
      "bundleId": "com.example.App",
      "productId": "com.example.App.pro",
      "subscriptionGroupIdentifier": "00000000",
      "purchaseDate": 0000000000000,
      "originalPurchaseDate": 0000000000000,
      "expiresDate": 0000000000000,
      "quantity": 1,
      "type": "Auto-Renewable Subscription",
      "inAppOwnershipType": "PURCHASED",
      "signedDate": 000000000000
    },
    "signedRenewalInfo": {
      "originalTransactionId": "0000000000000000",
      "autoRenewProductId": "com.example.App.pro",
      "productId": "com.example.App.pro",
      "autoRenewStatus": 1,
      "signedDate": 0000000000000
    }
  },
  "version": "2.0"
}
```

---

&copy; 2022 Rick Wierenga

