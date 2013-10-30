=============
Sale Scenario
=============

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> today = datetime.date.today()

Create database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install sale::

    >>> Module = Model.get('ir.module.module')
    >>> sale_module, = Module.find([('name', '=', 'sale_fedicom')])
    >>> Module.install([sale_module.id], config.context)
    >>> Wizard('ir.module.module.install_upgrade').execute('upgrade')

Create company::

    >>> Currency = Model.get('currency.currency')
    >>> CurrencyRate = Model.get('currency.currency.rate')
    >>> currencies = Currency.find([('code', '=', 'EUR')])
    >>> if not currencies:
    ...     currency = Currency(name='Euro', symbol=u'€', code='EUR',
    ...         rounding=Decimal('0.01'), mon_grouping='[3, 3, 0]',
    ...         mon_decimal_point=',')
    ...     currency.save()
    ...     CurrencyRate(date=today + relativedelta(month=1, day=1),
    ...         rate=Decimal('1.0'), currency=currency).save()
    ... else:
    ...     currency, = currencies
    >>> Company = Model.get('company.company')
    >>> Party = Model.get('party.party')
    >>> company_config = Wizard('company.company.config')
    >>> company_config.execute('company')
    >>> company = company_config.form
    >>> party = Party(name='B2CK')
    >>> party.save()
    >>> company.party = party
    >>> company.currency = currency
    >>> company_config.execute('add')
    >>> company, = Company.find([])

Reload the context::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> config._context = User.get_preferences(True, config.context)

Create fiscal year::

    >>> FiscalYear = Model.get('account.fiscalyear')
    >>> Sequence = Model.get('ir.sequence')
    >>> SequenceStrict = Model.get('ir.sequence.strict')
    >>> fiscalyear = FiscalYear(name=str(today.year))
    >>> fiscalyear.start_date = today + relativedelta(month=1, day=1)
    >>> fiscalyear.end_date = today + relativedelta(month=12, day=31)
    >>> fiscalyear.company = company
    >>> post_move_seq = Sequence(name=str(today.year), code='account.move',
    ...     company=company)
    >>> post_move_seq.save()
    >>> fiscalyear.post_move_sequence = post_move_seq
    >>> invoice_seq = SequenceStrict(name=str(today.year),
    ...     code='account.invoice', company=company)
    >>> invoice_seq.save()
    >>> fiscalyear.out_invoice_sequence = invoice_seq
    >>> fiscalyear.in_invoice_sequence = invoice_seq
    >>> fiscalyear.out_credit_note_sequence = invoice_seq
    >>> fiscalyear.in_credit_note_sequence = invoice_seq
    >>> fiscalyear.save()
    >>> FiscalYear.create_period([fiscalyear.id], config.context)

Create chart of accounts::

    >>> AccountTemplate = Model.get('account.account.template')
    >>> Account = Model.get('account.account')
    >>> account_template, = AccountTemplate.find([('parent', '=', None)])
    >>> create_chart = Wizard('account.create_chart')
    >>> create_chart.execute('account')
    >>> create_chart.form.account_template = account_template
    >>> create_chart.form.company = company
    >>> create_chart.execute('create_account')
    >>> receivable, = Account.find([
    ...         ('kind', '=', 'receivable'),
    ...         ('company', '=', company.id),
    ...         ])
    >>> payable, = Account.find([
    ...         ('kind', '=', 'payable'),
    ...         ('company', '=', company.id),
    ...         ])
    >>> revenue, = Account.find([
    ...         ('kind', '=', 'revenue'),
    ...         ('company', '=', company.id),
    ...         ])
    >>> expense, = Account.find([
    ...         ('kind', '=', 'expense'),
    ...         ('company', '=', company.id),
    ...         ])
    >>> create_chart.form.account_receivable = receivable
    >>> create_chart.form.account_payable = payable
    >>> create_chart.execute('create_properties')

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer', fedicom_user='xxxx',
    ...         fedicom_password='xxxx')
    >>> customer.save()

Create category::

    >>> ProductCategory = Model.get('product.category')
    >>> category = ProductCategory(name='Category')
    >>> category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.category = category
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
    >>> template.category = category
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

Create payment term::

    >>> PaymentTerm = Model.get('account.invoice.payment_term')
    >>> PaymentTermLine = Model.get('account.invoice.payment_term.line')
    >>> payment_term = PaymentTerm(name='Direct')
    >>> payment_term_line = PaymentTermLine(type='remainder', days=0)
    >>> payment_term.lines.append(payment_term_line)
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
    >>> 
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


