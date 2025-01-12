<template>
  <div class="mod-demo-echarts">
    <el-alert
      type="warning"
      :closable="false">
      
    </el-alert>
    <el-row :gutter="20">
      <el-col :span="24">
        <p class="custom-font">网络攻击模板</p>
      </el-col>
      <el-col :span="24">
        <el-card>
          <el-col :span="6">
            <p class="custom-font">DOS攻击</p>
          </el-col>
          
          <el-col :span="9">
            <el-button type="success" @click="qidongdos">启动DOS攻击</el-button>
          </el-col>
          <el-col :span="9">
            <el-button type="success" @click="gbdos">关闭DOS攻击</el-button>
          </el-col>
        </el-card>
      </el-col>
      <el-col :span="24">
        <el-col :span="16">
          <div class="">
            <svg width="100%" height="300">
              <!-- 定义UA服务器 -->
              <image href="/static/img/6.png" x="100" y="100" width="100" height="100" />
              <text x="90" y="220" font-size="14">UA服务器</text>
              <!-- 定义dos攻击主机 -->
              <image href="/static/img/2.png" x="700" y="100" width="100" height="100" />
              <text x="700" y="220" font-size="14">dos攻击主机</text>

              <!-- 绘制箭头路径 -->
              <!-- 第一条路径 -->
             <path
              ref="animatedPath7"
              d="M 750 100 Q 400 50 160 110"
              fill="none"
              :stroke="dosloag === 1 ? 'red' : 'white'"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition7)" :fill="dosloag === 1 ? 'red' : 'white'"/>
            
            </svg>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="container">
                
                <!-- 温度卡片 -->
                <el-col :span="24" class="col-center">
                  <div class="card3">
                    <div class="card-top">{{ dosshu }}</div>
                    <div class="card-bottom">累计发包数量</div>
                  </div>
                </el-col>
                
        </div>
        </el-col>
      </el-col>
    </el-row>
    <el-col :span="24">
        <p class="custom-font">假冒攻击</p>
      </el-col>
    <el-row :gutter="20">
      
      <el-col :span="24">
        <el-col :span="12">
          <el-card>
            <!-- 卡片区域 -->
            <el-col :span="24">
              <div class="container">
                <el-col :span="6" class="col-center">
                  <p class="custom-font">实时监听传感器数据</p>
                </el-col>
                <!-- 温度卡片 -->
                <el-col :span="6" class="col-center">
                  <div class="card">
                    <div class="card-top">{{ getdata1.temperature }}</div>
                    <div class="card-bottom">温度</div>
                  </div>
                </el-col>
                <!-- 压力卡片 -->
                <el-col :span="6" class="col-center">
                  <div class="card">
                    <div class="card-top">{{ getdata1.pressure }}</div>
                    <div class="card-bottom">压力</div>
                  </div>
                </el-col>
                <!-- 空气质量卡片 -->
                <el-col :span="6" class="col-center">
                  <div class="card">
                    <div class="card-top">{{ getdata1.airQuality }}</div>
                    <div class="card-bottom">空气质量</div>
                  </div>
                </el-col>
              </div>
            </el-col>
            <!-- 折线图区域 -->
            <el-col :span="24" class="chart-container">
              <el-card>
                <div id="J_chartLineBox" class="chart-box"></div>
              </el-card>
            </el-col>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <p class="custom-font">篡改传感器数据</p>
            <!-- 第一个表单 -->
            <el-col :span="24">
              <el-form :model="dataForm" :rules="dataFormRules" ref="dataForm" label-width="100px">
                <el-col :span="16" class="chart-container">
                  <el-row class="form-horizontal" type="flex" justify="space-between" align="middle">
                    <el-col>
                      <el-row type="flex" align="middle">
                        <span style="margin-right: 10px;"><p class="custom-font">温  度  ：</p> </span>
                        <el-form-item prop="temperature">
                          <el-input
                            v-model="dataForm.temperature"
                            placeholder="输入篡改的温度"
                            style="width: 400px; height: 40px; margin-right: 20px;"
                          ></el-input>
                        </el-form-item>
                      </el-row>
                    </el-col>
                  </el-row>
                </el-col>

                <el-col :span="8">
                  <el-row class="form-vertical">
                    <el-col :span="12" style="margin-bottom: 10px;">
                      <el-button
                        type="primary"
                        block
                        style="height: 50px; width: 100px"
                        @click="dataFormSubmit"
                      >启动修改</el-button>
                    </el-col>
                    <el-col :span="12">
                      <el-button
                        type="success"
                        block
                        style="height: 50px; width: 100px"
                        @click="pauseModification1"
                      >暂停修改</el-button>
                    </el-col>
                  </el-row>
                </el-col>
              </el-form>
              <el-form :model="dataForm2" :rules="dataFormRules2" ref="dataForm2" label-width="100px">
                <el-col :span="16" class="chart-container">
                  <el-row class="form-horizontal" type="flex" justify="space-between" align="middle">
                    <el-col>
                      <el-row type="flex" align="middle">
                        <span style="margin-right: 10px;"><p class="custom-font">压  力 ：</p></span>
                        <el-form-item prop="pressure">
                          <el-input
                            v-model="dataForm2.pressure"
                            placeholder="输入篡改的压力"
                            style="width: 400px; height: 40px; margin-right: 20px;"
                          ></el-input>
                        </el-form-item>
                      </el-row>
                    </el-col>
                  </el-row>
                </el-col>

                <el-col :span="8">
                  <el-row class="form-vertical">
                    <el-col :span="12" style="margin-bottom: 10px;">
                      <el-button
                        type="primary"
                        block
                        style="height: 50px; width: 100px"
                        @click="dataFormSubmit2"
                      >启动修改</el-button>
                    </el-col>
                    <el-col :span="12">
                      <el-button
                        type="success"
                        block
                        style="height: 50px; width: 100px"
                        @click="tingyali"
                      >暂停修改</el-button>
                    </el-col>
                  </el-row>
                </el-col>
              </el-form>
              <el-form :model="dataForm3" :rules="dataFormRules3" ref="dataForm3" label-width="100px">
                <el-col :span="16" class="chart-container">
                  <el-row class="form-horizontal" type="flex" justify="space-between" align="middle">
                    
                    <el-col>
                      <el-row type="flex" align="middle">
                        <span style="margin-right: 10px;"><p class="custom-font">空气质量：</p> </span>
                        <el-form-item  prop="airQuality">
                          <el-input
                            v-model="dataForm3.airQuality"
                            placeholder="输入篡改的空气质量"
                            style="width: 400px; height: 40px; margin-right: 20px;">
                          </el-input>
                        </el-form-item>
                      </el-row>
                    </el-col>
                  </el-row>
                </el-col>

                <el-col :span="8">
                  <el-row class="form-vertical">
                    <el-col :span="12" style="margin-bottom: 10px;">
                      <el-button
                        type="primary"
                        block
                        style="height: 50px; width: 100px"
                        @click="dataFormSubmit3"
                      >启动修改</el-button>
                    </el-col>
                    <el-col :span="12">
                      <el-button
                        type="success"
                        block
                        style="height: 50px; width: 100px"
                        @click="zantingkongqi"
                      >暂停修改</el-button>
                    </el-col>
                  </el-row>
                </el-col>
              </el-form>
              <el-col :span="24">
                      <el-button type="success" block style="height: 50px; width: 100px" @click="pauseModification">暂停全部修改</el-button>
              </el-col>
            </el-col>
              <hr>
            
            <el-divider></el-divider>
          </el-card>
        </el-col>
      </el-col>
      <el-col :span="24">
        <div class="animation-container">
          <svg width="100%" height="600">
            <!-- 定义设备 -->
            <image href="/static/img/1.png" x="50" y="100" width="100" height="100" />
            <text x="90" y="220" font-size="14">设备</text>

            <!-- 定义假冒主机 -->
            <image href="/static/img/2.png" x="500" y="100" width="100" height="100" />
            <text x="520" y="220" font-size="14">假冒主机</text>

            <!-- 定义主PLC -->
            <image href="/static/img/3.png" x="950" y="100" width="100" height="100" />
            <text x="980" y="220" font-size="14">主PLC</text>

            <!-- 定义前端 -->
            <image href="/static/img/4.png" x="500" y="400" width="100" height="100" />
            <text x="520" y="520" font-size="14">Web</text>
            <!-- 绘制箭头路径 -->
            <!-- 第一条路径 -->
            <path
              ref="animatedPath1"
              d="M 150 100 Q 250 50 550 100"
              fill="none"
              stroke="gray"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition1)" fill="gray" />

            <!-- 第二条路径 -->
            <path
              ref="animatedPath2"
              d="M 560 100 Q 750 50 980 100"
              fill="none"
              :stroke="loag === 1 ? 'red' : 'gray'"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition2)" :fill="loag === 1 ? 'red' : 'gray'" />

            <!-- 第三条路径 -->
            <path
              ref="animatedPath3"
              d="M 970 200 Q 750 250 560 200"
              fill="none"
              stroke="gray"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition3)" fill="gray" />

            <!-- 第四条路径 -->
            <path
              ref="animatedPath4"
              d="M 550 200 Q 250 250 150 200"
              fill="none"
              stroke="gray"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition4)" fill="gray" />
            <path
              ref="animatedPath5"
              d="M 550 200 Q 480 250 550 400"
              fill="none"
              stroke="gray"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition5)" fill="gray" />

            <!-- Web 发向假冒主机 -->
            <path
              ref="animatedPath6"
              d="M 570 400 Q 640 250 560 200"
              fill="none"
              :stroke="loag === 1 ? 'red' : 'gray'"
              stroke-width="2"
            />
            <polygon :points="getArrowPoints(arrowPosition6)" :fill="loag === 1 ? 'red' : 'gray'" />
          </svg>
        </div>

      </el-col>
      <el-col :span="24">
        <el-col :span="24">
          <p class="custom-font">设备的当前状态</p>
            <el-col :span="24">
              <div class="container">
                <!-- 温度卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.iron_water }}</div>
                    <div class="card-bottom">初始铁水温度(K)</div>
                  </div>
                </el-col>
                <!-- 压力卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.steel_plate }}</div>
                    <div class="card-bottom">初始钢板厚度(m)</div>
                  </div>
                </el-col>
                <!-- 空气质量卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.roller }}</div>
                    <div class="card-bottom">轧辊间距(mm)</div>
                  </div>
                </el-col>
                <!-- 温度卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.mold }}</div>
                    <div class="card-bottom">模具温度(K)</div>
                  </div>
                </el-col>
                <!-- 压力卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.conveyor_belt1 }}</div>
                    <div class="card-bottom">传送带1速度(cm/s)</div>
                  </div>
                </el-col>
                <!-- 空气质量卡片 -->
                <el-col :span="4" class="col-center">
                  <div class="card2">
                    <div class="card-top">{{ getdata2.conveyor_belt2 }}</div>
                    <div class="card-bottom">传送带2速度(cm/s)</div>
                  </div>
                </el-col>
              </div>
            </el-col>
        </el-col>
        
      </el-col>
      
    </el-row>
  </div>
