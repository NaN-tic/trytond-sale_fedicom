# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import logging
import subprocess
from trytond.model import Model, ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all_ = ['FedicomConfiguration', 'FedicomConfigurationCompany']


class FedicomConfiguration(ModelSingleton, ModelSQL, ModelView):
    'Fedicom Configuration'
    __name__ = 'fedicom.configuration'

    name = fields.Function(fields.Char('Name'), 'get_company_config',
        'set_company_config')
    host = fields.Function(fields.Char('Host'), 'get_company_config',
        'set_company_config')
    port = fields.Function(fields.Integer('Port'), 'get_company_config',
        'set_company_config')
    user = fields.Function(fields.Many2One('res.user', 'User'),
        'get_company_config', 'set_company_config')
    warehouse = fields.Function(fields.Many2One('stock.location',
            'Default Warehouse', domain=[
                ('type', '=', 'warehouse')
                ]), 'get_company_config', 'set_company_config')

    @classmethod
    def __setup__(cls):
        super(FedicomConfiguration, cls).__setup__()
        cls._buttons.update({
            'test': {},
            'restart': {},
            })

    @classmethod
    def get_company_config(cls, configs, names):
        pool = Pool()
        CompanyConfig = pool.get('fedicom.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])

        res = {}
        for fname in names:
            res[fname] = {
                configs[0].id: None,
                }
            if company_configs:
                val = getattr(company_configs[0], fname)
                if isinstance(val, Model):
                    val = val.id
                res[fname][configs[0].id] = val
        return res

    @classmethod
    def set_company_config(cls, configs, name, value):
        pool = Pool()
        CompanyConfig = pool.get('fedicom.configuration.company')

        company_id = Transaction().context.get('company')
        company_configs = CompanyConfig.search([
                ('company', '=', company_id),
                ])
        if company_configs:
            company_config = company_configs[0]
        else:
            company_config = CompanyConfig(company=company_id)
        setattr(company_config, name, value)
        company_config.save()

    @classmethod
    @ModelView.button
    def restart(cls, instances):
        logging.getLogger('sale_fedicom').info(
                "Starting/Restarting Service")

        service_file = "./modules/sale_fedicom/service/fedicom_service.py"
        subprocess.Popen(["pkill", "-9", "-f", service_file])
        subprocess.Popen(["python", service_file], stdout=subprocess.PIPE)

    @classmethod
    @ModelView.button
    def test(cls, instances):
        try:
            subprocess.check_output(["python",
                "./modules/sale_fedicom/service/client.py"])
        except:
            raise UserError(gettext('test_failed'), gettext('restart_server'))
        raise UserError(gettext('sale_fedicom.test_ok'))


class FedicomConfigurationCompany(ModelSQL):
    'Fedicom Configuration per Company'
    __name__ = 'fedicom.configuration.company'

    company = fields.Many2One('company.company', 'Company', required=True,
        ondelete='CASCADE', select=True)
    name = fields.Char('Name')
    host = fields.Char('Host')
    port = fields.Integer('Port')
    user = fields.Many2One('res.user', 'User')
    warehouse = fields.Many2One('stock.location', 'Default Warehouse',
        domain=[('type', '=', 'warehouse')], required=True)
