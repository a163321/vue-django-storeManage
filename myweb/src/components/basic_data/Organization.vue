<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 库存组织管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" icon="el-icon-plus" @click="handleAlter" class="alter-button">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.orga_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="orga_iden" sortable label="编码"  align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="名称" :filters="orga_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="area_name" sortable label="区域" :filters="area_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="orga_creator" sortable label="创建人" :filters="orga_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="orga_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-unlock"
              class="red"
              @click="handleStop(scope.row)"
              v-if="scope.row.orga_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.orga_status===0"
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
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
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="70px"  class="form" >
          <el-row>
          <el-form-item label="编码" class="inputs" align="left">
            <el-col :span="10">
              <el-input v-model="form.orga_iden" ></el-input>
            </el-col>
          </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs"  align="left">
              <el-col :span="10">
                <el-input v-model="form.orga_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="区域"  align="left">
              <el-select v-model="form.area_name" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in area_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.orga_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="70px">
          <el-row>
            <el-form-item label="编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.orga_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.orga_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="区域"  align="left">
              <el-select v-model="editform.area_name" placeholder="请选择区域" disabled class="option" >
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.orga_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      area_options: [],
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        orga_iden: '',
        orga_name: '',
        orga_remarks: '',
        area_name: ''
      },
      orga_iden: '',
      orga_nameSet: [],
      area_nameSet: [],
      orga_creatorSet: [],
      editform: {
        orga_iden: '',
        orga_name: '',
        orga_remarks: '',
        area_name: ''
      },
      username: '',
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      getAPI('/base/organizations').then(function (res) {
        let n = res.data.max_iden.length
        let num = parseInt(res.data.max_iden) + 1
        _this.username = String(Array(n > ('' + num).length ? (n - ('' + num).length + 1) : 0).join(0) + num)
        if (!res.data.organizations) {
          return
        }
        _this.tableData = res.data.organizations
        _this.pageTotal = res.data.organizations.length
        _this.find()
        _this.orga_nameSet = []
        _this.area_nameSet = []
        _this.orga_creatorSet = []
        let nameset = new Set()
        let areaset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['orga_name'])
          areaset.add(_this.tableData[i]['area_name'])
          creatorset.add(_this.tableData[i]['orga_creator'])
        }
        for (let i of nameset) {
          _this.orga_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of areaset) {
          _this.area_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.orga_creatorSet.push({
            text: i,
            value: i
          })
        }
      }).catch(function (err) {
        console.log(err)
      })
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
    // 新增
    handleAlter () {
      this.getlist()
      this.alterVisible = true
      this.form.orga_iden = this.username
    },
    // 一键清除新增表单
    clearform () {
      this.form.area_name = ''
      this.form.orga_iden = ''
      this.form.orga_name = ''
      this.form.orga_remarks = ''
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.orga_status = 0
          postAPI('/base/organizationStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.orga_status = 1
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.orga_status = 1
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.orga_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_iden).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.area_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_createDate).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.orga_status = 1
          postAPI('/base/organizationStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.orga_status = 0
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.orga_status = 0
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消启用'
          })
        })
    },
    // 获取列表
    getlist () {
      let _this = this
      getAPI('/base/organizationNew').then(function (res) {
        _this.area_options = res.data.areas
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.orga_iden = row.orga_iden
      this.editform.orga_name = row.orga_name
      this.editform.area_name = row.area_name
      this.editform.orga_remarks = row.orga_remarks
      this.editform.orga_status = row.orga_status
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      if (!this.editform.orga_iden || !this.editform.orga_name || !this.editform.area_name) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/organizationUpdate', _this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.editVisible = false
          _this.$message.success(`修改成功`)
          _this.getData()
          _this.clearform()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`修改失败`)
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      if (!this.form.orga_iden || !this.form.orga_name || !this.form.area_name) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      _this.form.orga_status = 0
      postAPI('/base/organizationAdd', _this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`新增失败`)
        console.log(err)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    }
  }
}</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
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
    position: relative;
  }

  .input-search {
    width: 50%;
  }
  .alter-button{
    position: absolute;
    right:0;
  }

  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: GREEN;
  }
  .inputs {
    width: 590px;
  }
</style>
