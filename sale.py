# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime
import logging
import subprocess
import sys
import traceback

from trytond.model import ModelSingleton, ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.rpc import RPC
from trytond.transaction import Transaction

__metaclass__ = PoolMeta

__all__ = ['Party', 'Sale', 'FedicomConfig', 'FedicomLog']


def isInt(value):
    try:
        int(value)
        return True
    except:
        return False


def convertToInt(value):
    try:
        return int(value)
    except:
        return 0


class Party:
    __name__ = 'party.party'

    fedicom_user = fields.Char('Fedicom User')
    fedicom_password = fields.Char('Fedicom password')


class Sale:
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls.__rpc__.update({
                'process_order': RPC(instantiate=0, readonly=False),
                })
        cls._error_messages.update({
            'user_not_exists': 'User code (%s) not Exists',
            'incorrect_login': 'Incorrect Login User',
            'incorrect_password': 'Incorrect Password (%s)',
            'no_products': 'El pedido no ha podido assignar ningun Producto',
            })

    @staticmethod
    def remove_rec_names(values):
        for key in values.copy().keys():
            if '.rec_name' in key:
                del values[key]

    @classmethod
    def process_order(cls, sales, customer_code, password, order, products):
        try:
            return cls.process_order_internal(sales, customer_code, password,
                order, products)
        except Exception, e:
            exc_type, exc_value = sys.exc_info()[:2]
            logger = logging.getLogger('sale_fedicom')
            logger.warning("Exception processing fedicom order: %s (%s)\n  %s"
                % (exc_type, exc_value, traceback.format_exc()))

            # Ensure we free table lock
            print "Process Order Internal ha petat :("
            print str(e)
            return {"error": 'Error Intern'}

    # Processes an incoming order request
    # products format: [('product_code', amount), ]
    # returns [('product_code', amount, 'reason'), ]
    @classmethod
    def process_order_internal(cls, sales, customer_code, password, order,
            products):
        pool = Pool()
        transaction = Transaction()

        Party = pool.get('party.party')
        FedicomLog = pool.get('fedicom.log')
        Product = pool.get('product.product')
        SaleLine = pool.get('sale.line')
        ShipmentOut = pool.get('stock.shipment.out')
        Location = pool.get('stock.location')

        logger = logging.getLogger('sale_fedicom')

        logger.info('Process Order %s From Party %s' % (order, customer_code))

        # Check if party exists. Password will be checked later so we can
        # at least add a log entry with "user with this customerCode has
        # tried to send an order" and  properly fill in the 'party' field.
        parties = Party.search([('fedicom_user', '=', customer_code)])

        if len(parties) == 0:
            # Log error
            with transaction.set_user(0):
                FedicomLog.create([{
                    'message': cls.raise_user_error('user_not_exists',
                               str(customer_code), raise_exception=False)
                }])
            logger.info("Customer code %s not found" % customer_code)
            return {'error': cls.raise_user_error('incorrect_login',
                    raise_exception=False)}

        party = parties[0]
        if party.fedicom_password != password:
            # Log error, specifying party
            with transaction.set_user(0):
                FedicomLog.create([{
                    'message': cls.raise_user_error('incorrect_password',
                            password, raise_exception=False),
                    'party': party
                }])
            logger.info("Invalid password for user %s " % customer_code)
            return {'error': cls.raise_user_error('incorrect_login',
                    raise_exception=False)}
        sale = {
            'state': 'draft',
            'party': party.id,
            }

        sale.update(cls(party=party).on_change_party())
        cls.remove_rec_names(sale)
        # We'll keep the sum of assigned units per product as there might be
        # a product in more than one line (or the same product with different
        # codes due to synonyms) We'll substract this amount to the available
        # stock to be sure we don't go under zero because the stock is
        # substracted once after processing all lines.

        assigned_products = {}
        missing_stock = []
        lines = []
        for prod in products:
            logger.info("Process: %s" % prod)
            product = None
            product_available = None
            # Search the product code within the products
            search_products = Product.search([
                    ('code', '=', str(prod[0][-7:]))])

            product_code = str(prod[0][-7:]).rjust(7, '0')
            if len(search_products) > 0:
                product = search_products[0]
                location_ids = [x.storage_location.id for x in
                    Location.search([('type', '=', 'warehouse')])]
                with Transaction().set_context(locations=location_ids):
                    product_available = int(product.forecast_quantity) or 0

            ordered = convertToInt(prod[1])
            if not product:
                # If product doesn't exist...
                missing_stock.append((prod[0], ordered, 'NOT_WORKED'))
                assigned = 0
                logger.info("Procuct %s Not Worked" % prod[0])
            else:
                # If product exists...
                already_assigned = assigned_products.get(product_code, 0)
                available = max(product_available - already_assigned, 0)
                available = max(min(available, product_available), 0)
                if available >= ordered:
                    assigned = ordered
                else:
                    assigned = available
                    missing_stock.append((prod[0],
                        ordered - assigned, 'NOT_STOCK'))

                assigned_products[product_code] = already_assigned + assigned

            logger.info("Procuct %s: [%s/%s Misses(%s)]" %
                (product_code, assigned, ordered, ordered - assigned))

            if assigned:
                lvals = {
                    'product': product.id,
                    'quantity': assigned,
                    'type': 'line',
                    'sequence': len(lines) + 1,
                    }
                lvals.update(SaleLine(product=product, sale=None, unit=None,
                        quantity=None, description=None).on_change_product())
                cls.remove_rec_names(lvals)
                if lvals.get('taxes'):
                    lvals['taxes'] = [('set', lvals['taxes'])]
                del lvals['amount']

                lines.append(lvals)

        logger.info("Process Lines Finished")

        if len(lines) == 0:
            with transaction.set_user(0):
                FedicomLog.create([{
                    'message': cls.raise_user_error('no_products',
                                raise_exception=False),
                    'party': party.id,
                }])

            logger.info("Returning Misses")
            return {'missingStock': missing_stock}

        sales = cls.create([sale])
        sale, = sales
        for line in lines:
            line['sale'] = sale.id
        SaleLine.create(lines)
        logger.info("Order Created: %s" % sale.rec_name)
        cls.quote(sales)
        cls.confirm(sales)
        cls.process(sales)

        logger.info("Order confirmed %s" % sale.rec_name)

        ShipmentOut.wait(sale.shipments)
        ShipmentOut.assign_try(sale.shipments)

        with transaction.set_user(0):
            FedicomLog.create([{
                'message': 'Nuevo pedido',
                'sale': sale.id,
                'party': party.id,
            }])

        logger.info("Returning Misses")
        return {'missingStock': missing_stock}


