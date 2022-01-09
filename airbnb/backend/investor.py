'''
  this.$http.get('http://127.0.0.1:8000/api/predict_ratio?neighbourhood_cleansed=' + this.input_neighbourhood_cleansed +
        '&city='+this.input_city + '&city='+this.input_purchase_amount + '&loan_ratio='+this.input_loan_ratio + '&loan_monthly_payment_amount='+this.input_loan_monthly_payment_amount
       + '&water_electricity_fees='+this.input_water_electricity_fees + '&property_tax='+this.input_property_tax)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.ratio = res['ratio']
          } else {
            console.log(res['msg'])
          }
        })
    }


'''
import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from backend.models import AvgPerPrice, MedianPerPrice
import pymysql
pymysql.install_as_MySQLdb()

#Ville-Marie
def build_ratio(city,neighbourhood_cleansed,purchase_amount,loan_ratio,loan_monthly_payment_amount,water_electricity_fees,property_tax):
    result = AvgPerPrice.objects.filter(neighbourhood_cleansed__contains=neighbourhood_cleansed)
    if result:
        Average_price = int(result[0].avg_val)*4
        print(Average_price)
        ratio = 100*(Average_price*365 - loan_monthly_payment_amount*12 - water_electricity_fees - property_tax)/(((100 - loan_ratio)/100)*purchase_amount)
    return ratio


