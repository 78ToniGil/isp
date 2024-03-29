# Copyright 2023 Toni Gil - antonio.gil@hilltech.es
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Telefonía",
    "summary": "Internet service providers",
    "version": "14.0.1.0.0",
    "category": "Services",
    "website": "https://github.com/78Tonigil/isp",
    "author": "Hilltech Digital",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/isp_security.xml",
        "security/ir.model.access.csv",
        "views/isp_linea_views.xml",
        "views/isp_fibra_views.xml",
        "data/cron.xml"
    ],
}
