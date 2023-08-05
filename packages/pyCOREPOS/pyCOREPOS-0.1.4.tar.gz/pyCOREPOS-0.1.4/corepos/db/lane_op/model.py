# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2021 Lance Edgar
#
#  This file is part of pyCOREPOS.
#
#  pyCOREPOS is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  pyCOREPOS is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  pyCOREPOS.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data model for CORE POS "lane_op" DB
"""

import sqlalchemy as sa
# from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Product(Base):
    """
    Represents a product, purchased and/or sold by the organization.
    """
    __tablename__ = 'products'
    # __table_args__ = (
    #     sa.ForeignKeyConstraint(['department'], ['departments.dept_no']),
    #     sa.ForeignKeyConstraint(['subdept'], ['subdepts.subdept_no']),
    #     sa.ForeignKeyConstraint(['tax'], ['taxrates.id']),
    # )

    id = sa.Column(sa.Integer(), nullable=False, 
                   primary_key=True, autoincrement=True)

    upc = sa.Column(sa.String(length=13), nullable=True)

    description = sa.Column(sa.String(length=30), nullable=True)

    brand = sa.Column(sa.String(length=30), nullable=True)

    formatted_name = sa.Column(sa.String(length=30), nullable=True)

    normal_price = sa.Column(sa.Float(), nullable=True)

    price_method = sa.Column('pricemethod', sa.SmallInteger(), nullable=True)

    group_price = sa.Column('groupprice', sa.Float(), nullable=True)

    quantity = sa.Column(sa.SmallInteger(), nullable=True)

    special_price = sa.Column(sa.Float(), nullable=True)

    special_price_method = sa.Column('specialpricemethod', sa.SmallInteger(), nullable=True)

    special_group_price = sa.Column('specialgroupprice', sa.Float(), nullable=True)

    special_quantity = sa.Column('specialquantity', sa.SmallInteger(), nullable=True)

    special_limit = sa.Column(sa.SmallInteger(), nullable=True)

    start_date = sa.Column(sa.DateTime(), nullable=True)

    end_date = sa.Column(sa.DateTime(), nullable=True)

    department_number = sa.Column('department', sa.SmallInteger(), nullable=True)
    # department = orm.relationship(
    #     Department,
    #     primaryjoin=Department.number == department_number,
    #     foreign_keys=[department_number],
    #     doc="""
    #     Reference to the :class:`Department` to which the product belongs.
    #     """)

    size = sa.Column(sa.String(length=9), nullable=True)

    tax_rate_id = sa.Column('tax', sa.SmallInteger(), nullable=True)
    # tax_rate = orm.relationship(TaxRate)

    foodstamp = sa.Column(sa.Boolean(), nullable=True)

    scale = sa.Column(sa.Boolean(), nullable=True)

    scale_price = sa.Column('scaleprice', sa.Float(), nullable=True)

    mix_match_code = sa.Column('mixmatchcode', sa.String(length=13), nullable=True)

    created = sa.Column(sa.DateTime(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    # TODO: what to do about this 'replaces' thing?
    # 'batchID'=>array('type'=>'TINYINT', 'replaces'=>'advertised'),
    # batch_id = sa.Column('batchID', sa.SmallInteger(), nullable=True)
    # advertised = sa.Column(sa.Boolean(), nullable=True)

    tare_weight = sa.Column('tareweight', sa.Float(), nullable=True)

    discount = sa.Column(sa.SmallInteger(), nullable=True)

    discount_type = sa.Column('discounttype', sa.SmallInteger(), nullable=True)

    line_item_discountable = sa.Column(sa.Boolean(), nullable=True)

    unit_of_measure = sa.Column('unitofmeasure', sa.String(length=15), nullable=True)

    wicable = sa.Column(sa.SmallInteger(), nullable=True)

    quantity_enforced = sa.Column('qttyEnforced', sa.Boolean(), nullable=True)

    id_enforced = sa.Column('idEnforced', sa.SmallInteger(), nullable=True)

    cost = sa.Column(sa.Float(), nullable=True)

    special_cost = sa.Column(sa.Float(), nullable=True)

    received_cost = sa.Column(sa.Float(), nullable=True)

    in_use = sa.Column('inUse', sa.Boolean(), nullable=True)

    flags = sa.Column('numflag', sa.Integer(), nullable=True)

    subdepartment_number = sa.Column('subdept', sa.SmallInteger(), nullable=True)
    # subdepartment = orm.relationship(
    #     Subdepartment,
    #     primaryjoin=Subdepartment.number == subdepartment_number,
    #     foreign_keys=[subdepartment_number],
    #     doc="""
    #     Reference to the :class:`Subdepartment` to which the product belongs.
    #     """)

    deposit = sa.Column(sa.Float(), nullable=True)

    local = sa.Column(sa.Integer(), nullable=True,
                      default=0) # TODO: do we want a default here?

    store_id = sa.Column(sa.SmallInteger(), nullable=True)

    default_vendor_id = sa.Column(sa.Integer(), nullable=True)
    # default_vendor = orm.relationship(
    #     Vendor,
    #     primaryjoin=Vendor.id == default_vendor_id,
    #     foreign_keys=[default_vendor_id],
    #     doc="""
    #     Reference to the default :class:`Vendor` from which the product is obtained.
    #     """)

    current_origin_id = sa.Column(sa.Integer(), nullable=True)

    auto_par = sa.Column(sa.Float(), nullable=True,
                         default=0) # TODO: do we want a default here?

    price_rule_id = sa.Column(sa.Integer(), nullable=True)

    # TODO: some older DB's might not have this?  guess we'll see
    last_sold = sa.Column(sa.DateTime(), nullable=True)
