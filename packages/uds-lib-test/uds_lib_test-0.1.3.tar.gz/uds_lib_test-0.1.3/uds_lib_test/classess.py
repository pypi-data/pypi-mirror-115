from typing import List

class Error:
    """docstring"""

    def __init__(
            self,
            error_code: str,
            error_message: str,
            error_description: str
    ):
        """Constructor"""
        self.error_code = error_code
        self.error_message = error_message
        self.error_description = error_description


class Response:
    """docstring"""

    def __init__(
            self,
            status_code:int,
            response_data:object,
            response_headers: object,
            error_info: Error
    ):
        """Constructor"""
        self.status_code = status_code
        self.response_data = response_data
        self.response_headers = response_headers
        self.error_info = error_info


class TotalCashSpent:
    """
    Upgrade status when customer reaches that amount of cash spent.
        target (number) - Amount of cash spent.
    """

    def __init__(
            self,
            target: float = None
    ):
        """Constructor"""
        self.target = target


class EffectiveInvitedCount:
    """
    Upgrade to tier when customer reaches target of invited count.
        target - Amount of invited count.
    """

    def __init__(
            self,
            target: float = None
    ):
        """Constructor"""
        self.target = target


class Condition:
    """
    Conditions to upgrade customer's status automatically.
        total_cash_spent - Upgrade status when customer reaches that amount of cash spent.
        effective_invited_count - Upgrade to tier when customer reaches target of invited count.
     """

    def __init__(
            self,
            total_cash_spent: TotalCashSpent = None,
            effective_invited_count: EffectiveInvitedCount = None
    ):
        """Constructor"""
        self.total_cash_spent = total_cash_spent
        self.effective_invited_count = effective_invited_count


class MembershipTier:
    """
    Status settings.
        uid	- Status UID.
        name - Status name.
        rate -  Status rate.
        conditions - Conditions to upgrade customer's status automatically.
    """

    def __init__(
            self,
            uid: str,
            name: str,
            rate: float,
            condition: Condition = None
    ):
        """Constructor"""
        self.uid = uid
        self.name = name
        self.rate = rate
        self.condition = condition


class ListMembershipTiers:
    """
    List of statuses.
        membership_tiers_list - Status settings.
    """

    def __init__(self, *membership_tiers_list: List[MembershipTier]):
        """Constructor."""
        self.membership_tiers_list = []
        for tier_data in membership_tiers_list:

            self.membership_tiers_list.append(MembershipTier(
                uid=tier_data.get('uid'),
                name=tier_data.get('name'),
                rate=tier_data.get('rate'),
                condition=Condition(total_cash_spent=TotalCashSpent(target= tier_data.get('conditions').get('totalCashSpent').get('target'))
                                    if tier_data.get('conditions').get('totalCashSpent') else None,
                                    effective_invited_count = EffectiveInvitedCount(target= tier_data.get('conditions').get('totalCashSpent').get('target'))
                                    if tier_data.get('conditions').get('effectiveInvitedCount') else None)
            ))


class LoyaltyProgramSettings:
    """
    General loyalty program settings of the company.
        base_membership_tier - Base status settings.
        membership_tiers - List of statuses settings.
        max_scores_discount - Maximum discount (as a percentage) allowed for redeeming points.
        referral_cashback_rates - Referral cashback rates (3 levels as a percentage).
        cashier_award - Cashier’s reward rate for the performed transaction.
        referral_reward - Customer’s reward for an effective recommendation.
        receipt_limit - Maximum transaction amount that can be made through UDS Cashier.
        defer_points_for_days - Term (in days) to accrue deferred points.
    """

    def __init__(
            self,
            max_scores_discount: float,
            referral_cashback_rates: list,
            cashier_award: float,
            referral_reward: float,
            receipt_limit: float,
            defer_points_for_days: float,
            base_membership_tier: MembershipTier,
            membership_tiers: ListMembershipTiers
    ):
        """Constructor"""
        self.max_scores_discount = max_scores_discount
        self.referral_cashback_rates = referral_cashback_rates
        self.cashier_award = cashier_award
        self.referral_reward = referral_reward
        self.receipt_limit = receipt_limit
        self.defer_points_for_days = defer_points_for_days
        self.base_membership_tier = base_membership_tier
        self.membership_tiers = membership_tiers


