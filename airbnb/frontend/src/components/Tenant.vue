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
           <el-select v-model="input" placeholder="please input the city" style="display:inline-table; width: 20%; float:left" clearable @change="perPrice()">
            <el-option value="Toronto" >Toronto</el-option>
            <el-option value="Vancouver" >Vancouver</el-option>
            <el-option value="Montreal"  >Montreal</el-option>
            <el-option value="Quebec"  >Quebec city</el-option>
            <el-option value="Victoria"  >Victoria</el-option>
            <el-option value="Ottawa"  >Ottawa</el-option>
            <el-option value="New Brunswick"  >New Brunswick</el-option>
          </el-select>
        </el-row>
        <el-input v-model="input_neighborhood" placeholder="please input the neighborhood" style="display:inline-table; width: 25%; float:left" clearable>
          <template slot="append"><el-button type="info" @click="topScoreNeighborhood()" style="float:left;">search</el-button></template>
        </el-input>
        <div class="chart">
          <bar-chart class="item" :x-data="neighborhoodId" :y-data="neighborhoodScore" title="Top Score GroupBy Neighborhood" :min-value="4.3" />
        </div>
        <div class="chart">
          <bar-chart class="item" :x-data="avgPriceX" :y-data="avgPriceY" title="Average Per Price GroupBy Neighorbood" :min-value="0" />
          <bar-chart class="item" :x-data="medianPriceX" :y-data="medianPriceY" title="Median Per Price GroupBy Neighorbood" :min-value="0" />
        </div>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
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
      input_neighborhood: '',
      neighborhoodId: [],
      neighborhoodScore: [],
      avgPriceX : [],
      avgPriceY : [],
      medianPriceX : [],
      medianPriceY : [],
      city: '',

    }
  },
  mounted: function () {
    this.topScoreNeighborhood ()
    this.perPrice ()
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
    topScoreNeighborhood () {
      this.$http.get('http://127.0.0.1:8000/api/top_score_neighborhood?city=' + this.input+'&'+'neighborhood='+this.input_neighborhood)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.city = res['city']
            this.neighborhoodId = res['id']
            this.neighborhoodScore = res['score']
          } else {
            console.log(res['msg'])
          }
        })
    },
    perPrice () {
       this.$http.get('http://127.0.0.1:8000/api/per_price?city=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.city = res['city']
            this.avgPriceX = res['avg_per_price_x']
            this.avgPriceY = res['avg_per_price_y']
            this.medianPriceX = res['median_per_price_x']
            this.medianPriceY = res['median_per_price_y']
          } else {
            console.log(res['msg'])
          }
        })
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