</template>
<script>
import axios from "axios";
export default {
  name: 'ChartWithButtons',
  methods: {
    handleButton1() {
      console.log('按钮1被点击');
    },
    handleButton2() {
      console.log('按钮2被点击');
    }
  },
  name: "RoundedCard",
  data() {
    return {
      t: 0, // 动画时间
      loag: 0,
      dosloag: 0,
      dosshu: 0,
      intervalId: null,
      athLength: 0, // 设置路径长度
      dashOffset: 0, // 初始偏移量，用于隐藏路径
      pathLength: 0, // 路径总长度
      currentLength: 0, // 当前动画位置
      arrowPosition1: { x: 0, y: 0 }, // 第一条路径的箭头位置
      arrowPosition2: { x: 0, y: 0 }, // 第二条路径的箭头位置
      arrowPosition3: { x: 0, y: 0 }, // 第三条路径的箭头位置
      arrowPosition4: { x: 0, y: 0 }, // 第四条路径的箭头位置
      arrowPosition5: { x: 0, y: 0 }, // 假冒主机发向 Web 的箭头位置
      arrowPosition6: { x: 0, y: 0 }, // Web 发向假冒主机的箭头位置
      arrowPosition7: { x: 0, y: 0 }, // Web 发向假冒主机的箭头位置
      variableValue: 17, // 你可以根据实际需求动态设置
      chartLine: null,  //折线图
      chartScatter: null,
      wendu: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    dataForm: {
      temperature: ''// 温度
    },
    getdata1: {
      temperature: '', // 温度
      pressure: '',    // 压力
      airQuality: ''   // 空气质量
    },
    dataForm2: {
      pressure: ''
      },
    dataForm3: {
      airQuality: ''
      },
      getdata2: {
        iron_water: '',
        steel_plate: '',
        roller: '',
        mold: '',
        conveyor_belt1: '',
        conveyor_belt2: ''
      },
      dataGroup: {
      wendu: [],
      yali: [],
      kqzl: []
    },
    dataFormRules: {
      temperature: [
        { required: true, message: '请输入温度', trigger: 'blur' }
      ]
    },
    dataFormRules2: {
        pressure: [
          { required: true, message: "请输入压力值", trigger: "blur" },
        ],
      },
    dataFormRules3: {
      airQuality: [
          { required: true, message: "请输入空气质量", trigger: "blur" },
        ],
      },
    };
  },
  
  mounted () {
      
      //this.animateArrow();
      this.$nextTick(() => {
      //this.initChartLine()
      //this.initChartScatter()

      const path1 = this.$refs.animatedPath1;
      const path2 = this.$refs.animatedPath2;
      const path3 = this.$refs.animatedPath3;
      const path4 = this.$refs.animatedPath4;
      const path5 = this.$refs.animatedPath5;
      const path6 = this.$refs.animatedPath6;
      const path7 = this.$refs.animatedPath7;

      if (path5) this.animateArrow(path5, "arrowPosition5");
      if (path6) this.animateArrow(path6, "arrowPosition6");
      if (path1) this.animateArrow(path1, "arrowPosition1");
      if (path2) this.animateArrow(path2, "arrowPosition2");
      if (path3) this.animateArrow(path3, "arrowPosition3");
      if (path4) this.animateArrow(path4, "arrowPosition4");

      if (path7) this.animateArrow(path7, "arrowPosition7");
    });
  },
  activated () {
      // 由于给echart添加了resize事件, 在组件激活时需要重新resize绘画一次, 否则出现空白bug
      if (this.chartLine) {
        this.chartLine.resize()
      }
      if (this.chartScatter) {
        this.chartScatter.resize()
      }
  },
  methods: {
    /**
     * 动画逻辑，用于动态更新箭头位置
     * @param {SVGPathElement} path 路径元素
     * @param {String} arrowKey 对应箭头位置的数据键名
     */
     animateArrow(path, arrowKey) {
      const pathLength = path.getTotalLength(); // 获取路径总长度
      const animationDuration = 2000; // 动画持续时间（2秒）
      const frameRate = 16; // 帧率 (16ms 一帧)
      let currentLength = 0; // 当前路径位置

      setInterval(() => {
        if (currentLength >= pathLength) {
          currentLength = 0; // 如果到达路径终点，重置为起点
        } else {
          currentLength += pathLength / (animationDuration / frameRate); // 每帧增加路径长度
        }
        const point = path.getPointAtLength(currentLength); // 获取路径上当前长度对应的点
        this[arrowKey] = { x: point.x, y: point.y }; // 更新对应箭头的位置
      }, frameRate);
    },

    /**
     * 计算箭头的三角形顶点
     * @param {Object} arrowPosition 箭头的当前位置
     * @returns {String} 三角形的顶点坐标
     */
    getArrowPoints(arrowPosition) {
      const size = 8; // 箭头大小
      const centerX = 500; // 默认中间参考点（调整角度用）
      const centerY = 150; // 默认中间参考点（调整角度用）
      const angle = Math.atan2(arrowPosition.y - centerY, arrowPosition.x - centerX); // 箭头方向角度
      const x = arrowPosition.x;
      const y = arrowPosition.y;

      // 计算三角形顶点位置
      const point1 = `${x},${y}`; // 三角形顶点
      const point2 = `${x - size * Math.cos(angle - Math.PI / 6)},${y - size * Math.sin(angle - Math.PI / 6)}`; // 左下角
      const point3 = `${x - size * Math.cos(angle + Math.PI / 6)},${y - size * Math.sin(angle + Math.PI / 6)}`; // 右下角

      return `${point1} ${point2} ${point3}`; // 返回三角形的三个顶点
    },
    async qidongdos() {
      try {
        const response = await axios.post("http://localhost:5000/example/test", {
          target_ip: "192.168.103.133", // 替换为实际目标 IP
          target_port: 8001            // 替换为实际目标端口
        });
        // 根据响应结果处理
        if (response.status === 200 && response.data.status === "success") {
          this.$message.success(response.data.message);
          this.dosloag = 1;
        } else {
          this.$message.error("请求失败！");
        }
        if (!this.intervalId) {
          this.intervalId = setInterval(() => {
            // 生成 6000 到 10000 的随机数
            const randomIncrement = Math.floor(Math.random() * (10000 - 6000 + 1)) + 6000;
            this.dosshu += randomIncrement; // 累加随机值
          }, 1000);
        }
      } catch (error) {
        console.error("请求错误:", error);
        this.$message.error("请求过程中发生错误！");
      }
     
    },
    async gbdos() {
      try {
        const response = await axios.post("http://localhost:5000/example/stop", {
          loag : 0
        });

        // 根据响应结果处理
        if (response.status === 200 && response.data.status === "success") {
          this.$message.success(response.data.message);
          this.dosloag = 0;
        } else {
          this.$message.error("请求失败！");
        }
        if (this.intervalId) {
          clearInterval(this.intervalId); // 清除定时器
          this.intervalId = null; // 重置定时器 ID
        }
      } catch (error) {
        console.error("请求错误:", error);
        this.$message.error("请求过程中发生错误！");
      }
    },
  
    dataFormSubmit() {
      // 进行表单验证
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // 提交表单数据
          this.$http({
            url: 'http://localhost:8080/renren-fast/app/data/modify', // 确保路径正确
            method: 'post',
            data: this.$http.adornData({
              temperature: this.dataForm.temperature,
              pressure: 0,
              airQuality: 0
            })
          }).then(({ data }) => {
            if (data && data.code === 0) {
              this.$message.success('数据提交成功！')
              this.loag = 1;
            } else {
              this.$message.error(data.msg || '提交失败，请重试！')
            }
          }).catch((error) => {
            this.$message.error('网络请求失败，请检查！')
            console.error(error)
          })
        }
      })
    },
    dataFormSubmit2() {
      // 进行表单验证
      this.$refs['dataForm2'].validate((valid) => {
        if (valid) {
          // 提交表单数据
          this.$http({
            url: 'http://localhost:8080/renren-fast/app/data/modify2', // 确保路径正确
            method: 'post',
            data: this.$http.adornData({
              temperature: 0,
              pressure: this.dataForm2.pressure,
              airQuality: 0
            })
          }).then(({ data }) => {
            if (data && data.code === 0) {
              this.$message.success('数据提交成功！')
              this.loag = 1;
            } else {
              this.$message.error(data.msg || '提交失败，请重试！')
            }
          }).catch((error) => {
            this.$message.error('网络请求失败，请检查！')
            console.error(error)
          })
        }
      })
    },
    dataFormSubmit3() {
      // 进行表单验证
      this.$refs['dataForm3'].validate((valid) => {
        if (valid) {
          // 提交表单数据
          this.$http({
            url: 'http://localhost:8080/renren-fast/app/data/modify3', // 确保路径正确
            method: 'post',
            data: this.$http.adornData({
              temperature: 0,
              pressure: 0,
              airQuality: this.dataForm3.airQuality
            })
          }).then(({ data }) => {
            if (data && data.code === 0) {
              this.$message.success('数据提交成功！')
              this.loag = 1;
            } else {
              this.$message.error(data.msg || '提交失败，请重试！')
            }
          }).catch((error) => {
            this.$message.error('网络请求失败，请检查！')
            console.error(error)
          })
        }
      })
    },
    pauseModification() {
      // 表单一暂停发送请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/pause1',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          load: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
          this.loag = 0;
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    pauseModification1() {
      // 表单一温度暂停发送请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/tingwendu',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          load: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    tingyali() {
      // 表单一温度暂停发送请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/ting',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          pressure: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    zantingkongqi() {
      // 表单一温度暂停发送请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/tingkongqi',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          airQuality: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    qidongarp() {
      // 启动ARP请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/arp1',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          arp: 1
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    zantingarp() {
      // 暂停ARP请求到后端
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/arp2',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          arp: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    
    pauseModification2() {
      // 表单二暂停发送请求到后端
      
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/pause2',  // 后端接口
        method: 'post',
        data: this.$http.adornData({
          load: 0
        })
      }).then(({ data }) => {
        if (data && data.code === 0) {
          this.$message.success('修改已暂停！');
        } else {
          this.$message.error(data.msg || '暂停失败，请重试！');
        }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    //从后端获取数据
    fetchLatestData() {
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/getLatestData',  // 后端接口
        method: 'get'
      }).then(({ data }) => {
        // 在这里更新getdata1变量的值
        this.getdata1.temperature = data.temperature;
        this.getdata1.pressure = data.pressure;
        this.getdata1.airQuality = data.airQuality;

         // 根据返回的代码显示提示消息
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
     },
     fetchLatestData1() {
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/getTgzmData',  // 后端接口
        method: 'get'
      }).then(({ data }) => {
        // 在这里更新getdata1变量的值
        this.getdata2.iron_water = data.ironWater;
        this.getdata2.steel_plate = data.steelPlate;
        this.getdata2.roller = data.roller;
        this.getdata2.mold = data.mold;
        this.getdata2.conveyor_belt1 = data.conveyorBelt1;
        this.getdata2.conveyor_belt2 = data.conveyorBelt2;
         // 根据返回的代码显示提示消息
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
     },
     getdataGroup() { 
      this.$http({
        url: 'http://localhost:8080/renren-fast/app/data/getdataGroup',  // 后端接口
        method: 'get'
      }).then(({ data }) => {
        // 确保后端返回的数据符合预期
        if (data && data.code === 0 && data.data) { // 这里访问的是 "data" 而不是 "readings"
        // 初始化三个数组
        const wenduArray = [];
        const yaliArray = [];
        const kqzlArray = [];

        // 使用 for 循环处理 readings 数组
        for (let i = 0; i < data.data.length; i++) {
          const reading = data.data[i];  // 获取每一条数据
          
          // 将温度、压力和空气质量分别推入对应的数组
          wenduArray.push(reading.temperature);
          yaliArray.push(reading.pressure);
          kqzlArray.push(reading.airQuality);
        }

        // 输出数组的值，调试查看数据是否正确
        console.log("温度数组: ", wenduArray);  // 输出温度数据
        console.log("压力数组: ", yaliArray);  // 输出压力数据
        console.log("空气质量数组: ", kqzlArray);  // 输出空气质量数据
        
        // 更新 Vue 数据模型
        this.dataGroup.wendu = wenduArray;
        this.dataGroup.yali = yaliArray;
        this.dataGroup.kqzl = kqzlArray;

        // 输出数组的值，调试查看数据是否正确
        console.log("0000温度数组: ", this.dataGroup.wendu);  // 输出温度数据
        console.log("000压力数组: ", this.dataGroup.yali);  // 输出压力数据
        console.log("000空气质量数组: ", this.dataGroup.kqzl);  // 输出空气质量数据
        this.initChartLine();
        
      } else {
        this.$message.error('加载失败，请重试！');
      }
      }).catch((error) => {
        this.$message.error('网络请求失败，请检查！');
        console.error(error);
      });
    },
    initChartLine () {
        var option = {
          'title': {
            'text': '近20次设备状态的变化'
          },
          'tooltip': {
            'trigger': 'axis'
          },
          'legend': {
            'data': [ '温度', '压力', '空气质量' ]
          },
          'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': true
          },
          'toolbox': {
            'feature': {
              'saveAsImage': { }
            }
          },
          'xAxis': {
            'type': 'category',
            'boundaryGap': false,
            'data': [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
          },
          'yAxis': {
            'type': 'value'
          },
          'series': [
            {
              'name': '温度',
              'type': 'line',
              'stack': '总量',
              'data': this.dataGroup.wendu
            },
            {
              'name': '压力',
              'type': 'line',
              'stack': '总量',
              'data': this.dataGroup.yali
            },
            {
              'name': '空气质量',
              'type': 'line',
              'stack': '总量',
              'data': this.dataGroup.kqzl
            }
            
          ]
        }
        this.chartLine = echarts.init(document.getElementById('J_chartLineBox'))
        this.chartLine.setOption(option)
        window.addEventListener('resize', () => {
          this.chartLine.resize()
        })
      },
  },
  created() {
    this.fetchLatestData();
      
    this.fetchLatestData1();
    this.getdataGroup();
    setInterval(() => {
      this.fetchLatestData();
      this.fetchLatestData1();
      this.getdataGroup();
    }, 1000);
  }
};
</script>

<style scoped>
.animation-container {
  width: 100%;
  height: auto;
}
/* 折线图容器样式 */
.chart-container {
  margin-top: 0px; /* 上方卡片和折线图之间的距离 */
  display: block; /* 保证折线图单独占据一行 */
}
.chart-box {
  /* 折线图盒子 */
  min-height: 5000px;
  background: #f7f7faf8; /* 可选：折线图背景色 */
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.xui{
  background: #e6e6ebf8;
  color: #3c6c9c;
}
.custom-font {
  font-family: 'Arial', sans-serif; /* 可根据需要选择一个你喜欢的字体 */
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50; /* 你可以修改颜色来匹配设计风格 */
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: flex-start;
  gap: 45%; /* 控制按钮之间的间距 */
}

.el-button {
  margin-right: 10px;
  padding: 10px 10px;
}
/* el-col 的居中样式 */
.col-center {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100%; /* 需要高度来居中 */
}
.container {
  display: flex;
  justify-content: space-between; /* 卡片间距自动分配 */
  align-items: center; /* 垂直居中 */
  height: 180px; /* 父容器高度 */
  background-color: #fff; /* 背景颜色（灰） */
  margin-bottom: 20px; /* 和折线图的距离 */
}


.card {
  width: 120px; /* 卡片宽度 */
  height: 150px; /* 卡片高度 */
  background: linear-gradient(180deg, #1e90ff, #00c6ff); /* 渐变背景色 */
  border-radius: 5px; /* 圆角 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  flex-direction: column;
  color: white; /* 字体颜色 */
  font-family: Arial, sans-serif; /* 字体 */
}
.card2 {
  width: 120px; /* 卡片宽度 */
  height: 150px; /* 卡片高度 */
  background: linear-gradient(180deg, #2263a3, #2b8aa5); /* 渐变背景色 */
  border-radius: 5px; /* 圆角 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  flex-direction: column;
  color: white; /* 字体颜色 */
  font-family: Arial, sans-serif; /* 字体 */
}
.card3 {
  width: 200px; /* 卡片宽度 */
  height: 220px; /* 卡片高度 */
  background: linear-gradient(180deg, #7d93a8, #9cc0ca); /* 渐变背景色 */
  border-radius: 5px; /* 圆角 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 阴影 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  flex-direction: column;
  color: white; /* 字体颜色 */
  font-family: Arial, sans-serif; /* 字体 */
}
.card-top {
  /* 卡片内容 */
  font-size: 36px; /* 上部数字字体大小 */
  font-weight: bold;
  margin-bottom: 10px; /* 数字和线条的间距 */
}

.card-bottom {
  font-size: 14px; /* 下部文字字体大小 */
  border-top: 1px solid rgba(255, 255, 255, 0.5); /* 分隔线 */
  padding-top: 5px; /* 分隔线和文字的间距 */
  width: 80%; /* 分隔线宽度 */
  text-align: center;
}
.mod-demo-echarts {
    > .el-alert {
      margin-bottom: 10px;
    }
    > .el-row {
      margin-top: -10px;
      margin-bottom: -10px;
      .el-col {
        padding-top: 10px;
        padding-bottom: 10px;
      }
    }
    .chart-box {
      min-height: 400px;
    }
  }
  .form-horizontal {
  margin-bottom: 20px;
}
.form-vertical {
  display: flex;
  flex-direction: row;
}
</style>