class CustomerShortInfo:
    """Customer short information.
        id - Customer ID in the company.
        display_name	- Customer name.
        uid	- Customer UID in the UDS.
        membership_tier - Status settings.
    """

    def __init__(self,
                 id: int,
                 display_name: str,
                 uid: str,
                 membership_tier=MembershipTier
                 ):
        """Constructor"""
        self.id = id
        self.display_name = display_name
        self.uid = uid
        self.membership_tier = membership_tier


class CashierShortInfo:
    """Cashier information.
        id - Cashier ID in the UDS.
        display_name - Cashier name.
"""

    def __init__(self,
                 id: int,
                 display_name: str
                 ):
        """Constructor"""
        self.id = id
        self.display_name = display_name


class BranchShortInfo:
    """Branch information.
        id	- Branch ID in the UDS.
        display_name - Branch name."""

    def __init__(self,
                 id: int,
                 display_name: str
                 ):
        """Constructor"""
        self.id = id
        self.display_name = display_name


class Company:
    """
    Company settings.
        id - Company ID.
        name - Company name.
        promo_code - Company promo code for customers to join.
        currency - Currency in ISO-4217 format.
        base_discount_policy - Enum: "APPLY_DISCOUNT" "CHARGE_SCORES"
            Defines loyalty program type:
            APPLY_DISCOUNT — apply a discount to an order;
            CHARGE_SCORES — customer will receive points award (cashback).
        loyalty_program_settings - General loyalty program settings of the company.
        purchase_by_phone - Permission to make purchases by phone number.
        write_invoice - Necessity to indicate a bill number when performing transactions through UDS Cashier.
        burn_points_on_purchase - Feature of deduction of points during perfomance of transactions.
        burn_points_on_price - Feature of deduction of points during execution of orders.
        slug - The domain name that appears in the link to your company's web page.
    """

    def __init__(
            self,

            id: int,
            name: str,
            promo_code: str,
            currency: str,
            base_discount_policy: str,
            purchase_by_phone: bool,
            write_invoice: bool,
            burn_points_on_purchase: bool,
            burn_points_on_price: bool,
            slug: str,
            loyalty_program_settings: LoyaltyProgramSettings

    ):
        """Constructor"""

        self.id = id
        self.name = name
        self.promo_code = promo_code
        self.currency = currency
        self.base_discount_policy = base_discount_policy
        self.purchase_by_phone = purchase_by_phone
        self.write_invoice = write_invoice
        self.burn_points_on_purchase = burn_points_on_purchase
        self.burn_points_on_price = burn_points_on_price
        self.slug = slug
        self.loyalty_program_settings = loyalty_program_settings



class Transaction:
    """
    Transaction information.
        id - Transaction ID in the UDS.
        date_created - Transaction date.
        action - Transaction type.
        state - Transaction status.
         Enum: "NORMAL", "CANCELED", "REVERSAL"
        customer - Customer information.
        cashier	 - Cashier information.
        branch - Branch information.
        points - Number of points that will be deducted from the customer's balance when a transaction is completed. A negative value indicates deduction of points, and a positive value indicates accrual of points.
        receipt_number - Bill number.
        origin - Reference to initial transaction (for transactions in state REVERSAL).
        total - Total bill amount without discount.
        cash - Payment amount (in currency units).
    """

    def __init__(self,

                 id: int,
                 date_created: str,
                 action: str,
                 state: str,
                 points: float,
                 cash: float,
                 total: float,
                 receipt_number: str,
                 origin: object,
                 customer: CustomerShortInfo,
                 cashier: CashierShortInfo,
                 branch: BranchShortInfo
                 ):
        """Constructor"""

        self.id = id
        self.date_created = date_created
        self.action = action
        self.state = state
        self.customer = customer
        self.cashier = cashier
        self.branch = branch
        self.points = points
        self.receipt_number = receipt_number
        self.origin = origin
        self.total = total
        self.cash = cash


class ListTransactions:
    """
    List of transactions.
    transactions - transaction information.
    """

    def __init__(self, *transactions: List[Transaction]):
        """Constructor."""
        self.transactions = transactions


