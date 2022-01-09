<template>
  <div class="bar-chart" ref="chart"></div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'BarChart',
  props: {
    xData: {
      type: Array,
      default: () => []
    },
    yData: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: '',
    },
    minValue: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      chartInstance: null
    }
  },
  methods: {
    updateChart() {
      this.chartInstance.setOption({
        title: {
          text: this.title,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: this.xData,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            min: this.minValue
          }
        ],
        series: [
          {
            name: 'Direct',
            type: 'bar',
            barMaxWidth: 30,
            barMinWidth: '15%',
            data: this.yData,
          }
        ]
      })
    }
  },
  watch: {
    xData() {
      this.updateChart()
    },
    yData() {
      this.updateChart()
    }
  },
  mounted() {
    const chartDom = this.$refs.chart
    this.chartInstance = echarts.init(chartDom)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bar-chart {
  height: 300px;
  width: 100%;
}
</style>
