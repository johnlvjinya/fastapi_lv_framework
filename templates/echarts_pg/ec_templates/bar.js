


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
var t_color_{{rd_id}} = "black";
var dom = document.getElementById('container_{{rd_id}}');
var chart_{{rd_id}} = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_{{rd_id}};},
    },

    title: {
        text: ''
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        },
        textStyle : {
            color: 'black',
            decoration: 'none',
            // fontFamily: 'Verdana, sans-serif',
            fontSize: 16,
            // fontStyle: 'italic',
            // fontWeight: 'bold'
        },
        
    },
    legend: {
        // left: 'center',
        // top: 'bottom',         
        icon: 'rectangle',
        data: mydata_{{rd_id}}.legend_data,
        right: '4%',
        padding:[20,0,0,0],   //可设定图例[距上方距离，距右方距离，距下方距离，距左方距离]
        textStyle: {
            fontSize: 20,
            color: function(){},
         }
    },

    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
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
            axisTick: true,
            data: mydata_{{rd_id}}.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_{{rd_id}};},
                }
            },
        }
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_{{rd_id}};},
                }
            },
            splitLine: {show : false},             
            axisTick:{ //y轴刻度线
                show:true,
            },
            axisLine:{ //y轴
                show:true,
            },
        }
    ],
    series: mydata_{{rd_id}}.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                  const element = document.getElementById("container_{{rd_id}}");
                    if (t_color_{{rd_id}}=='white'){
                        t_color_{{rd_id}} = 'black';
                    }else{
                        t_color_{{rd_id}} = 'white';
                    }
                  
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