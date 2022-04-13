


// **********************************************************************************************************************
// 图标类型: bar
// container_id: c1
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar.json
// **********************************************************************************************************************

function get_my_data_c1() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar.json",
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
var mydata_c1 = get_my_data_c1();
console.log(mydata_c1);
var t_color_c1 = "black";
var dom = document.getElementById('container_c1');
var chart_c1 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c1;},
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
        data: mydata_c1.legend_data,
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
            data: mydata_c1.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c1;},
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
                    color: function(){return t_color_c1;},
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
    series: mydata_c1.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                  const element = document.getElementById("container_c1");
                    if (t_color_c1=='white'){
                        t_color_c1 = 'black';
                    }else{
                        t_color_c1 = 'white';
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
    chart_c1.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c1.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: area_stack
// container_id: c2
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=area_stack.json
// **********************************************************************************************************************
function get_my_data_c2() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=area_stack.json",
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
var mydata_c2 = get_my_data_c2();
console.log(mydata_c2)
var t_color_c2 = "black";

var dom = document.getElementById('container_c2');
var chart_c2 = echarts.init(dom);
var app = {};
option = null;

option = {

    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:t_color_c2,
    },
    
    title: {
        text: ''
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
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
        icon:'line',
        data: mydata_c2.legend_data,
        textStyle: {
            fontSize: 20,
            color: function(){},
         }        
    },
    toolbox: {
        feature: {
            saveAsImage: {}
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
            boundaryGap: false,
            data: mydata_c2.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c2;},
                }
            },            
        }
    ],
    yAxis: [
        {
            splitLine:{
                show:false
            },
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c2;},
                }
            },             
        }
    ],
    series: mydata_c2.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c2=='white'){
                        t_color_c2 = 'black';
                    }else{
                        t_color_c2 = 'white';
                    }
                    
                  const element = document.getElementById("container_c2");
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
    chart_c2.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c2.resize();
    });

}
// **********************************************************************************************************************************************************


// **********************************************************************************************************************
// 图标类型: pie
// container_id: c3
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=pie.json
// **********************************************************************************************************************
function get_my_data_c3() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=pie.json",
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


var mydata_c3 = get_my_data_c3();
console.log(mydata_c3);
var t_color_c3 = "black";
var dom = document.getElementById('container_c3');
var chart_c3 = echarts.init(dom);
var app = {};

option = null;
option = {
    textStyle: {
        fontSize:20,
        color: function(){return t_color_c3;},
    },

    tooltip: {
        trigger: 'item',
        formatter: '{b} : {c} ({d}%)',
        textStyle: {
          fontFamily: 'times new roman',
          fontSize:16,
          color: "black",
        },

    },
    // legend: {
    //     left: 'center',
    //     top: 'bottom',
    //     data: mydata_c3.name_list
    // },

    // legend: {
    //     left: 'center',
    //     top: 'bottom',        
    //     icon: 'rectangle',
    //     data: mydata_c3.name_list,
    //     right: '4%',
    //     padding:[20,0,0,0],   //可设定图例[距上方距离，距右方距离，距下方距离，距左方距离]
    //     textStyle: {
    //         fontSize: 20,
    //         color: "white"
    //      }
    // },

    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '占比',
            type: 'pie',
            radius: ['25%', '95%'],
            roseType: 'area',
            data: mydata_c3.data_list
        }
    ],
    // backgroundColor:'rgba(0,0,0,0)', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c3=='white'){
                        t_color_c3 = 'black';
                    }else{
                        t_color_c3 = 'white';
                    }
                    
                  const element = document.getElementById("container_c3");
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
    chart_c3.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c3.resize();
    });

}