class Participant:
    """
    Customer details.
        id - Customer ID in the company.
        inviter_id - ID of the inviting user in the company.
        points - Points available.
        discount_rate - Discount rate (as a percentage).
        cashback_rate - Cashback rate (as a percentage) for this UDS user.
        membership_tier - Status settings.
        date_created - Date when the customer joined the company.
        last_transaction_time - Date and time when the customer made the last transaction.
        birth_date - Customer birth date.
"""

    def __init__(self,
                 id: int,
                 inviter_id: int,
                 points: float,
                 discount_rate: float,
                 cashback_rate: float,
                 date_created: str,
                 last_transaction_time: str,
                 birth_date: str,
                 membership_tier: MembershipTier
                 ):
        """Constructor"""
        self.id = id
        self.inviter_id = inviter_id
        self.points = points
        self.discount_rate = discount_rate
        self.cashback_rate = cashback_rate
        self.membership_tier = membership_tier
        self.date_created = date_created
        self.last_transaction_time = last_transaction_time
        self.birth_date = birth_date


class Customer:
    """
    Customer information.
        uid	- Customer UID in the UDS.
        avatar	- URL of user profile picture.
        display_name	- Customer name.
        gender	- Gender.
            Enum: "MALE", "FEMALE", "NOT_SPECIFIED"
        phone	- Customer phone number.
        participant	- Customer details.
        """

    def __init__(self,

                 uid: str,
                 avatar: str,
                 display_name: str,
                 gender: str,
                 phone: str,
                 participant: Participant
                 ):
        """Constructor"""

        self.uid = uid
        self.avatar = avatar
        self.display_name = display_name
        self.gender = gender
        self.phone = phone
        self.participant = participant
        # self.code = code


class CustomerPurchase:
    """
    Operation information.
        max_points - Maximum number of points available.
        total - Total bill (in currency units).
        skip_loyalty_total - A part of the bill amount for which cashback is not credited and to which the discount does not apply (in currency units).
        discount_amount - Discount amount (in currency units).
        discount_percent - Discount rate (as a percentage).
        points - Payable points.
        points_percent - Discount rate due to points (as a percentage).
        net_discount	- Total discount amount (in currency unit).
        net_discount_percent - Total discount rate (as a percentage of the total bill).
        cash - Payable amount (in currency units).
        cash_total - The total amount to be paid including extras (delivery), in currency units.
        cash_back - Reward (cashback) that will be accrued after transaction completion (in points).
        extras - Additional payments will not be taken into account by the loyalty program."""

    def __init__(self,
                 max_points: float,
                 total: float,
                 skip_loyalty_total: float,
                 discount_amount: float,
                 discount_percent: float,
                 points: float,
                 points_percent: float,
                 net_discount: float,
                 net_discount_percent: float,
                 cash: float,
                 cash_total: float,
                 cash_back: float,
                 extras: object,
                 ):
        """Constructor"""
        self.max_points = max_points
        self.total = total
        self.skip_loyalty_total = skip_loyalty_total
        self.discount_amount = discount_amount
        self.discount_percent = discount_percent
        self.points = points
        self.points_percent = points_percent
        self.net_discount = net_discount
        self.net_discount_percent = net_discount_percent
        self.cash = cash
        self.cash_total = cash_total
        self.cash_back = cash_back
        self.extras = extras


class ListCustomers:
    """
    List of customers.
    customers - customer information
    """

    def __init__(self, *customers: List[Customer]):
        """Constructor."""
        self.customers = customers


class CustomerPurchaseCalc:
    """
    Information on available points for deduction or discount rate (
    depending on bonus program settings), payable amount after applying
    discounts/rewards and number of points that will be accrued after
    transaction.
        user - Customer information.
        code - New long-term payment
        promo code for method Find customer, if exchangeCode queried.
        purchase - Operation information.
    """

    def __init__(self,
                 user: Customer = None,
                 code: str = None,
                 purchase: CustomerPurchase = None
                 ):
        """Constructor"""
        self.user = user
        self.code = code
        self.purchase = purchase


class GoodsOffer:
    """Promotional information.
        offer_price - Discount price.
        skip_loyalty	- Flag of goods item price which cashback is not credited
        and to which the discount does not apply (in currency units).
    """

    def __init__(
            self,
            offer_price: float,
            skip_loyalty: bool
    ):
        """Constructor"""
        self.offer_price = offer_price
        self.skip_loyalty = skip_loyalty

class GoodsInventory:
    """
    Item quantity in stock.
        inStock	- Item quantity. The "null" value means unlimited quantity.
    """

    def __init__(
            self,
            in_stock: int
    ):
        """Constructor"""
        self.in_stock = in_stock


