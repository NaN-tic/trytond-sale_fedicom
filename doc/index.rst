GENERAL DESCRIPTION
===================

This is an Tryton module for managing needs to handle incomming
orders that use the TCP/IP Fedicom protocol. This is a standard protocol in the
pharmaceutical business in Spain. The protocol itself is implemented somewhere
else and this module simply handles orders reception, calculates units available
and returns the quantity the customer will receive.

TECHNICAL DESCRIPTION
=====================

The most important functionalities of the module are:
- Process Internet orders and return unserved units.
- Update modem incoming orders into our Tryton database to keep in sync our stock. This should
be executed every minute by the cron job framework of Tryton and just before any new Internet
order is processed.
