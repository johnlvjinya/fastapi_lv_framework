


// **********************************************************************************************************************
// 图标类型: area_stack
// container_id: c_0
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=area_stack.json
// **********************************************************************************************************************
function get_my_data_c_0() {
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
var mydata_c_0 = get_my_data_c_0();
console.log(mydata_c_0)
var t_color_c_0 = "black";

var dom = document.getElementById('container_c_0');
var chart_c_0 = echarts.init(dom);
var app = {};
option = null;

option = {

    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:t_color_c_0,
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
        data: mydata_c_0.legend_data,
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
            data: mydata_c_0.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c_0;},
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
                    color:  function(){return t_color_c_0;},
                }
            },             
        }
    ],
    series: mydata_c_0.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c_0=='white'){
                        t_color_c_0 = 'black';
                    }else{
                        t_color_c_0 = 'white';
                    }
                    
                  const element = document.getElementById("container_c_0");
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
    chart_c_0.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_0.resize();
    });

}
// **********************************************************************************************************************************************************


// **********************************************************************************************************************
// 图标类型: bar
// container_id: c_1
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar.json
// **********************************************************************************************************************

function get_my_data_c_1() {
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
var mydata_c_1 = get_my_data_c_1();
console.log(mydata_c_1);
var t_color_c_1 = "black";
var dom = document.getElementById('container_c_1');
var chart_c_1 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c_1;},
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
        data: mydata_c_1.legend_data,
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
            data: mydata_c_1.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c_1;},
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
                    color: function(){return t_color_c_1;},
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
    series: mydata_c_1.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                  const element = document.getElementById("container_c_1");
                    if (t_color_c_1=='white'){
                        t_color_c_1 = 'black';
                    }else{
                        t_color_c_1 = 'white';
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
    chart_c_1.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_1.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: bar_stack
// container_id: c_2
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar_stack.json
// **********************************************************************************************************************

function get_my_data_c_2() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar_stack.json",
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
var mydata_c_2 = get_my_data_c_2();
// console.log(mydata_c_2)
var t_color_c_2 = "black";
var dom = document.getElementById('container_c_2');
var chart_c_2 = echarts.init(dom);
var app = {};
option = null;

option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color: function(){return t_color_c_2;},
      
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
            fontSize: 16,
            // fontStyle: 'italic',
            // fontWeight: 'bold'
        },
    },
    legend: {
        icon: 'rectangle',
        data: mydata_c_2.legend_data,
        right: '4%',
        padding:[20,0,0,0],   //可设定图例[距上方距离，距右方距离，距下方距离，距左方距离]
        textStyle: {
            fontSize: 20,
            color: function(){return t_color_c_2;},
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
            // boundaryGap: false,
            data: mydata_c_2.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c_2;},
                }
            }            
        }
    ],
    yAxis: [
        {
            type: 'value',
            splitLine: {show : false},             
            axisTick:{ show:true,},   //y轴刻度线
            axisLine:{ show:true,},    //y轴
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_2;},
                }
            }
        }
    ],
    series: mydata_c_2.series,
    // backgroundColor:'white', //设置无背景色 
    // backgroundColor:'rgba(0,0,0,0)', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏查看',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c_2=='white'){
                        t_color_c_2 = 'black';
                    }else{
                        t_color_c_2 = 'white';
                    }

                  const element = document.getElementById("container_c_2");
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
    chart_c_2.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_2.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: china_map
// container_id: c_3
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=china_map.json
// **********************************************************************************************************************

function get_my_data_c_3() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=china_map.json",
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

var mydata_c_3 = get_my_data_c_3();
console.log(mydata_c_3);
var t_color_c_3 = "black";
var mydata = mydata_c_3;
var dom = document.getElementById('container_c_3');
var chart_c_3 = echarts.init(dom);
var app = {};
option = null;

var data = mydata.data
var province = mydata.province

var res = [];
for (var j = 0; j < data.length; j++) {
    res.push({
        name: province[j],
        value: data[j]
    });
}
res.sort(function(a, b) {
    return a.value - b.value;
});
var res1 = [];
var res2 = [];
for (var t = 0; t < 10; t++) {
    res1[t] = res[res.length - 1 - t].name;
    res2[t] = res[res.length - 1 - t].value;
}