class Variant:
    """
    Variant of item.
        name - Variant name.
        sku - Variant stock number.
        price - Variant price.
        offer - Promotional information.
        inventory - Item quantity in stock.
    """

    def __init__(
            self,
            name: str,
            sku: str,
            price: float,
            offer: GoodsOffer,
            inventory: GoodsInventory

    ):
        """Constructor"""
        self.name = name
        self.sku = sku
        self.price = price
        self.offer = offer
        self.inventory = inventory


class ListVariants:
    """
    List of variants.
    variants - variant information.
    """

    def __init__(self, *variants: List[Variant]):
        """Constructor."""
        self.variants = []
        for variant in variants:
            self.variants.append(Variant(
                sku=variant.get('sku'),
                name=variant.get('name'),
                price=variant.get('price'),
                offer=GoodsOffer(
                    offer_price=variant.get('offer').get('offerPrice'),
                    skip_loyalty=variant.get('offer').get('skipLoyalty'))
                if variant.get('offer') else None,
                inventory=GoodsInventory(
                    in_stock=variant.get('inventory').get('inStock'))
                if variant.get('inventory') else None

            ))


class VaryingItem:
    """
    Item with variants information
        name - Goods name.
        id	- Goods ID in the UDS.
        external_id	- External goods idetifier.
        hidden - Is the goods hidden.
        blocked	- Is the goods blocked.
        description	- Variant description.
        type -  VARYING_ITEM
        variants - Variants of item.
"""

    def __init__(
            self,
            name: str,
            id: int,
            external_id: str,
            hidden: bool,
            blocked: bool,
            description: str,
            type: str,
            variants: ListVariants
    ):
        """Constructor"""
        self.name = name
        self.id = id
        self.external_id = external_id
        self.type = type
        self.hidden = hidden
        self.blocked = blocked
        self.variants = variants
        self.description = description



class Category:
    """
    Category information
        name - category name.
        id	- category ID in the UDS.
        external_id	- External category idetifier.
        hidden - Is the category hidden.
        blocked	- Is the category blocked.
        type -  CATEGORY.
    """

    def __init__(
            self,
            name: str,
            id: int,
            external_id: str,
            hidden: bool,
            blocked: bool,
            type: str

    ):
        """Constructor"""
        self.name = name
        self.id = id
        self.external_id = external_id
        self.type = type
        self.hidden = hidden
        self.blocked = blocked

class Item:
    """
    Item information
        id - Goods ID in the UDS.
        name - Goods name.
        externalId - External goods idetifier.
        hidden - Is the goods hidden.
        blocked - Is the goods blocked.
        type - ITEM
        sku - Item stock number.
        price - Item price.
        description	- Item description.
        offer - Promotional information.
        inventory - Item quantity in stock.
"""

    def __init__(
            self,
            name: str,
            id: int,
            external_id: str,
            hidden: bool,
            blocked: bool,
            type: str,
            description: str,
            sku: str,
            price: float,
            offer: GoodsOffer,
            inventory: GoodsInventory
    ):
        """Constructor"""
        self.name = name
        self.id = id
        self.external_id = external_id
        self.type = type
        self.hidden = hidden
        self.blocked = blocked
        self.price = price
        self.description = description
        self.sku = sku
        self.offer = offer
        self.inventory = inventory


class DeliveryCase:
    """
    Delivery information.
        name - Delivery name.
        value - Cost of delivery.
    """

    def __init__(
            self,
            name: str,
            value: float):
        """Constructor"""
        self.name = name
        self.value = value


class DeliveryTypes:
    """
    Method of receiving the order.
        type - Type of receiving the order.
        address - Delivery address.
        branch - Branch information.
        delivery - Delivery information.

    """
    def __init__(
            self,
            type: str,
            address: str,
            branch: BranchShortInfo,
            delivery: DeliveryCase
    ):
        """Constructor"""
        self.type = type
        self.branch = branch
        self.delivery = delivery
        self.address = address


class DeliveryType:
    """
    Information of receiving the order .
        receiver_name - Name of the customer who will receive the order.
        receiver_phone - Phone number of the customer who will receive
        the order.
        user_comment - Customer comment on the order.
        type - Method of receiving the order.
    """

    def __init__(
            self,
            receiver_name: str,
            receiver_phone: str,
            user_comment: str,
            type: DeliveryTypes
    ):
        """Constructor"""
        self.receiver_name = receiver_name
        self.receiver_phone = receiver_phone
        self.user_comment = user_comment
        self.type = type


