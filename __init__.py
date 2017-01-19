#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.Party,
        sale.Sale,
        sale.FedicomConfig,
        sale.FedicomLog,
        module='sale_fedicom', type_='model')
