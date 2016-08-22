=============
Sale Scenario
=============

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax, set_tax_code
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install sale_fedicom::

    >>> Module = Model.get('ir.module')
    >>> sale_module, = Module.find([('name', '=', 'sale_fedicom')])
    >>> Module.install([sale_module.id], config.context)
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()
    >>> party = company.party

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> payable = accounts['payable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']
    >>> account_cash = accounts['cash']

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer', fedicom_user='xxxx',
    ...         fedicom_password='xxxx')
    >>> customer.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.cost_price = Decimal('5')
    >>> template.cost_price_method = 'fixed'
    >>> template.account_expense = expense
    >>> template.account_revenue = revenue
    >>> template.save()
    >>> product.template = template
    >>> product.code = '1234567'
    >>> product.save()
    >>> product2 = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.cost_price = Decimal('5')
    >>> template.cost_price_method = 'fixed'
    >>> template.account_expense = expense
    >>> template.account_revenue = revenue
    >>> template.save()
    >>> product2.template = template
    >>> product2.code = '2345678'
    >>> product2.save()

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> warehouse_loc, = Location.find([('code', '=', 'WH')])

Configure Fedicom::

    >>> FedicomConfiguration = Model.get('fedicom.configuration')
    >>> fedicom_config = FedicomConfiguration(1)
    >>> fedicom_config.warehouse = warehouse_loc
    >>> fedicom_config.save()

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create an Inventory::

    >>> Inventory = Model.get('stock.inventory')
    >>> InventoryLine = Model.get('stock.inventory.line')
    >>> Location = Model.get('stock.location')
    >>> storage, = Location.find([
    ...         ('code', '=', 'STO'),
    ...         ])
    >>> inventory = Inventory()
    >>> inventory.location = storage
    >>> inventory.save()
    >>> inventory_line = InventoryLine(product=product, inventory=inventory)
    >>> inventory_line.quantity = 10.0
    >>> inventory_line.expected_quantity = 0.0
    >>> inventory.save()
    >>> inventory_line.save()
    >>> inventory_line = InventoryLine(product=product2, inventory=inventory)
    >>> inventory_line.quantity = 10.0
    >>> inventory_line.expected_quantity = 0.0
    >>> inventory.save()
    >>> inventory_line.save()
    >>> Inventory.confirm([inventory.id], config.context)
    >>> inventory.state
    u'done'

Create sales from fedicom::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> Sale.process_order([],'1234','1234','FEDI', [], config.context)
    {'error': 'Incorrect Login User'}
    >>> Sale.process_order([],'xxxx','1234','FEDI', [], config.context)
    {'error': 'Incorrect Login User'}
    >>> products = [['1234567', 5]]
    >>> ret = Sale.process_order([],'xxxx','xxxx','FEDI', products,
    ...     config.context)

    >>> len(ret['missingStock']) == 0
    True
    >>> sale, = Sale.find([])
    >>> len(sale.lines) == 1
    True
    >>> len(sale.shipments) == 1
    True
    >>> sum(x.quantity for x in sale.moves) == 5
    True
    >>> sum(x.quantity for x in sale.lines) == 5
    True
    >>> sale.state
    u'processing'
    >>> sale.shipment_state
    u'waiting'
    >>> sale.shipments[0].state
    u'assigned'
    >>> products = [['1234567', 3], ['2345678', 2], ['2345678', 3]]
    >>> ret = Sale.process_order([],'xxxx','xxxx','FEDI2', products,
    ...     config.context)
    >>> len(ret['missingStock']) == 0
    True
    >>> sale = Sale(2)
    >>> len(sale.lines) == 3
    True
    >>> len(sale.shipments) == 1
    True
    >>> sum(x.quantity for x in sale.moves) == 8
    True
    >>> sum(x.quantity for x in sale.lines) == 8
    True
    >>> sale.state
    u'processing'
    >>> sale.shipment_state
    u'waiting'
    >>> sale.shipments[0].state
    u'assigned'

Test missing stocks::

    >>> products = [['1234567', 5], ['2345678', 5]]
    >>> ret = Sale.process_order([],'xxxx','xxxx','FEDI3', products,
    ...     config.context)
    >>> len(ret['missingStock']) == 1
    True
    >>> sum(x[1] for x in ret['missingStock']) == 3
    True
    >>> sale = Sale(3)
    >>> len(sale.lines) == 2
    True
    >>> len(sale.shipments) == 1
    True
    >>> sum(x.quantity for x in sale.moves) == 7
    True
    >>> sum(x.quantity for x in sale.lines) == 7
    True
    >>> sale.state
    u'processing'
    >>> sale.shipment_state
    u'waiting'
    >>> sale.shipments[0].state
    u'assigned'
    >>> products = [['1234567', 5], ['2345678', 5]]
    >>> ret = Sale.process_order([],'xxxx','xxxx','FEDI4', products,
    ...     config.context)
    >>> len(ret['missingStock']) == 2
    True
    >>> sum(x[1] for x in ret['missingStock']) == 10
    True
    >>> sales = Sale.find([('reference', '=', 'FEDI4')])
    >>> len(sales) == 0
    True