option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color: function(){return t_color_c_3;},
    },
    
    
    tooltip: {
        show: true,
        formatter: function(params) {
            return params.name + '：' + params.value
        },
        textStyle : {
            color: 'black',
            decoration: 'none',
            fontSize: 16,
            // fontStyle: 'italic',
            // fontWeight: 'bold'
        },
        
    },
    visualMap: {
        type: 'piecewise',
        text: mydata.text,
        pieces: mydata.pieces,
        orient: 'vertical',
        itemSymbol: 'circle',
        itemWidth: 20,
        itemHeight: 20,
        showLabel: true,
        seriesIndex: [0],
        textStyle: {
            color: '#7B93A7'
        },
        bottom: '10%',
        left: "5%",
    },
    grid: {
        right: '5%',
        top: '20%',
        bottom: '10%',
        width: '20%'
    },
    xAxis: {
        min: mydata.xAxis_min,
        max: mydata.xAxis_max,
        axisTick: {
            show: false,
        },
        axisLabel: {
            textStyle: {
                fontSize: 20,
                color:function(){return t_color_c_3;},
            },
            interval: 0
        },
    },
    yAxis: {
        inverse: true,
        offset: '2',
        'type': 'category',
        data: res1,
        nameTextStyle: {
            color: '#fff'
        },
        axisTick: {
            show: false,
        },
        axisLabel: {
            textStyle: {
                fontSize: 20,
                color:function(){return t_color_c_3;},
            },
            interval: 0
        },
        axisLine: {
            show: false
        },
        splitLine: {
            show: false
        },
    },
    geo: {
        map: 'china',
        right: '35%',
        left: '5%',
        label: {
            emphasis: {
                show: false,
            }
        },
        itemStyle: {
            emphasis: {
                areaColor: '#99FF99'
            }
        }
    },
    series: [{
            name: 'mapSer',
            type: 'map',
            map: 'china',
            roam: false,
            geoIndex: 0,
            label: {
                show: false,
            },
            data: res
        },
        {
            'name': 'barSer',
            'type': 'bar',
            zlevel: 2,
            barWidth: '40%',
            label: {
                normal: {
                    show: true,
                    fontSize: 14,
                    position: 'right',
                    formatter: '{c}'
                }
            },
            data: res2,
            itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [{
                                colorStops: [{
                                    offset: 0,
                                    color: '#FF0000' // 0% 处的颜色
                                }, {
                                    offset: 1,
                                    color: '#990000' // 100% 处的颜色
                                }]
                            },
                            {
                                colorStops: [{
                                    offset: 0,
                                    color: '#00C0FA' // 0% 处的颜色
                                }, {
                                    offset: 1,
                                    color: '#2F95FA' // 100% 处的颜色
                                }]
                            }
                        ];
                        if (params.dataIndex < 3) {
                            return colorList[0]
                        } else {
                            return colorList[1]
                        }
                    },
                }
            }
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
                  const element = document.getElementById("container_c_3");
                    if (t_color_c_3=='white'){
                        t_color_c_3 = 'black';
                    }else{
                        t_color_c_3 = 'white';
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
    chart_c_3.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_3.resize();
    });

}














// **********************************************************************************************************************
// 图标类型: funnel
// container_id: c_4
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=funnel.json
// **********************************************************************************************************************

function get_my_data_c_4() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=funnel.json",
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
var mydata_c_4 = get_my_data_c_4();
console.log(mydata_c_4);
var t_color_c_4 = "black";
var dom = document.getElementById('container_c_4');
var chart_c_4 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:'white',
    },
    
    
    title: {
        text: '漏斗图',
        subtext: ' '
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c}%",
        axisPointer: {
            type: 'cross'
        },
        textStyle : {
            color: 'black',
            decoration: 'none',
            fontSize: 16,
            // fontStyle: 'italic',
            // fontWeight: 'bold'
        },

    },
    toolbox: {
        feature: {
            dataView: {readOnly: false},
            restore: {},
            saveAsImage: {}
        }
    },
    legend: {
        // left: 'center',
        // top: 'bottom',         
        icon: 'rectangle',
        data: mydata_c_4.legend_data,
        right: '4%',
        padding:[20,0,0,0],   //可设定图例[距上方距离，距右方距离，距下方距离，距左方距离]
        textStyle: {
            fontSize: 20,
            color:function(){return t_color_c_4;},
         }
    },

    series: [
        {
            name:'漏斗图',
            type:'funnel',
            left: '10%',
            top: 60,
            //x2: 80,
            bottom: 60,
            width: '80%',
            // height: {totalHeight} - y - y2,
            min: 0,
            max: 100,
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside'
            },
            labelLine: {
                length: 10,
                lineStyle: {
                    width: 1,
                    type: 'solid'
                }
            },
            itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
            },
            emphasis: {
                label: {
                    fontSize: 20
                }
            },
            data: mydata_c_4.data,
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
                  const element = document.getElementById("container_c_4");
                    if (t_color_c_4=='white'){
                        t_color_c_4 = 'black';
                    }else{
                        t_color_c_4 = 'white';
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
    chart_c_4.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_4.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: hist
// container_id: c_5
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=hist.json
// **********************************************************************************************************************

function get_my_data_c_5() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=hist.json",
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
var mydata_c_5 = get_my_data_c_5();
console.log(mydata_c_5);
var t_color_c_5 = "black";
var dom = document.getElementById('container_c_5');
var chart_c_5 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c_5;},
    },

    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        },
        textStyle : {
            color: 'black',
            decoration: 'none',
            fontSize: 16,
        },
     
    },
    xAxis: {
        type: 'category',
        data: mydata_c_5.name_list,
        axisLabel: {
            textStyle: {
                fontSize: 20,
                color: function(){return t_color_c_5;},
            }
        }, 
        axisLine:{ //y轴
            show:true,
        },
    },
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_5;},
                }
            },
            splitLine: {show : false},             
            axisTick:{ //y轴刻度线
                show:true,
            },
            axisLine:{ //y轴
                show:true,
            },

        },
       ],
    grid:{
        x: 100,
        y: 30,
        x2: 50,
        y2: 50
      },
    series: [
    {
        data: mydata_c_5.data_list,
        type: 'bar',
        color: mydata_c_5.color,
        // showBackground: true,
        // backgroundStyle: {
        //     color: 'azure'
        // }        
    }],
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c_5=='white'){
                        t_color_c_5 = 'black';
                    }else{
                        t_color_c_5 = 'white';
                    }

                  const element = document.getElementById("container_c_5");
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
    chart_c_5.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_5.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: hist_compare