class FedicomConfig(ModelSingleton, ModelSQL, ModelView):
    'Fedicom Config'
    __name__ = 'fedicom.config'

    name = fields.Char('Name', required=True)
    host = fields.Char('Host')
    port = fields.Integer('Port')
    user = fields.Many2One('res.user', 'User')

    @classmethod
    def __setup__(cls):
        super(FedicomConfig, cls).__setup__()
        cls._buttons.update({
            'test': {},
            'restart': {},
            })
        cls._error_messages.update({
            'test_failed': 'Test Failed',
            'test_ok': 'Test Ok',
            'restart_server': 'Please try to restart server',
            })

    @classmethod
    @ModelView.button
    def restart(cls, instances):
        logging.getLogger('sale_fedicom').info(
                "Starting/Restarting Service")

        service_file = "./modules/sale_fedicom/service/service.py"
        subprocess.Popen(["pkill", "-9", "-f", service_file])
        subprocess.Popen(["python", service_file], stdout=subprocess.PIPE)

    @classmethod
    @ModelView.button
    def test(cls, instances):
        try:
            subprocess.check_output(["python",
                "./modules/sale_fedicom/service/client.py"])
        except:
            cls.raise_user_error('test_failed', 'restart_server')

        cls.raise_user_warning('test_ok')


class FedicomLog(ModelSQL, ModelView):
    'Fedicom Log'
    __name__ = 'fedicom.log'
    _rec_name = "message"

    message = fields.Char('Message', required=True)
    timestamp = fields.DateTime('Timestamp')
    sale = fields.Many2One('sale.sale', 'Sale')
    party = fields.Many2One('party.party', 'Customer')

    @classmethod
    def __setup__(cls):
        super(FedicomLog, cls).__setup__()
        cls._order.insert(0, ('timestamp', 'DESC'))

    @staticmethod
    def default_timestamp():
        return datetime.datetime.now()
