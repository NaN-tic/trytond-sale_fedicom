#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.

from trytond.pool import Pool
from .sale import *
from .configuration import *


def register():
    Pool.register(
        Party,
        Sale,
        FedicomConfiguration,
        FedicomConfigurationCompany,
        FedicomLog,
        module='sale_fedicom', type_='model')
