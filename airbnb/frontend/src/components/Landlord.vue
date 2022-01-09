<template>
  <el-container direction="vertical">
    <div class="background"></div>
    <el-header class="header" style="height: 150px; font-size: 40px;">
      <div id="head" style="position:relative;left:300px; top: 30px; font-size: 50px;">Airbnb Analysis and Prediction</div>
    </el-header>
    <el-container>
      <el-aside width="150px" class="aside">
        <el-button-group>
          <el-button @click="goOverview">Overview</el-button>
          <el-button @click="goTenant">Tenant</el-button>
          <el-button @click="goLandlord">Landlord</el-button>
          <el-button @click="goInvestor">Investor</el-button>
          <el-button @click="goML">Machine Learning</el-button>
        </el-button-group>
      </el-aside>
      <el-main  class="frontground">
        <el-row display="margin-top:20px">
          <el-select v-model="input" placeholder="please input the city" style="display:inline-table; width: 20%; float:left" clearable @change="populaDescription()">
            <el-option value="Toronto" >Toronto</el-option>
            <el-option value="Vancouver" >Vancouver</el-option>
            <el-option value="Montreal"  >Montreal</el-option>
            <el-option value="Quebec"  >Quebec city</el-option>
            <el-option value="Victoria"  >Victoria</el-option>
            <el-option value="Ottawa"  >Ottawa</el-option>
            <el-option value="New Brunswick"  >New Brunswick</el-option>
          </el-select>
        </el-row>
        <div class="chart">
        <bar-chart class="item" :x-data="keyWordX" :y-data="keyWordY" title="TOP20 Popular Description Words" />
        </div>
         <div>
           <img width=730 height=500 :src="getCorrolationURL">
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>


<script>
// @ is an alias to /src
import BarChart from "@/components/BarChart";
export default {
  name: 'landload',
  components: { BarChart },
  data () {
    return {
      input: '',
      city: '',
      keyWordX: [],
      keyWordY: []
    }
  },
  mounted: function () {
    this.populaDescription()
  },
  methods: {
    goOverview: function () {
      this.$router.push('/overview')
    },
    goLandlord: function () {
      this.$router.push('/landlord')
    },
    goTenant: function () {
      this.$router.push('/tenant')
    },
    goInvestor: function () {
      this.$router.push('/investor')
    },
    goML: function () {
      this.$router.push('/machinelearning')
    },
    populaDescription () {
      this.$http.get('http://127.0.0.1:8000/api/popular_description?city=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.city = res['city']
            this.keyWordX = res['key_word_x']
            this.keyWordY = res['key_word_y']
          } else {
            console.log(res['msg'])
          }
        })
    }

  },
  computed : {
    getCorrolationURL : function() {
         return '../../static/Corrolation/Correlation_' + this.input + '.png'
    }
  }
}
</script>

<style scoped>
 .frontground{
  background-image: url("../../static/blue-snow.png");

  height: 100%;
  width: 100%;

}
.aside{
  background-image: url("../../static/blue-snow.png");
}
  .header{
    background-image: url("../../static/234.jpeg");
    background-repeat: no-repeat;
    background-position-x: 0%;
    background-position-y: 60%;
    background-size: 680px;
  }
  .chart {
  display: flex;
  border: 1px solid #2c3e50;
  width: 100%;
  margin: 20px 0;
}
.home {
  display: flex;
  border: 1px solid #2c3e50;
}
.item {
  flex: 1;
}
.item:not(:last-child) {
  border-right: 1px solid #2c3e50;
}
.info {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.city, .avg {
  font-size: 20px;
}
.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 100px;
  font-size: 30px;
}
.el-row {
  position: relative;
  margin-top: 10px;
  margin-bottom: 5px;
}
.el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    /*line-height: 160px;*/
}
.el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
}
</style>