// container_id: c_6
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=hist_compare.json
// **********************************************************************************************************************

function get_my_data_c_6() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=hist_compare.json",
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
var mydata_c_6 = get_my_data_c_6();
console.log(mydata_c_6);
var t_color_c_6 = "black";
var dom = document.getElementById('container_c_6');
var chart_c_6 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c_6;},
    },
    
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        },
        textStyle : {
            color: 'black',
            decoration: 'none',
            fontSize: 16,
        },
     
    },
    xAxis: {
        type: 'category',
        data: mydata_c_6.name_list,
        axisLabel: {
            textStyle: {
                fontSize: 20,
                color: function(){return t_color_c_6;},
            }
        }, 
        axisLine:{ //y轴
            show:true,
        },
    },
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_6;},
                }
            },
            splitLine: {show : false},             
            axisTick:{ //y轴刻度线
                show:true,
            },
            axisLine:{ //y轴
                show:true,
            },

        },
       ],

    grid:{
        x: 100,
        y: 30,
        x2: 50,
        y2: 50
      },
    series: [
        {
            name: mydata_c_6.c1_name,
            data: mydata_c_6.data_list_c1,
            type: 'bar',
            color:'rgba(255,0,0,.5)',
            // showBackground: true,
            // backgroundStyle: {
            //     color: 'azure'
            // }
        },
        {
            barGap: '-100%',
            name:mydata_c_6.c2_name,
            data:mydata_c_6.data_list_c2,
            type: 'bar',
            color:'rgba(0,255,0,.5)',
            // showBackground: true,
            // backgroundStyle: {
            //     color: 'azure'
            // }
        }],
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                  const element = document.getElementById("container_c_6");
                    if (t_color_c_6=='white'){
                        t_color_c_6 = 'black';
                    }else{
                        t_color_c_6 = 'white';
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
    chart_c_6.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_6.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: line_bars_mix
// container_id: c_7
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=line_bars_mix.json
// **********************************************************************************************************************
function get_my_data_c_7() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=line_bars_mix.json",
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
var mydata_c_7 = get_my_data_c_7();
console.log(mydata_c_7);
var t_color_c_7 = "black";
console.log(t_color_c_7);
var dom = document.getElementById('container_c_7');
var chart_c_7 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c_7;},

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
            fontSize: 16,
        },
     
    },
    // legend: {
    //     data: mydata_c_7.legend_data
    // },
    legend: {
        // left: 'center',
        // top: 'bottom',         
        icon: 'rectangle',
        data: mydata_c_7.legend_data,
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
            data: mydata_c_7.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_7;},
                }
            }, 
            axisLine:{ //y轴
                show:true,
            },          
        }
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_7;},
                }
            },
            splitLine: {show : false},             
            axisTick:{ //y轴刻度线
                show:true,
            },
            axisLine:{ //y轴
                show:true,
            },

        },
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color:  function(){return t_color_c_7;},
                }
            },
            axisTick:{ //y轴刻度线
                show:true,
            },
            axisLine:{ //y轴
                show:true,
            },


            splitLine: {show : false},            
            // name: '次坐标',
            // min: 0,
            // max: 25,
            // interval: 5,
            // axisLabel: {
            //     formatter: '{value} °C'
            // }
        }
    ],
    
    series: mydata_c_7.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c_7=='white'){
                        t_color_c_7 = 'black';
                    }else{
                        t_color_c_7 = 'white';
                    }
                  
                  console.log(t_color_c_7);
                  const element = document.getElementById("container_c_7");
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
    chart_c_7.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_7.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: map_heat_shanghai
