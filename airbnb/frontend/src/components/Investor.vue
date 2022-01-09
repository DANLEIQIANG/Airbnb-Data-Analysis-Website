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
          <div>
            City: <el-input v-model="input_city" placeholder="please input the city" style="display:inline-table; width: 20%; " clearable></el-input>
          </div>
          <br>
          <div>
            Neighborhood: <el-input v-model="input_neighbourhood_cleansed" placeholder="please input the neighbourhood" style="display:inline-table; width: 20%; " clearable></el-input>
          </div>
          <br>
          <div>
            Purchase Amount: <el-input v-model="input_purchase_amount" placeholder="please input the purchase amount" style="display:inline-table; width: 20%; " clearable></el-input>
          </div>
          <br>
          <div>
            Loan Ratio:  <el-input v-model="input_loan_ratio" placeholder="please input the Loan Ratio" style="display:inline-table; width: 20%;" clearable></el-input>
          </div>
          <br>
          <div>
            Monthly Payment Amount:  <el-input v-model="input_loan_monthly_payment_amount" placeholder="please input the monthly repayment amount" style="display:inline-table; width: 20%;" clearable></el-input>
          </div>
          <br>
          <div>
            Water and Electricity Fees:  <el-input v-model="input_water_electricity_fees" placeholder="please input the water and electricity fees" style="display:inline-table; width: 20%;" clearable></el-input>
          </div>
          <br>
          <div>
            Property Tax:  <el-input v-model="input_property_tax" placeholder="please input the water and Property Tax" style="display:inline-table; width: 20%;" clearable></el-input>
          </div>
          <br>
          <div>
             <el-button type="info" @click="predictPrice()" style="">Find Predict Ration</el-button>
          </div>
          <br>
          <div class="price">Predict Ratio: {{ this.ratio }} %</div>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
        </el-row>
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
      input_accommodates: '',
      input_neighbourhood_cleansed: '',
      input_bedrooms: '',
      input_room_type: '',
      input_city: '',
      input_purchase_amount: '',
      input_loan_ratio: '',
      input_loan_monthly_payment_amount: '',
      input_water_electricity_fees: '',
      input_property_tax: '',
      price: 0,
      ratio: 0
    }
  },
  mounted: function () {
    this.predictPrice()
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
    predictPrice () {
      this.$http.get('http://127.0.0.1:8000/api/predict_ratio?neighbourhood_cleansed=' + this.input_neighbourhood_cleansed +
        '&city='+this.input_city + '&purchase_amount='+this.input_purchase_amount + '&loan_ratio='+this.input_loan_ratio + '&loan_monthly_payment_amount='+this.input_loan_monthly_payment_amount
       + '&water_electricity_fees='+this.input_water_electricity_fees + '&property_tax='+this.input_property_tax)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.ratio = res['ratio'].toFixed(2)
            console.log(this.ratio)
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
}
.el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
}
</style>