class OnlinePayment:
    """
    Online payment information.
        payment_provider - Payment provider type.
            Enum: "B2P", "CLOUD_PAYMENTS", "CUSTOM"
        id - Payment identifier in external payment system.
        completed - Payment status.
"""

    def __init__(
            self,
            payment_provider: str,
            id: str,
            completed: bool
    ):
        """Constructor"""
        self.payment_provider = payment_provider
        self.id = id
        self.completed = completed


class PaymentMethod:
    """
    Payment information.
        type - Payment type.
          Enum: "BEST_TO_PAY", "CLOUD_PAYMENTS", "CASH", "MANUAL", "CUSTOM"
        name - Name for custom payment method with type MANUAL.
"""

    def __init__(
            self,
            type: str,
            name: str
    ):
        """Constructor"""
        self.type = type
        self.name = name


class OrderItem:
    """
    Item information.
        id - Item ID in the UDS.
        external_id - External item identifier.
        name - Item name.
        variant_name - Name of the item option, if the type of this item is VARYING_ITEM.
        sku - Item stock number.
        type - Item type.
            Enum: "ITEM" "VARYING_ITEM"
        qty - Quantity.
        price - Item price.
        """

    def __init__(
            self,
            id: int,
            name: str,
            external_id: str,
            variant_name: str,
            sku: str,
            type: str,
            qty: int,
            price: float

    ):
        """Constructor"""
        self.id = id
        self.name = name
        self.external_id = external_id
        self.variant_name = variant_name
        self.sku = sku
        self.type = type
        self.qty = qty
        self.price = price



class ListOrderItems:
    """
    List of items in order.
        items - item information.
    """

    def __init__(self, *items: List[OrderItem]):
        """Constructor."""
        self.items = []
        for item in items:
            self.items.append(OrderItem(
                id=item.get('id'),
                external_id=item.get('externalId'),
                variant_name=item.get('variantName'),
                name=item.get('name'),
                sku=item.get('sku'),
                type=item.get('type'),
                qty=item.get('qty'),
                price=item.get('price'),
            ))

class Order:
    """
    Order information.
        id - Order ID in the UDS.
        date_created - Order date.
        comment - Comment on the order.
        state - Order status.
          Enum: "NEW",  "COMPLETED", "DELETED", "WAITING_PAYMENT"
        cash - Amount payable in currency units.
        points - Number of deducted points.
        total - Total order amount.
        certificate_points - Number of deducted certificate points.
        customer - Customer information.
        delivery - Method of receiving the order.
        online_payment - Online payment information.
        payment_method - Payment information.
        items - Items information.
    """

    def __init__(
            self,
            id: int,
            date_created: str,
            comment: str,
            state: str,
            cash: float,
            points: float,
            total: float,
            certificate_points: float,
            customer: CustomerShortInfo,
            delivery: DeliveryType,
            payment_method: PaymentMethod,
            online_payment: OnlinePayment,
            items: ListOrderItems
    ):
        """Constructor"""
        self.id = id
        self.date_created = date_created
        self.comment = comment
        self.state = state
        self.cash = cash
        self.points = points
        self.total = total
        self.certificate_points = certificate_points
        self.customer = customer
        self.delivery = delivery
        self.payment_method = payment_method
        self.online_payment = online_payment
        self.items = items



class Voucher:
    """
    Voucher information.
        code	- UDS voucher code.
        qrCodeText - UDS voucher info for qrcode.
        qrCode64 - Link for generate qrcode image (size 64).
        qrCode128 - Link for generate qrcode image (size 128).
        qrCode256 - Link for generate qrcode image (size 256)
        expiresIn - Voucher code expires in (UTC time-zone).
        points - Minimum points for withdrawal.
    """

    def __init__(
            self,
            code: str,
            qr_code_text: str,
            expires_in: str,
            qr_code_128: str,
            qr_code_256: str,
            points: str,

    ):
        """Constructor"""
        self.code = code
        self.qr_code_text = qr_code_text
        self.expires_in = expires_in
        self.qr_code_128 = qr_code_128
        self.qr_code_256 = qr_code_256
        self.points = points

