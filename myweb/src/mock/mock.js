const Mock = require('mockjs')

Mock.mock('/req_pur_check', 'post', require('./json/req_pur_check'))
Mock.mock('/req_pur_prd', 'post', require('./json/req_pur_prd'))
Mock.mock('/req_pur_prd_add', 'post', require('./json/req_pur_prd_add'))

Mock.mock('/so_check', 'post', require('./json/so_check'))
Mock.mock('/so_sod', 'post', require('./json/so_sod'))
Mock.mock('/so_sod_add', 'post', require('./json/so_sod_add'))

Mock.mock('/pc_check', 'post', require('./json/pc_check'))
Mock.mock('/pc_cd', 'post', require('./json/pc_cd'))
Mock.mock('/pc_pay', 'post', require('./json/pc_pay'))
Mock.mock('/pc_cd_add', 'post', require('./json/pc_cd_add'))

Mock.mock('/po_check', 'post', require('./json/po_check'))
Mock.mock('/po_od', 'post', require('./json/po_od'))
Mock.mock('/po_od_add_rp', 'post', require('./json/po_od_add_rp'))
Mock.mock('/po_od_add_pc', 'post', require('./json/po_od_add_pc'))

Mock.mock('/department', 'post', require('./json/department'))
Mock.mock('/users', 'post', require('./json/users'))
Mock.mock('/role', 'post', require('./json/role'))
Mock.mock('/organization', 'post', require('./json/organization'))
Mock.mock('/area', 'post', require('./json/area'))
Mock.mock('/center', 'post', require('./json/center'))
Mock.mock('/brand', 'post', require('./json/brand'))
Mock.mock('/warehouse', 'post', require('./json/warehouse'))
Mock.mock('/store', 'post', require('./json/store'))
Mock.mock('/supplier', 'post', require('./json/supplier'))
Mock.mock('/customer', 'post', require('./json/customer'))
Mock.mock('/materage', 'post', require('./json/meterage'))
Mock.mock('/material_type', 'post', require('./json/material_type'))
Mock.mock('/material', 'post', require('./json/material'))

Mock.mock('/stock_check', 'post', require('./json/stock_check'))
