


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
console.log(mydata_{{rd_id}});
var data = mydata_{{rd_id}}.data;
var t_color_{{rd_id}} = "black";
var xmin_max_ymin_max = mydata_{{rd_id}}.xmin_max_ymin_max
// See https://github.com/ecomfe/echarts-stat
echarts.registerTransform(ecStat.transform.clustering);
var CLUSTER_COUNT = 6;
var DIENSIION_CLUSTER_INDEX = 2;
var COLOR_ALL = [
    '#37A2DA', '#e06343', '#37a354', '#b55dba', '#b5bd48', '#8378EA', '#96BFFF'
];
var pieces = [];
for (var i = 0; i < CLUSTER_COUNT; i++) {
    pieces.push({
        value: i,
        label: 'cluster ' + i,
        color: COLOR_ALL[i]
    });
}


var dom = document.getElementById('container_{{rd_id}}');
var chart_{{rd_id}} = echarts.init(dom);
var app = {};
option = null;

option = {
    dataset: [{
        source: data
    }, {
        transform: {
            type: 'ecStat:clustering',
            // print: true,
            config: {
                clusterCount: CLUSTER_COUNT,
                outputType: 'single',
                outputClusterIndexDimension: DIENSIION_CLUSTER_INDEX
            }
        }
    }],

    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color: function(){return t_color_{{rd_id}};},
    },

    tooltip: {
        position: 'top'
    },
    visualMap: {
        type: 'piecewise',
        top: 'middle',
        min: 0,
        max: CLUSTER_COUNT,
        left: 10,
        splitNumber: CLUSTER_COUNT,
        dimension: DIENSIION_CLUSTER_INDEX,
        pieces: pieces
    },
    grid: {
        left: 120
    },
    xAxis: {
        min: xmin_max_ymin_max[0],
        max: xmin_max_ymin_max[1],
        axisLabel: {
            textStyle: {
                fontSize: 17,
                color: function(){return t_color_{{rd_id}};},
            }
        }        
    },
    yAxis: {
        min: xmin_max_ymin_max[2],
        max: xmin_max_ymin_max[3],        
        axisLabel: {
            textStyle: {
                fontSize: 17,
                color: function(){return t_color_{{rd_id}};},
            }
        }        
    },
    series: {
        type: 'scatter',
        encode: { tooltip: [0, 1] },
        symbolSize: 15,
        itemStyle: {
            borderColor: '#555'
        },
        datasetIndex: 1
    },
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

};


if (option && typeof option === "object") {
    chart_{{rd_id}}.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_{{rd_id}}.resize();
    });

}