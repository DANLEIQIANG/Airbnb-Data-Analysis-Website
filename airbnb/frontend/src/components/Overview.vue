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
        <el-row display="margin-top:10px" :inline="true">
          <!---<el-input v-model="input" placeholder="please input the city" style="display:inline-table; width: 20%; float:left" clearable>
            <template slot="append"><el-button type="info" @click="mockRes(),avgScore()" style="float:left;">search</el-button></template>
          </el-input>--->
          <el-select v-model="input" placeholder="please input the city" style="display:inline-table; width: 20%; float:left" clearable @change="mockRes(),avgScore()">
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
          <div class="info item">
            <div class="city">{{ this.city }}</div>
            <div class="avg">Average Price: {{ this.avgPrice }}</div>
          </div>
            <bar-chart class="item" :x-data="roomXData" :y-data="roomYData" title="Room Type" />
            <bar-chart class="item" :x-data="tenancyXData" :y-data="tenancyYData" title="Tenancy Term" />
          </div>
        <div>
          <iframe width=730 height=500 style="float:left;" frameborder=0 scrolling=auto :src="getheatMapURL"></iframe>
          <iframe width=730 height=500 style="float:right;" frameborder=0 scrolling=auto :src="getneighURL"></iframe>
          <div id="testHeatMap" style="float: left; width: 40%; font-size: 30px">Heat Map</div>
          <div id="testNeighborMap" style="float: right; width: 40%; font-size: 30px">Neighbor Map</div>
        </div>
        <div class="chart">
          <bar-chart class="item" :x-data="Xneighborhood" :y-data="Yscore" title="Avg Neighborhood Score Group By City" :min-value="3.5" />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
// @ is an alias to /src
import BarChart from "@/components/BarChart";
export default {
  name: 'home',
  components: { BarChart },
  data () {
    return {
      input: '',
      roomXData: [],
      roomYData: [],
      tenancyXData: [],
      tenancyYData: [],
      city: '',
      avgPrice: 0,
      Xneighborhood: [],
      Yscore: [],

    }
  },
  mounted: function () {
    this.mockRes()
    this.avgScore()
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
    mockRes () {
      this.$http.get('http://127.0.0.1:8000/api/display_city?city=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.city = res['city']
            this.roomXData = res['room_type_x']
            this.roomYData = res['room_type_y']
            this.tenancyXData = res['tenancy_term_x']
            this.tenancyYData = res['tenancy_term_y']
            this.avgPrice = res['Average_price'].toFixed(2)
          } else {
            console.log(res['msg'])
          }
        })
    },
    avgScore () {
      this.$http.get('http://127.0.0.1:8000/api/avg_score?city=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.city = res['city']
            this.Xneighborhood = res['neighborhood']
            this.Yscore = res['score']
          } else {
            console.log(res['msg'])
          }
        })
    }

  },
  computed : {
    getheatMapURL : function() {
         return '../../static/htmlMap/map_heatmap_' + this.input + '.html'
    },
    getneighURL : function() {
         return '../../static/htmlMap/map_neigh_' + this.input + '.html'
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
    line-height: 200px
}
</style>
