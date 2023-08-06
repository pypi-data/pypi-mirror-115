errors_en = \
    {None: "Ok", "readTimeOut": "The request timed out",
     "requestException": "OOps: Something Else",
     "HTTPError":"Http Error",
     "connectionError": "Error Connecting",
        "badRequest": "Form validation errors occurred. See JSON errors "
                   "property for detailed information about errors.",
     "invalidChecksum": "Given total, cash and points fields don't correlate "
                        "with "
                        "company marketing settings in UDS.",
     "withdrawNotPermitted": "Method was called with participant → uid or "
                             "participant → phone parameter and points "
                             "field doesn't equal to 0.0.",
     "insufficientFunds": "Given points value is greater than actual "
                          "customer balance of points.",
     "discountLimitExceed": "Given points/total rate is more than allowed by "
                            "marketing settings.",
     "purchaseByPhoneDisabled": "Trying to make purchase by phone number "
                                "when it is disabled in company settings.",
     "participantIsBlocked": "Customer is blocked.",
     "goods.nodeIndex.invalid": "Specification of the identifier node_id to "
                                "create a category is not allowed",
     "goods.limitIsReached": "Quantity limit exceeded",
     "unauthorized": "API key or company id are incorrect.",
     "companyIsInactive": "Company is not active. Please renew the UDS "
                          "subscription",
     "notFound": "Customer with given code or ID is not found.",
     "goodsOrder.notFound": "Order with given ID is not found."}