import{d as _e,u as ve,c as d,a as n,b as t,w as l,F as I,m as z,e as Q,H as Y,v as _,n as v,j as u,r as o,o as r,D as j,i as c,t as w,g as W,E as p}from"./index-DejdUQV-.js";import{_ as ye}from"./_plugin-vue_export-helper-DlAUqK2U.js";const fe={class:"ai-assistant"},ge={class:"sidebar"},ke={class:"menu-header"},Ce={class:"content"},we={key:0,class:"chat-container"},xe={class:"chat-messages",ref:"messageContainer"},he={class:"avatar"},be={class:"bubble"},Me=["innerHTML"],Ve={key:0,class:"sql-box"},Se={class:"chat-input"},qe={class:"input-actions"},De={class:"card-header"},Ee={key:0,class:"advice-content"},Le={key:0,class:"report-content"},Te={class:"report-actions"},Re={key:3,class:"chat-container"},Pe={class:"chat-messages"},Ie={class:"avatar"},ze={class:"bubble"},He=["innerHTML"],Ae={class:"chat-input"},Ke={class:"input-actions"},Fe=_e({__name:"index",setup(Ne){const H=ve(),y=u("query"),g=u(""),M=u(!1),V=u([{role:"assistant",content:`您好！我是您的数据查询助手。您可以问我：
- "查询本周延期的任务"
- "库存低于安全线的物料有哪些"
- "铝合金班组进行中的任务"`}]),S=u(null),q=u(!1),D=u(""),$=u([{id:1,yacht_name:"海鹰号"},{id:2,yacht_name:"蓝鲸号"}]),E=u(""),L=u(!1),x=u(""),k=u(""),T=u(!1),R=u([{role:"assistant",content:"您好！我是工艺知识助手，熟悉铝合金游艇建造的各类规范。请随时提问！"}]),O=a=>{y.value=a},A=a=>a.replace(/\n/g,"<br>"),K=async()=>{if(!g.value.trim())return;const a=g.value;V.value.push({role:"user",content:a}),g.value="",M.value=!0;try{await new Promise(e=>setTimeout(e,1500)),V.value.push({role:"assistant",content:"根据您的查询，我为您生成了以下 SQL 语句：",sql:"SELECT * FROM tasks WHERE status = 'delayed' AND plan_start >= '2024-02-01'"})}catch(e){p.error(e.message||"查询失败")}finally{M.value=!1}},G=a=>{p.success("执行查询: "+a.substring(0,50)+"...")},J=async()=>{if(!S.value){p.warning("请先选择项目");return}q.value=!0;try{await new Promise(a=>setTimeout(a,2e3)),D.value=`## 采购建议报告

### 1. 紧急采购清单
- 4mm铝合金板 5083-H116：预计3天内用完，建议立即采购200平米
- 铝合金焊丝 ER5356：库存不足，建议采购500kg

### 2. 供应商比价建议
- 中铝：价格适中，质量稳定，推荐
- 西南铝：价格略低，交货期较长

### 3. 库存优化建议
- 铝合金型材库存积压，建议暂停采购
- 建议与供应商协商分批交货`}catch(a){p.error(a.message||"获取建议失败")}finally{q.value=!1}},X=async()=>{L.value=!0;try{await new Promise(a=>setTimeout(a,2e3)),x.value=`## 生产日报 (${E.value||"今日"})

### 一、今日完成任务
1. 飞桥结构设计审核 - 设计部张三
2. 船体放样验收 - 生产部李四

### 二、进行中任务
1. 船体结构制作 (65%) - 预计4月30日完成
2. 电气系统设计 (80%) - 预计2月20日完成

### 三、延期任务
1. 外板矫正 - 延期5天，原因：材料延迟到货

### 四、明日计划
1. 继续船体结构制作
2. 开始电气系统布线

### 五、风险提示
- 铝合金板材库存不足，可能影响后续进度`}catch(a){p.error(a.message||"生成失败")}finally{L.value=!1}},Z=()=>{navigator.clipboard.writeText(x.value),p.success("已复制到剪贴板")},ee=()=>{p.success("导出功能开发中")},F=async()=>{if(!k.value.trim())return;const a=k.value;R.value.push({role:"user",content:a}),k.value="",T.value=!0;try{await new Promise(e=>setTimeout(e,1500)),R.value.push({role:"assistant",content:`根据《铝合金船体建造规范》CCS 要求：

**船体对接焊间隙标准：**

1. **根部间隙**：3-5mm
2. **钝边高度**：1-2mm
3. **角度**：60°±5°

**注意事项：**
- 焊接前需清理坡口及两侧20mm范围内的氧化膜
- 环境温度低于5℃时需预热
- 焊后需进行外观检查和渗透检测

建议参考具体项目的焊接工艺评定报告(WPQR)。`})}catch(e){p.error(e.message||"查询失败")}finally{T.value=!1}};return(a,e)=>{const te=o("Cpu"),i=o("el-icon"),ne=o("Search"),h=o("el-menu-item"),le=o("ShoppingCart"),se=o("Document"),oe=o("Reading"),ae=o("el-menu"),b=o("el-avatar"),m=o("el-button"),N=o("el-input"),U=o("Promotion"),re=o("el-option"),ue=o("el-select"),ie=o("MagicStick"),B=o("el-card"),de=o("el-date-picker"),ce=o("DocumentChecked"),pe=o("CopyDocument"),me=o("Download");return r(),d("div",fe,[n("div",ge,[n("div",ke,[t(i,{size:"32",color:"#409EFF"},{default:l(()=>[t(te)]),_:1}),e[4]||(e[4]=n("span",{class:"title"},"AI 助手",-1))]),t(ae,{"default-active":y.value,onSelect:O},{default:l(()=>[t(h,{index:"query"},{default:l(()=>[t(i,null,{default:l(()=>[t(ne)]),_:1}),e[5]||(e[5]=n("span",null,"智能查询",-1))]),_:1}),t(h,{index:"procurement"},{default:l(()=>[t(i,null,{default:l(()=>[t(le)]),_:1}),e[6]||(e[6]=n("span",null,"采购建议",-1))]),_:1}),t(h,{index:"report"},{default:l(()=>[t(i,null,{default:l(()=>[t(se)]),_:1}),e[7]||(e[7]=n("span",null,"日报生成",-1))]),_:1}),t(h,{index:"knowledge"},{default:l(()=>[t(i,null,{default:l(()=>[t(oe)]),_:1}),e[8]||(e[8]=n("span",null,"工艺知识",-1))]),_:1})]),_:1},8,["default-active"])]),n("div",Ce,[y.value==="query"?(r(),d("div",we,[e[13]||(e[13]=n("div",{class:"chat-header"},[n("h3",null,"💬 智能数据查询"),n("p",{class:"subtitle"},'用自然语言查询系统数据，如"查询本周延期的任务"')],-1)),n("div",xe,[(r(!0),d(I,null,z(V.value,(s,P)=>(r(),d("div",{key:P,class:j(["message",s.role])},[n("div",he,[s.role==="user"?(r(),v(b,{key:0,size:36},{default:l(()=>{var f,C;return[c(w(((C=(f=W(H).userInfo)==null?void 0:f.real_name)==null?void 0:C[0])||"我"),1)]}),_:1})):(r(),v(b,{key:1,size:36,src:"/ai-avatar.png"},{default:l(()=>[...e[9]||(e[9]=[c("🤖",-1)])]),_:1}))]),n("div",be,[n("div",{class:"text",innerHTML:A(s.content)},null,8,Me),s.sql?(r(),d("div",Ve,[n("pre",null,[n("code",null,w(s.sql),1)]),t(m,{type:"primary",size:"small",onClick:f=>G(s.sql)},{default:l(()=>[...e[10]||(e[10]=[c("执行查询",-1)])]),_:1},8,["onClick"])])):_("",!0)])],2))),128))],512),n("div",Se,[t(N,{modelValue:g.value,"onUpdate:modelValue":e[0]||(e[0]=s=>g.value=s),type:"textarea",rows:2,placeholder:"输入您的问题，如：查询铝合金班组本周的任务",onKeyup:Q(Y(K,["ctrl"]),["enter"])},null,8,["modelValue","onKeyup"]),n("div",qe,[e[12]||(e[12]=n("span",{class:"hint"},"Ctrl + Enter 发送",-1)),t(m,{type:"primary",onClick:K,loading:M.value},{default:l(()=>[t(i,null,{default:l(()=>[t(U)]),_:1}),e[11]||(e[11]=c(" 发送 ",-1))]),_:1},8,["loading"])])])])):_("",!0),y.value==="procurement"?(r(),v(B,{key:1},{header:l(()=>[n("div",De,[e[14]||(e[14]=n("span",null,"🛒 AI 采购建议",-1)),t(ue,{modelValue:S.value,"onUpdate:modelValue":e[1]||(e[1]=s=>S.value=s),placeholder:"选择项目",style:{width:"200px"}},{default:l(()=>[(r(!0),d(I,null,z($.value,s=>(r(),v(re,{key:s.id,label:s.yacht_name,value:s.id},null,8,["label","value"]))),128))]),_:1},8,["modelValue"])])]),default:l(()=>[t(m,{type:"primary",onClick:J,loading:q.value},{default:l(()=>[t(i,null,{default:l(()=>[t(ie)]),_:1}),e[15]||(e[15]=c(" 生成采购建议 ",-1))]),_:1},8,["loading"]),D.value?(r(),d("div",Ee,[n("pre",null,w(D.value),1)])):_("",!0)]),_:1})):_("",!0),y.value==="report"?(r(),v(B,{key:2},{header:l(()=>[...e[16]||(e[16]=[n("span",null,"📋 AI 日报生成",-1)])]),default:l(()=>[t(de,{modelValue:E.value,"onUpdate:modelValue":e[2]||(e[2]=s=>E.value=s),type:"date",placeholder:"选择日期","value-format":"YYYY-MM-DD"},null,8,["modelValue"]),t(m,{type:"primary",onClick:X,loading:L.value,style:{"margin-left":"12px"}},{default:l(()=>[t(i,null,{default:l(()=>[t(ce)]),_:1}),e[17]||(e[17]=c(" 生成日报 ",-1))]),_:1},8,["loading"]),x.value?(r(),d("div",Le,[n("div",Te,[t(m,{type:"primary",link:"",onClick:Z},{default:l(()=>[t(i,null,{default:l(()=>[t(pe)]),_:1}),e[18]||(e[18]=c(" 复制 ",-1))]),_:1}),t(m,{type:"primary",link:"",onClick:ee},{default:l(()=>[t(i,null,{default:l(()=>[t(me)]),_:1}),e[19]||(e[19]=c(" 导出 ",-1))]),_:1})]),n("pre",null,w(x.value),1)])):_("",!0)]),_:1})):_("",!0),y.value==="knowledge"?(r(),d("div",Re,[e[23]||(e[23]=n("div",{class:"chat-header"},[n("h3",null,"📚 工艺知识助手"),n("p",{class:"subtitle"},"询问焊接、涂装、检验等工艺规范")],-1)),n("div",Pe,[(r(!0),d(I,null,z(R.value,(s,P)=>(r(),d("div",{key:P,class:j(["message",s.role])},[n("div",Ie,[s.role==="user"?(r(),v(b,{key:0,size:36},{default:l(()=>{var f,C;return[c(w(((C=(f=W(H).userInfo)==null?void 0:f.real_name)==null?void 0:C[0])||"我"),1)]}),_:1})):(r(),v(b,{key:1,size:36},{default:l(()=>[...e[20]||(e[20]=[c("👨‍🔧",-1)])]),_:1}))]),n("div",ze,[n("div",{class:"text",innerHTML:A(s.content)},null,8,He)])],2))),128))]),n("div",Ae,[t(N,{modelValue:k.value,"onUpdate:modelValue":e[3]||(e[3]=s=>k.value=s),type:"textarea",rows:2,placeholder:"输入您的问题，如：船体对接焊间隙标准是多少？",onKeyup:Q(Y(F,["ctrl"]),["enter"])},null,8,["modelValue","onKeyup"]),n("div",Ke,[e[22]||(e[22]=n("span",{class:"hint"},"Ctrl + Enter 发送",-1)),t(m,{type:"primary",onClick:F,loading:T.value},{default:l(()=>[t(i,null,{default:l(()=>[t(U)]),_:1}),e[21]||(e[21]=c(" 提问 ",-1))]),_:1},8,["loading"])])])])):_("",!0)])])}}}),Qe=ye(Fe,[["__scopeId","data-v-b33f88e2"]]);export{Qe as default};
//# sourceMappingURL=index-NIbdHthT.js.map