// container_id: c_8
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=map_heat_shanghai.json
// **********************************************************************************************************************

function get_my_data_c_8() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=map_heat_shanghai.json",
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


var mydata_c_8 = get_my_data_c_8();
// console.log(mydata_c_8);
var t_color_c_8 = "black";
var dom = document.getElementById('container_c_8');
var chart_c_8 = echarts.init(dom);
var app = {};
var option;

var cdmap = "/static/map_json/上海.json";
chart_c_8.showLoading();


$.getJSON(cdmap, function(geoJson) {
    chart_c_8.hideLoading();
    echarts.registerMap('shanghai', geoJson);

var data = mydata_c_8.data;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color: function(){return t_color_c_8;},
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
            text: mydata_c_8.title,
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
            min: mydata_c_8.min_v,
            max: mydata_c_8.max_v,
            text: ['High', 'Low'],
            textStyle: {
                color:function(){return t_color_c_8;},
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
                    if (t_color_c_8=='white'){
                        t_color_c_8 = 'black';
                    }else{
                        t_color_c_8 = 'white';
                    }

                  const element = document.getElementById("container_c_8");
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
        chart_c_8.setOption(option, true);
        window.addEventListener("resize",function(){
            chart_c_8.resize();
        });

    }

});


// **********************************************************************************************************************
// 图标类型: multi_line
// container_id: c_9
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=multi_line.json
// **********************************************************************************************************************
function get_my_data_c_9() {
    var datas= null;//定义一个全局变量
    $.ajax({
        type:"GET",
        url:"/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=multi_line.json",
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
var mydata_c_9 = get_my_data_c_9();
console.log(mydata_c_9);
var t_color_c_9 = "black";
var dom = document.getElementById('container_c_9');
var chart_c_9 = echarts.init(dom);
var app = {};
option = null;
option = {
    textStyle: {
      fontFamily: 'times new roman',
      fontSize:20,
      color:function(){return t_color_c_9;},
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
            fontSize: 16,
        },
     
    },
    legend: {
        data: mydata_c_9.legend_data,
        right: '4%',
        icon: 'line',
        padding:[20,0,0,0],   //可设定图例[距上方距离，距右方距离，距下方距离，距左方距离]
        textStyle: {
            fontSize: 20,
            color:function(){return t_color_c_9;},
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
            axisTick: false,
            data: mydata_c_9.xAxis_data,
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_9;},
                }
            }, 
            axisLine:{ //y轴
                show:true,
            },  

        }
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 20,
                    color: function(){return t_color_c_9;},
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
    series: mydata_c_9.series,
    // backgroundColor:'white', //设置无背景色    
    toolbox:{
            show: true,
            feature: {
              myFull: {
                show: true,
                title: '全屏',
                icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891",

                onclick: (e) => {
                    if (t_color_c_9=='white'){
                        t_color_c_9 = 'black';
                    }else{
                        t_color_c_9 = 'white';
                    }
                  
                  const element = document.getElementById("container_c_9");
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
    chart_c_9.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_9.resize();
    });

}


// **********************************************************************************************************************
// 图标类型: pie
// container_id: c_10
// 数据url:/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=pie.json
// **********************************************************************************************************************
function get_my_data_c_10() {
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


var mydata_c_10 = get_my_data_c_10();
console.log(mydata_c_10);
var t_color_c_10 = "black";
var dom = document.getElementById('container_c_10');
var chart_c_10 = echarts.init(dom);
var app = {};

option = null;
option = {
    textStyle: {
        fontSize:20,
        color: function(){return t_color_c_10;},
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
    //     data: mydata_c_10.name_list
    // },

    // legend: {
    //     left: 'center',
    //     top: 'bottom',        
    //     icon: 'rectangle',
    //     data: mydata_c_10.name_list,
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
            data: mydata_c_10.data_list
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
                    if (t_color_c_10=='white'){
                        t_color_c_10 = 'black';
                    }else{
                        t_color_c_10 = 'white';
                    }
                    
                  const element = document.getElementById("container_c_10");
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
    chart_c_10.setOption(option, true);
    window.addEventListener("resize",function(){
        chart_c_10.resize();
    });

}