


// **********************************************************************************************************************
// 图标类型: {{plt_type}}
// container_id: {{rd_id}}
// 数据url:{{js_data_url}}
// **********************************************************************************************************************

function get_my_data_{{rd_id}}() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"{{js_data_url}}",
        async:false,
        data:"",
        success:function(res){
            // 获取数据并保存至变量
            // console.log(res)
            datas = res;
            }
        });
    return datas
}


var mydata_{{rd_id}} = get_my_data_{{rd_id}}();
// console.log(mydata_{{rd_id}});
var t_color_{{rd_id}} = "black";
var dom = document.getElementById('container_{{rd_id}}');
var chart_{{rd_id}} = echarts.init(dom);
var app = {};
var option;

var cdmap = "/static/map_json/上海.json";
chart_{{rd_id}}.showLoading();


$.getJSON(cdmap, function(geoJson) {
    chart_{{rd_id}}.hideLoading();
    echarts.registerMap('shanghai', geoJson);

var data = mydata_{{rd_id}}.data;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color: function(){return t_color_{{rd_id}};},
    },
        
    baseOption: {
        animationDurationUpdate: 1000,
        animationEasingUpdate: 'quinticInOut',
        timeline: {
            axisType: 'category',
            orient: 'vertical',
            autoPlay: true,
            inverse: true,
            playInterval: 2000,
            left: null,
            right: 5,
            top: 20,
            bottom: 20,
            width: 46,
            height: null,
            label: {
                normal: {
                    textStyle: {
                        color: '#ddd'
                    }
                },
                emphasis: {
                    textStyle: {
                        color: '#fff'
                    }
                }
            },
            symbol: 'none',
            lineStyle: {
                color: '#555'
            },
            checkpointStyle: {
                color: '#bbb',
                borderColor: '#777',
                borderWidth: 1
            },
            controlStyle: {
                showNextBtn: false,
                showPrevBtn: false,
                normal: {
                    color: '#666',
                    borderColor: '#666'
                },
                emphasis: {
                    color: '#aaa',
                    borderColor: '#aaa'
                }
            },
            data: data.map(function(ele) {
                return ele.time
            })
        },
        // backgroundColor: '#404a59',
        title: {
            text: mydata_{{rd_id}}.title,
            subtext: '',
            left: 'center',
            top: 'top',
            textStyle: {
                fontSize: 25,
                color: 'rgba(255,255,255, 0.9)'
            }
        },
        tooltip: {
            formatter: function(params) {
                if ('value' in params.data) {
                    return params.data.value[2] + ': ' + params.data.value[0];
                }
            }
        },
        grid: {
            left: '12%',
            right: '45%',
            top: '70%',
            bottom: 20
        },
        xAxis: {},
        yAxis: {},
        series: [
        {
            id: 'map',
            type: 'map',
            mapType: 'shanghai',
            label:{
                show: true
            },            
            top: '1%',
            bottom: '1%',
            left: '50%',
            itemStyle: {
                normal: {
                    areaColor: '#323c48',
                    borderColor: '#404a59'
                },
                emphasis: {
                    label: {
                        show: true
                    },
                    areaColor: 'rgba(255,255,255, 0.5)'
                }
            },
            data: []
        }, 
        {
            id: 'bar',
            type: 'bar',
            tooltip: {
                formatter: ''
            },
            data: [],
            label: {
                normal: {
                    textStyle: {
                        color: '#ddd'
                    }
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: '#ddd'
                    }
                }
            },
            itemStyle: {
                normal: {
                    borderColor: 'rgba(0,0,0,0.3)',
                    borderSize: 1
                }
            },
            data: []
        }, 
        {
            id: 'pie',
            type: 'pie',
            right: '70%',
            top: '-350%',
            radius: ['10%', '50%'],
            center: ['70%', '85%'],
            roseType: 'radius',
            tooltip: {
                formatter: '{b} {d}%'
            },
            data: [],
            label: {
                normal: {
                    textStyle: {
                        color: '#ddd'
                    }
                }
            },
            labelLine: {
                normal: {
                    lineStyle: {
                        color: '#ddd'
                    }
                }
            },
            itemStyle: {
                normal: {
                    borderColor: 'rgba(0,0,0,0.3)',
                    borderSize: 1
                }
            }
        }]
    },
    options: [],

};

for (var i = 0; i < data.length; i++) {
    //计算其余国家GDP
    var restPercent = 100;
    var restValue = 0;
    data[i].data.forEach(function(ele) {
        restPercent = restPercent - ele.value[1];
    });
    restValue = data[i].data[0].value[0] * (restPercent / data[i].data[0].value[1]);
    console.log(restPercent);
    console.log(restValue);
    option.options.push({
        visualMap: [{
            dimension: 0,
            left: 10,
            itemWidth: 12,
            min: mydata_{{rd_id}}.min_v,
            max: mydata_{{rd_id}}.max_v,
            text: ['High', 'Low'],
            textStyle: {
                color:function(){return t_color_{{rd_id}};},
            },
            inRange: {
                color: ['royalblue', 'cornflowerblue',  'lightskyblue','greenyellow', 'yellow', 'orangered', 'red']
            }
        }],
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.1],
            axisLabel: {
                show: false,
            }
        },
        yAxis: {
            type: 'category',
            axisLabel: {
                textStyle: {
                    color: '#ddd'
                }
            },
            data: data[i].data.map(function(ele) {
                return ele.value[2]
            })//.reverse()
        },
        series: [
          {
              id: 'map',
              data: data[i].data
          }, 
          {
              id: 'bar',
              data: data[i].data.map(function(ele) {
                  return ele.value[0]
              }).sort(function(a, b) {
                  return a > b
              })
          }, 
          {
              id: 'pie',
              data: data[i].data.map(function(ele) {
                  return {
                      name: ele.value[2],
                      value: ele.value
                  }
              }),
          }

          ],
          
          // backgroundColor:'white', //设置无背景色
          toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_{{rd_id}}=='white'){
                        t_color_{{rd_id}} = 'black';
                    }else{
                        t_color_{{rd_id}} = 'white';
                    }

                  const element = document.getElementById("container_{{rd_id}}");
                  if (element.requestFullScreen) { // HTML W3C 提议
                        element.requestFullScreen();
                      } else if (element.msRequestFullscreen) { // IE11
                        element.msRequestFullScreen();
                      } else if (element.webkitRequestFullScreen) { // Webkit (works in Safari5.1 and Chrome 15)
                        element.webkitRequestFullScreen();
                      } else if (element.mozRequestFullScreen) { // Firefox (works in nightly)
                        element.mozRequestFullScreen();
                      }
                  // 退出全屏
                  if (element.requestFullScreen) {
                        document.exitFullscreen();
                      } else if (element.msRequestFullScreen) {
                        document.msExitFullscreen();
                      } else if (element.webkitRequestFullScreen) {
                        document.webkitCancelFullScreen();
                      } else if (element.mozRequestFullScreen) {
                        document.mozCancelFullScreen();
                      }


                },
              },
            },
          },
    })
};


    if (option && typeof option === "object") {
        chart_{{rd_id}}.setOption(option, true);
        window.addEventListener("resize",function(){
            chart_{{rd_id}}.resize();
        });

    }

});