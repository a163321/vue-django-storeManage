<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 物料明细
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-button
          type="primary"
          icon="el-icon-delete"
          v-if="ifchange"
          @click="delAllSelection"
        >批量删除</el-button>
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" icon="el-icon-plus" class="button-save" @click="add" v-if="ifchange">选择请购单</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        :row-class-name="tableRowClassName"
        @selection-change="handleSelectionChange"
        size="mini"
      >
        <el-table-column
          type="selection"
          v-if="ifchange"
          width="55">
        </el-table-column>
        <el-table-column prop="cd_iden" sortable label="物料编码" :filters="cd_idenSet"
      :filter-method="filter"  align="center"></el-table-column>
        <el-table-column prop="cd_name" sortable label="物料名称" :filters="cd_nameSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_specification" sortable label="规格" :filters="cd_specificationSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_model" sortable label="型号" :filters="cd_modelSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_meterage" sortable label="单位" :filters="cd_meterageSet"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_num" sortable label="数量" align="center">
          <template slot-scope="scope">
            <el-input
              v-if="formadd.so_type=='退换货'"
              prefix-icon="el-icon-minus"
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.cd_num"
              @input="scope.row.cd_num = inputnum(scope.row.cd_num)"
              @change="scope.row.cd_num = changenum(scope.row.cd_num)">
            </el-input>
            <el-input
              v-else
              placeholder="1"
              :disabled="!ifchange"
              v-model="scope.row.cd_num"
              @input="scope.row.cd_num = inputnum(scope.row.cd_num)"
              @change="scope.row.cd_num = changenum(scope.row.cd_num)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="cd_taxRate" sortable label="税率" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="13"
              :disabled="!ifchange"
              v-model="scope.row.cd_taxRate"
              @input="scope.row.cd_taxRate = inputcdTaxRate(scope.row.cd_taxRate,scope.$index)"
              @change="scope.row.cd_taxRate = changecdTaxRate(scope.row.cd_taxRate)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="cd_tax_unitPrice" sortable label="含税单价" align="center">
          <template slot-scope="scope">
            <el-input
              placeholder="0"
              :disabled="!ifchange"
              v-model="scope.row.cd_tax_unitPrice"
              @input="scope.row.cd_tax_unitPrice = inputcdTaxUnitPrice(scope.row.cd_tax_unitPrice)"
              @change="scope.row.cd_tax_unitPrice = changecdTaxUnitPrice(scope.row.cd_tax_unitPrice)">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column prop="cd_tax_unitPrice/(1+cd_taxRate/100)" sortable label="无税单价" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.cd_tax_unitPrice/(1+scope.row.cd_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cd_tax_unitPrice*cd_num" sortable label="含税金额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.cd_tax_unitPrice*scope.row.cd_num).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cd_tax_unitPrice*cd_num/(1+cd_taxRate/100)" sortable label="无税金额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.cd_tax_unitPrice*scope.row.cd_num/(1+scope.row.cd_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cd_tax_unitPrice*cd_num*cd_taxRate/100/(1+cd_taxRate/100)" sortable label="税额" align="center">
          <template slot-scope="scope">
            <el-tag
              :type="'success'"
            >{{(scope.row.cd_tax_unitPrice*scope.row.cd_num*scope.row.cd_taxRate/100/(1+scope.row.cd_taxRate/100)).toFixed(2)}}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cd_pr_iden" sortable label="请购单号" :filters="cd_rpidenset"
      :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="cd_prd_remarks" sortable label="备注" align="center">
          <template slot-scope="props">
            <el-input type="textarea" v-model="props.row.cd_prd_remarks" rows="3" :disabled="!ifchange"
              placeholder="请输入200字以内的描述" maxlength="200" show-word-limit clearable @input="find"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" v-if="ifchange">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
            >删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
          :page-sizes="[5, 10, 20, 50, 100, 200, 500]"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </div>
    </div>
    <!-- 新增弹出框 -->
    <el-dialog title="新增物料" :visible.sync="addVisible" width="90%" append-to-body :close-on-click-modal="false" :destroy-on-close="true">
      <Cdadd ref="Cdadd" @add="addPrd" :tableHas="tableData" :formadd="formadd" :ifhasorga="ifhasorga" :orga_name="orga_name"></Cdadd>
    </el-dialog>
  </div>
</template>

<script>
import {postAPI} from '../../../api/api'
import Cdadd from './PurConCdAdd.vue'

export default {
  name: 'pc_cd',
  props: ['formadd', 'ifchange', 'orga_name', 'cds'],
  components: {
    Cdadd
  },
  data () {
    return {
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      cd_idenSet: [],
      cd_nameSet: [],
      cd_specificationSet: [],
      cd_modelSet: [],
      cd_meterageSet: [],
      cd_rpidenset: [],
      addVisible: false,
      ifhasorga: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
    // this.$nextTick(function () {
    //   if (!this.formadd.orga_name) {
    //     this.addVisible = true
    //   }
    // })
  },
  methods: {
    getData () {
      if (this.formadd.pc_iden === '') {
        return
      }
      let _this = this
      _this.tableData = this.cds
      _this.pageTotal = _this.tableData.length
      _this.find()
      _this.cd_idenSet = []
      _this.cd_nameSet = []
      _this.cd_specificationSet = []
      _this.cd_modelSet = []
      _this.cd_meterageSet = []
      _this.cd_pr_idenset = []
      let nameset = new Set()
      let specificationset = new Set()
      let modelset = new Set()
      let meterageset = new Set()
      let rpidenset = new Set()
      let idenset = new Set()
      for (let i in _this.tableData) {
        nameset.add(_this.tableData[i]['cd_name'])
        specificationset.add(_this.tableData[i]['cd_specification'])
        modelset.add(_this.tableData[i]['cd_model'])
        meterageset.add(_this.tableData[i]['cd_meterage'])
        rpidenset.add(_this.tableData[i]['cd_pr_iden'])
        idenset.add(_this.tableData[i]['cd_iden'])
      }
      for (let i of nameset) {
        _this.cd_nameSet.push({
          text: i,
          value: i
        })
      }
      for (let i of idenset) {
        _this.cd_idenSet.push({
          text: i,
          value: i
        })
      }
      for (let i of meterageset) {
        _this.cd_meterageSet.push({
          text: i,
          value: i
        })
      }
      for (let i of rpidenset) {
        _this.cd_pr_idenset.push({
          text: i,
          value: i
        })
      }
      for (let i of specificationset) {
        _this.cd_specificationSet.push({
          text: i,
          value: i
        })
      }
      for (let i of modelset) {
        _this.cd_modelSet.push({
          text: i,
          value: i
        })
      }
    },
    // 表格每行的class样式
    tableRowClassName ({row, rowIndex}) {
      this.pageTotal = rowIndex + 1
      if (rowIndex >= (this.query.pageIndex - 1) * this.query.pageSize && rowIndex < this.query.pageIndex * this.query.pageSize) {
        return ''
      }
      return 'tableRowDisplay'
    },
    // 表格下拉筛选
    filter (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
        String(data.cd_iden).toLowerCase().includes(String(this.search).toLowerCase()) ||
        String(data.cd_name).toLowerCase().includes(String(this.search).toLowerCase()) ||
        String(data.cd_specification).toLowerCase().includes(String(this.search).toLowerCase()) ||
        String(data.cd_model).toLowerCase().includes(String(this.search).toLowerCase()) ||
        String(data.cd_meterage).toLowerCase().includes(String(this.search).toLowerCase()))
    },
    // 新增
    add () {
      this.addVisible = true
      if (!this.formadd.orga_name || this.formadd.orga_name === '') {
        this.ifhasorga = false
      } else {
        this.ifhasorga = true
      }
      let _this = this
      this.$nextTick(() => _this.$refs.Cdadd.getData())
    },
    // 新增物料
    addPrd (val) {
      for (let i in val) {
        val[i].cd_num = val[i].prd_num
        val[i].cd_taxRate = '13'
        val[i].cd_tax_unitPrice = '0.00'
        val[i].cd_iden = val[i].prd_iden
        val[i].cd_name = val[i].prd_name
        val[i].cd_specification = val[i].prd_specification
        val[i].cd_model = val[i].prd_model
        val[i].cd_meterage = val[i].prd_meterage
        val[i].cd_pr_iden = val[i].pr_iden
        val[i].cd_pcd_prd_remarksr_iden = val[i].prd_remarks
      }
      this.tableData = this.tableData.concat(val)
      this.find()
      let message = '新增' + val.length + '条'
      this.$message.success(message)
      this.addVisible = false
    },
    // 修改数量
    inputnum (num) {
      num = num.replace(/[^\d]/g, '')
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      this.find()
      return num
    },
    changenum (num) {
      if (num < 1) {
        num = 1
      }
      if (num === '') {
        num = 1
      }
      this.find()
      return num
    },
    inputcdTaxRate (num, index) {
      console.log(index)
      num = num.replace(/[^\d]/g, '')
      if (num.substr(0, 1) === '0' && num.length === 2) {
        num = num.substr(1, num.length)
      }
      this.find()
      return num
    },
    changecdTaxRate (num) {
      if (num === '') {
        num = 13
      }
      if (num > 16) {
        num = 16
      }
      this.find()
      return num
    },
    inputcdTaxUnitPrice (num) {
      if (num !== '' && num.substr(0, 1) === '.') {
        num = ''
      }
      num = num.replace(/^0*(0\.|[1-9])/, '$1') // 粘贴不生效
      num = num.replace(/[^\d.]/g, '') // 清除“数字”和“.”以外的字符
      num = num.replace(/\.{2,}/g, '.') // 只保留第一个. 清除多余的
      num = num.replace('.', '$#$').replace(/\./g, '').replace('$#$', '.')
      num = num.replace(/^()*(\d+)\.(\d\d).*$/, '$1$2.$3')// 只能输入两个小数
      if (num.indexOf('.') < 0 && num !== '') { // 以上已经过滤，此处控制的是如果没有小数点，首位不能为类似于 01、02的金额
        if (num.substr(0, 1) === '0' && num.length === 2) {
          num = num.substr(1, num.length)
        }
      }
      this.find()
      return num
    },
    changecdTaxUnitPrice (num) {
      if (num === '') {
        num = 0
      }
      num = Number(num).toFixed(2)
      this.find()
      return num
    },
    // 删除操作
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          this.$message.success('删除成功')
          this.tableData.splice(index, 1)
          let pageIndexNew = Math.ceil((this.pageTotal - 1) / this.query.pageSize) // 新的页面数量
          this.query.pageIndex = (this.query.pageIndex > pageIndexNew) ? pageIndexNew : this.query.pageIndex
          this.query.pageIndex = (this.query.pageIndex === 0) ? 1 : this.query.pageIndex
          this.find()
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    },
    // 多选操作
    handleSelectionChange (val) {
      this.multipleSelection = val
    },
    // 批量删除
    delAllSelection () {
      let delnum = this.multipleSelection.length
      if (delnum === 0) {
        return
      }
      this.$confirm('确定要删除' + delnum + '条吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let pageIndexNew = Math.ceil((this.pageTotal - this.multipleSelection.length) / this.query.pageSize) // 新的页面数量
          this.query.pageIndex = (this.query.pageIndex > pageIndexNew) ? pageIndexNew : this.query.pageIndex
          this.query.pageIndex = (this.query.pageIndex === 0) ? 1 : this.query.pageIndex
          for (let i in this.multipleSelection) {
            let x = this.tableData.valueOf(this.multipleSelection[i])
            this.tableData.splice(x, 1)
          }
          this.find()
          this.$message.success('删除' + delnum + '条成功')
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消删除'
          })
        })
    },
    // 保存
    save (callback = null) {
      let _this = this
      _this.$emit('saveall', val => {
        if (val) {
          let data = {
            cds: _this.tableData,
            pc_iden: _this.formadd.pc_iden
          }
          postAPI('/purchase/cdSave', data).then(function (res) {
            console.log(res.data)
            if (res.data.signal === 0) {
              _this.$message.success(`保存物料明细成功`)
              if (typeof (callback) === 'function') {
                let back = true
                callback(back)
              }
            } else {
              _this.$message.error('保存物料明细失败')
              if (typeof (callback) === 'function') {
                let back = false
                callback(back)
              }
            }
          }).catch(function (err) {
            _this.$message.error('保存物料明细失败')
            console.log(err)
            if (typeof (callback) === 'function') {
              let back = false
              callback(back)
            }
          })
        } else {
          if (typeof (callback) === 'function') {
            let back = false
            callback(back)
          }
        }
      })
    },
    // 提交
    commit () {
      let _this = this
      this.$confirm('确定要提交吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          _this.save(val => {
            if (val) {
              postAPI('/purchase/cdSubmit', _this.formadd).then(function (res) {
                console.log(res.data)
                if (res.data.signal === 0) {
                  _this.$message.success(`提交成功`)
                  _this.$emit('save')
                  _this.$emit('commit')
                } else {
                  _this.$message.error('提交失败')
                }
              }).catch(function (err) {
                _this.$message.error('提交失败')
                console.log(err)
              })
            }
          })
        })
        .catch(() => {
          _this.$message({
            type: 'info',
            message: '取消提交'
          })
        })
    },
    // 新增窗口弹出
    addShow () {
      this.addVisible = true
    },
    getTable () {
      for (let i in this.tableData) {
        this.tableData[i].cd_unitPrice = this.tableData[i].cd_tax_unitPrice / (1 + this.tableData[i].cd_taxRate / 100)
        this.tableData[i].cd_tax_sum = this.tableData[i].cd_tax_unitPrice * this.tableData[i].cd_num
        this.tableData[i].cd_sum = this.tableData[i].cd_tax_unitPrice * this.tableData[i].cd_num / (1 + this.tableData[i].cd_taxRate / 100)
        this.tableData[i].cd_tax_price = this.tableData[i].cd_tax_unitPrice * this.tableData[i].cd_num * this.tableData[i].cd_taxRate / 100 / (1 + this.tableData[i].cd_taxRate / 100)
      }
      return this.tableData
    }
  }
}
</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>

<style scoped>
  .handle-box {
    margin-bottom: 20px;
  }

  .table {
    width: 100%;
    font-size: 14px;
  }

  .red {
    color: #ff0000;
  }
  .input-search {
    margin-left: 20px;
    width: 40%;
  }
  .button-save {
    float: right;
    margin-left: 30px;
  }
</style>
